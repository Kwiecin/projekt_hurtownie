from tkinter import *
import tkintermapview

users: list = []


# hurtownie
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


root = Tk()
root.geometry("1200x800")
root.title("Lista hurtowni")