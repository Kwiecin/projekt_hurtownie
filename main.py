from tkinter import * # importujemy biblioteki
from tkinter import ttk, messagebox # importujemy biblioteki
import tkintermapview # importujemy biblioteki
from geopy.geocoders import Nominatim # importujemy biblioteki

hurtownie = []
pracownicy = []
klienci = []

geolocator = Nominatim(user_agent="hurtownie_app") # tworzenie obiektu

def get_coordinates(street, city): # definicja funkcji
    try:
        if not city.strip():
            raise ValueError("Brak miasta")
        query = f"{street.strip()}, {city.strip()}, Polska" if street else f"{city.strip()}, Polska" # tworzenie obiektu
        loc = geolocator.geocode(query, timeout=10) # tworzenie obiektu
        if loc:
            return [loc.latitude, loc.longitude]
    except Exception as e:
        print(f"[Błąd geolokalizacji] {street}, {city}: {e}")
    return [52.23, 21.0]

class Hurtownia: # definicja klasy
    def __init__(self, name, street, city): # definicja funkcji
        self.name = name
        self.street = street
        self.city = city
        self.coordinates = get_coordinates(street, city) # tworzenie obiektu
        self.marker = map_widget.set_marker(*self.coordinates, text=f"H: {self.name}") # tworzenie obiektu

class Pracownik: # definicja klasy
    def __init__(self, name, surname, street, city, hurtownia): # definicja funkcji
        self.name = name
        self.surname = surname
        self.street = street
        self.city = city
        self.hurtownia = hurtownia
        self.coordinates = get_coordinates(street, city) # tworzenie obiektu
        self.marker = map_widget.set_marker(*self.coordinates, text=f"P: {self.name} {self.surname}") # tworzenie obiektu

class Klient: # definicja klasy
    def __init__(self, name, surname, city, hurtownia, street=""): # definicja funkcji
        self.name = name
        self.surname = surname
        self.city = city
        self.street = street
        self.hurtownia = hurtownia
        self.coordinates = get_coordinates(street, city) # tworzenie obiektu
        self.marker = map_widget.set_marker(*self.coordinates, text=f"K: {self.name} {self.surname}") # tworzenie obiektu
