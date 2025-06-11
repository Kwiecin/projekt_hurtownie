from tkinter import *
import tkintermapview

users : list= []


class Wholesaler:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup

        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        print(latitude)
        print(longitude)
        return [latitude, longitude]

def add_wholesaler():
    zmienna_nazwa = entry_name.get()
    zmienna_lokalizacja = entry_location.get()

users.append(Wholesaler(name=zmienna_nazwa, surname=zmienna_lokalizacja))
    print(users)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()
    show_users()

root = Tk()
root.geometry("1200x800")
root.title("Lista hurtowni")

ramka_lista_hurtowni=Frame(root)
ramka_lista_pracownikow=Frame(root)

ramka_lista_hurtowni.grid(row=0, column=0)
ramka_lista_pracownikow.grid(row=0, column=1)

#ramka hurtowni

label_lista_hurtowni= Label(ramka_lista_hurtowni, text="Lista obiektów")
label_lista_hurtowni.grid(row=0, column=0, columnspan=2)
listbox_lista_hurtowni = Listbox(ramka_lista_hurtowni, width=60, height=15)
listbox_lista_hurtowni.grid(row=1, column=0, columnspan=3)
button_szczegoly = Button(ramka_lista_hurtowni, text="Pokaż szczegóły", command=show_user_details)
button_szczegoly.grid(row=2, column=0)
button_usun = Button(ramka_lista_hurtowni, text="Usuń hurtownie", command=remove_user)
button_usun.grid(row=2, column=1)
button_edytuj_hurtownie = Button(ramka_lista_hurtowni, text="Edytuj hurtownie", command=edit_user)
button_edytuj_hurtownie.grid(row=2, column=2)

#ramka pracownikow
label_lista_pracownikow= Label(ramka_lista_pracownikow, text="Lista pracowników")
label_lista_pracownikow.grid(row=0, column=0, columnspan=2)
listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=60, height=15)
listbox_lista_pracownikow.grid(row=1, column=0, columnspan=3)
button_szczegoly_pracownika = Button(ramka_lista_pracownikow, text="Pokaż szczegóły pracownika", command=show_user_details)
button_szczegoly_pracownika.grid(row=2, column=0)
button_usun_pracownika = Button(ramka_lista_pracownikow, text="Usuń pracownika", command=remove_user)
button_usun_pracownika.grid(row=2, column=1)
button_edytuj_pracownika = Button(ramka_lista_pracownikow, text="Edytuj informacje o pracowniku ", command=edit_user)
button_edytuj_pracownika.grid(row=2, column=2)
