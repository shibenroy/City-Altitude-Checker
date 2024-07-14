import customtkinter as ctk
from tkinter import messagebox
import requests

def get_altitude(city):
    try:
        # Open-Meteo Geocoding API 
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        response = requests.get(geocode_url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        if not data['results']:
            messagebox.showerror("Error", "City not found")
            return

        lat = data['results'][0]['latitude']
        lon = data['results'][0]['longitude']

        
        elevation_url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        response = requests.get(elevation_url)
        response.raise_for_status() 
        data = response.json()

        if 'elevation' in data:
            altitude = data['elevation']
            result_label.configure(text=f"Altitude of {city} is {altitude} meters.")
        else:
            messagebox.showerror("Error", "Could not fetch altitude or altitude data not available")
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        messagebox.showerror("Request Error", f"Request error occurred: {req_err}")
    except ValueError as json_err:
        messagebox.showerror("JSON Error", f"JSON decode error: {json_err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_submit():
    city = city_entry.get()
    if city:
        get_altitude(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")


ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")  
root = ctk.CTk()
root.title("City Altitude Finder")
root.geometry("400x300")  


frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)


title_label = ctk.CTkLabel(frame, text="City Altitude Finder", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(pady=10)


city_label = ctk.CTkLabel(frame, text="Enter city:")
city_label.pack(pady=5)
city_entry = ctk.CTkEntry(frame, width=200)
city_entry.pack(pady=5)


submit_button = ctk.CTkButton(frame, text="Get Altitude", command=on_submit)
submit_button.pack(pady=20)

result_label = ctk.CTkLabel(frame, text="")
result_label.pack(pady=10)

root.mainloop()


'''
Made By Astericc(Shiben Roy)
:D
'''