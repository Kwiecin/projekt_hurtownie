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
def filtruj_dla_hurtowni(event=None): # definicja funkcji
    wybrana = combo_szczegoly.get() # tworzenie obiektu
    if not wybrana:
        return
    hurtownia = next((h for h in hurtownie if h.name == wybrana), None) # tworzenie obiektu
    if not hurtownia:
        return
    listbox_szczegoly_pracownicy.delete(0, END) # usunięcie elementu
    listbox_szczegoly_klienci.delete(0, END) # usunięcie elementu
    for obj in hurtownie + pracownicy + klienci:
        if hasattr(obj, "marker") and obj.marker:
            obj.marker.delete() # usunięcie elementu
            obj.marker = None
    hurtownia.marker = map_widget.set_marker(*hurtownia.coordinates, text=f"H: {hurtownia.name}") # tworzenie obiektu
    map_widget.set_position(*hurtownia.coordinates) # ustawienie pozycji mapy
    map_widget.set_zoom(10) # ustawienie poziomu przybliżenia
    for p in pracownicy:
        if p.hurtownia.name == wybrana:
            listbox_szczegoly_pracownicy.insert(END, f"{p.name} {p.surname}") # dodanie wpisu do listy
            p.marker = map_widget.set_marker(*p.coordinates, text=f"P: {p.name} {p.surname}") # tworzenie obiektu
    for k in klienci:
        if k.hurtownia.name == wybrana:
            listbox_szczegoly_klienci.insert(END, f"{k.name} {k.surname}") # dodanie wpisu do listy
            k.marker = map_widget.set_marker(*k.coordinates, text=f"K: {k.name} {k.surname}") # tworzenie obiekt
# === GUI ===
root = Tk() # tworzymy główne okno aplikacji
root.title("System Hurtowni")
root.geometry("1400x800") # ustawienie rozmiaru okna

notebook = ttk.Notebook(root)
notebook.pack(side=LEFT, fill=BOTH, expand=True) # umieszczenie elementu w interfejsie

frame_hurtownie = Frame(notebook) # tworzenie obiektu
frame_pracownicy = Frame(notebook)
frame_klienci = Frame(notebook)
frame_szczegoly = Frame(notebook)

notebook.add(frame_hurtownie, text="Hurtownie") # tworzenie obiektu
notebook.add(frame_pracownicy, text="Pracownicy")
notebook.add(frame_klienci, text="Klienci")
notebook.add(frame_szczegoly, text="Szczegóły")


# === HURTOWNIE ===
entry_h_name = Entry(frame_hurtownie) # pole tekstowe do wprowadzania danych
entry_h_street = Entry(frame_hurtownie)
entry_h_city = Entry(frame_hurtownie)
Label(frame_hurtownie, text="Nazwa").pack() # etykieta tekstowa
entry_h_name.pack() # umieszczenie elementu w interfejsie
Label(frame_hurtownie, text="Ulica").pack()
entry_h_street.pack()
Label(frame_hurtownie, text="Miasto").pack() # etykieta tekstowa
entry_h_city.pack()

def add_hurtownia(): # definicja funkcji
    name = entry_h_name.get().strip() # tworzenie obiektu
    street = entry_h_street.get().strip()
    city = entry_h_city.get().strip()
    if not name or not city:
        messagebox.showwarning("Błąd", "Uzupełnij nazwę i miasto hurtowni.") # wyświetlenie komunikatu
        return
    h = Hurtownia(name, street, city) # tworzenie obiektu
    hurtownie.append(h) # dodanie elementu do listy
    listbox_hurtownie.insert(END, h.name) # dodanie wpisu do listy
    refresh_comboboxes()
    entry_h_name.delete(0,END); entry_h_street.delete(0,END); entry_h_city.delete(0,END) # usunięcie elementu

Button(frame_hurtownie, text="Dodaj", command=add_hurtownia).pack() # przycisk
listbox_hurtownie = Listbox(frame_hurtownie) # lista elementów
listbox_hurtownie.pack() # umieszczenie elementu w interfejsie
Button(frame_hurtownie, text="Usuń", command=lambda: delete_selected(listbox_hurtownie, hurtownie)).pack() # przycisk

# === PRACOWNICY ===
entry_p_name = Entry(frame_pracownicy) # pole tekstowe do wprowadzania danych
entry_p_surname = Entry(frame_pracownicy)
entry_p_street = Entry(frame_pracownicy)
entry_p_city = Entry(frame_pracownicy)
combo_p_hurtownia = ttk.Combobox(frame_pracownicy, state="readonly") # rozwijana lista wyboru
Label(frame_pracownicy, text="Imię").pack() # etykieta tekstowa
entry_p_name.pack() # umieszczenie elementu w interfejsie
Label(frame_pracownicy, text="Nazwisko").pack()
entry_p_surname.pack()
Label(frame_pracownicy, text="Ulica").pack()
entry_p_street.pack()
Label(frame_pracownicy, text="Miasto").pack()
entry_p_city.pack()
Label(frame_pracownicy, text="Hurtownia").pack()
combo_p_hurtownia.pack()
def add_pracownik(): # definicja funkcji
    name = entry_p_name.get().strip() # tworzenie obiektu
    surname = entry_p_surname.get().strip()
    street = entry_p_street.get().strip()
    city = entry_p_city.get().strip()
    hurtownia_name = combo_p_hurtownia.get().strip()
    if not name or not surname or not city or not hurtownia_name:
        messagebox.showwarning("Błąd", "Uzupełnij dane pracownika i wybierz hurtownię.") # wyświetlenie komunikatu
        return
    h = next(h for h in hurtownie if h.name == hurtownia_name) # tworzenie obiektu
    p = Pracownik(name, surname, street, city, h) # tworzenie obiektu
    pracownicy.append(p) # dodanie elementu do listy
    listbox_pracownicy.insert(END, f"{p.name} {p.surname}") # dodanie wpisu do listy
    for e in (entry_p_name, entry_p_surname, entry_p_street, entry_p_city): e.delete(0,END) # usunięcie elementu

Button(frame_pracownicy, text="Dodaj", command=add_pracownik).pack()
listbox_pracownicy = Listbox(frame_pracownicy) # lista elementów
listbox_pracownicy.pack() # umieszczenie elementu w interfejsie
Button(frame_pracownicy, text="Usuń", command=lambda: delete_selected(listbox_pracownicy, pracownicy)).pack() # przycisk

# === KLIENCI ===
entry_k_name = Entry(frame_klienci) # pole tekstowe do wprowadzania danych
entry_k_surname = Entry(frame_klienci)
entry_k_street = Entry(frame_klienci)
entry_k_city = Entry(frame_klienci)
combo_k_hurtownia = ttk.Combobox(frame_klienci, state="readonly") # rozwijana lista wyboru
Label(frame_klienci, text="Imię").pack() # etykieta tekstowa
entry_k_name.pack() # umieszczenie elementu w interfejsie
Label(frame_klienci, text="Nazwisko").pack()
entry_k_surname.pack()
Label(frame_klienci, text="Miasto").pack()
entry_k_city.pack()
Label(frame_klienci, text="Ulica (opcjonalnie)").pack()
entry_k_street.pack()
Label(frame_klienci, text="Hurtownia").pack()
combo_k_hurtownia.pack()

def add_klient():
    name = entry_k_name.get().strip()
    surname = entry_k_surname.get().strip()
    city = entry_k_city.get().strip()
    street = entry_k_street.get().strip()
    hurtownia_name = combo_k_hurtownia.get().strip() # tworzenie obiektu
    if not name or not surname or not city or not hurtownia_name:
        messagebox.showwarning("Błąd", "Uzupełnij dane klienta i wybierz hurtownię.") # wyświetlenie komunikatu
        return
    h = next(h for h in hurtownie if h.name == hurtownia_name) # tworzenie obiektu
    k = Klient(name, surname, city, h, street) # tworzenie obiektu
    klienci.append(k) # dodanie elementu do listy
    listbox_klienci.insert(END, f"{k.name} {k.surname}") # dodanie wpisu do listy
    for e in (entry_k_name, entry_k_surname, entry_k_city, entry_k_street): e.delete(0,END) # usunięcie elementu

Button(frame_klienci, text="Dodaj", command=add_klient).pack()
listbox_klienci = Listbox(frame_klienci) # lista elementów
listbox_klienci.pack() # umieszczenie elementu w interfejsie
Button(frame_klienci, text="Usuń", command=lambda: delete_selected(listbox_klienci, klienci)).pack() # przycisk