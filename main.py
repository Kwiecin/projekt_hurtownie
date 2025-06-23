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
def refresh_comboboxes(): # definicja funkcji
    names = [h.name for h in hurtownie]
    combo_p_hurtownia['values'] = names
    combo_k_hurtownia['values'] = names
    combo_szczegoly['values'] = names

def delete_selected(listbox, dataset): # definicja funkcji
    index = listbox.curselection() # tworzenie obiektu
    if not index:
        return
    obj = dataset[index[0]]
    if hasattr(obj, "marker") and obj.marker:
        obj.marker.delete() # usunięcie elementu
        obj.marker = None
    del dataset[index[0]]
    listbox.delete(index[0]) # usunięcie elementu
    refresh_comboboxes()

def show_details_worker(): # definicja funkcji
    i = listbox_szczegoly_pracownicy.curselection() # tworzenie obiektu
    if i:
        name = listbox_szczegoly_pracownicy.get(i[0]) # tworzenie obiektu
        for p in pracownicy:
            if f"{p.name} {p.surname}" == name:
                label_output.config(text=f"Pracownik:\n{p.name} {p.surname}\n{p.street}, {p.city}\nHurtownia: {p.hurtownia.name}") # tworzenie obiektu
                map_widget.set_position(*p.coordinates) # ustawienie pozycji mapy
                map_widget.set_zoom(13) # ustawienie poziomu przybliżenia

def show_details_client(): # definicja funkcji
    i = listbox_szczegoly_klienci.curselection() # tworzenie obiektu
    if i:
        name = listbox_szczegoly_klienci.get(i[0]) # tworzenie obiektu
        for k in klienci:
            if f"{k.name} {k.surname}" == name:
                label_output.config(text=f"Klient:\n{k.name} {k.surname}\n{(k.street+', ' if k.street else '')}{k.city}\nHurtownia: {k.hurtownia.name}") # tworzenie obiektu
                map_widget.set_position(*k.coordinates) # ustawienie pozycji mapy
                map_widget.set_zoom(13) # ustawienie poziomu przybliżenia