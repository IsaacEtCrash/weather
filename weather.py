from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# Clé API OpenWeatherMap 
API_KEY = "d950743303a8efbf9a0be627afbd5ebb"

root = Tk()
root.title("Application de météo")
root.geometry("900x500+300+200")
root.resizable(False, False)

def seMeterer():
    try:
        ville = texfield.get().strip()
        if not ville:
            raise ValueError("Veuillez entrer un nom de ville valide.")

        geolocalisation = Nominatim(user_agent="geoapiExercices")
        localisation = geolocalisation.geocode(ville)

        if localisation is None:
            raise ValueError("Ville introuvable. Vérifiez l'orthographe.")

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=localisation.longitude, lat=localisation.latitude)

        if result is None:
            raise ValueError("Impossible de déterminer le fuseau horaire.")

        home = pytz.timezone(result)
        heure_locale = datetime.now(home)
        heure_actuelle = heure_locale.strftime("%I:%M %p")
        heure.config(text=heure_actuelle)
        nom.config(text="TEMPS ACTUEL")

        # Requête API météo avec latitude et longitude
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={localisation.latitude}&lon={localisation.longitude}&appid={API_KEY}&units=metric&lang=fr"
        response = requests.get(api_url)

        if response.status_code != 200:
            raise ValueError("Impossible d'obtenir les données météo.")

        json_data = response.json()

        condition = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'])
        pression = json_data['main']['pressure'] 
        humidite = json_data['main']['humidity'] 
        vent = json_data['wind']['speed']  

        t.config(text=f"{temp}°C")
        c.config(text=f"{condition.capitalize()} | RESSENTI {temp}°C")

        w.config(text=f"{vent} m/s")
        h.config(text=f"{humidite} %")
        d.config(text=f"{condition.capitalize()}")
        p.config(text=f"{pression} hPa")

    except ValueError as ve:
        messagebox.showerror("Erreur", str(ve))
    except requests.exceptions.RequestException:
        messagebox.showerror("Erreur", "Problème de connexion Internet.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")

# Interface Graphique
recharge_image = PhotoImage(file="search.png")
monImage = Label(image=recharge_image)
monImage.place(x=20, y=20)

texfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
texfield.place(x=50, y=40)
texfield.focus()

icon_recherche = PhotoImage(file="search_icon.png")
monImage_icon = Button(image=icon_recherche, borderwidth=0, cursor="hand2", bg="#404040", command=seMeterer)
monImage_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Cadre
cadre_image = PhotoImage(file="box.png")
monCadre_image = Label(image=cadre_image)
monCadre_image.pack(padx=5, pady=5, side=BOTTOM)

# Temps
nom = Label(root, font=("arial", 15, "bold"))
nom.place(x=30, y=100)
heure = Label(root, font=("Helvetica", 20))
heure.place(x=30, y=130)

# Labels météo
label1 = Label(root, text="VENT", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITÉ", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
