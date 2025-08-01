from model.models import SQLconnect, select, Kupujacy, Kategoria, Sklep, Firma, Zamowienie, Artykul_Lista, artykuly_relacja
from view.view import View

import os

from tkinterdnd2 import DND_FILES, TkinterDnD

import threading
import json
import datetime as datetime

class Controller:
    def __init__(self):
        self.dsc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.master = TkinterDnD.Tk()
        self.session = SQLconnect()

        self.view    = View(self.master, dsc=self.dsc)

        if os.path.exists(self.dsc + "/resources/setting.json") == False:
            self.json_setting(status = "start")
            print("Setting file created.")
        
        self.konfiguracja_programu = self.json_setting(status="read")
        self.leksykon_programu = self.json_language(self.konfiguracja_programu["language"])

    def run(self):
        self.view.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.view.master.mainloop()

    def on_closing(self):
        if View.messagebox(self, type="close"):
            self.session.close()
            self.view.master.destroy()

    def json_language(self, language_code):
        try:
            with open(os.path.join(self.dsc, "resources", "language", f"{language_code}.json"), 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Language file '{language_code}.json' not found.")
            View.messagebox("language", language_code)
            return {}

    def json_setting(self, status = "read", key = None, value = None):
        if status == "start":
            config = {
                "volume": 0.1, 
                "language": "pl_PL",
                "start_sound": "start_sound.wav",
                "click_sound": "click_sound.wav",
                "error_sound": "error_sound.wav"
            }

            with open(os.path.join(self.dsc, "resources", "setting.json"), 'w', encoding='utf-8') as settings:
                json.dump(config, settings, ensure_ascii=False, indent=4)  

        elif status == "read":
            with open(os.path.join(self.dsc, "resources", "setting.json"), 'r', encoding='utf-8') as settings:
                config = json.load(settings)
                return config

        elif status == "edit":
            config = self.json_setting(status="read")
            config[key] = value


    def button_dodaj_sklep(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_sklep", self.stworz_sklep, icon=View.add_sklep_icon)

    def button_zmiana_nazwa_sklep(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zmiana_nazwa_sklep", self.zmien_nazwa_sklep, icon=View.edit_sklep_icon)

    def button_usun_sklep(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_sklep", self.usun_sklep, icon=View.delete_sklep_icon)

    def button_dodaj_firma(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_firma", self.stworz_firma, icon=View.add_firma_icon)

    def button_zmiana_nazwa_firma(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zmiana_nazwa_firma", self.zmien_nazwa_firma, icon=View.edit_firma_icon)

    def button_usun_firma(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_firma", self.usun_firma, icon=View.delete_firma_icon)

    def button_dodaj_kategoria(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_kategoria", self.stworz_kategoria, icon=View.add_kategoria_icon)

    def button_zmiana_nazwa_kategoria(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zmiana_nazwa_kategoria", self.zmien_nazwa_kategoria, icon=View.edit_kategoria_icon)

    def button_usun_kategorie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_kategorie", self.usun_kategorie, icon=View.delete_kategoria_icon)

    def button_dodaj_kupujacy(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_kupujacy", self.stworz_kupujacy, icon=View.add_kupujacy_icon)

    def button_zmiana_nazwa_kupujacy(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zmiana_nazwa_kupujacy", self.zmien_nazwa_kupujacy, icon=View.edit_kupujacy_icon)

    def button_usun_kupujacy(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_kupujacy", self.usun_kupujacego, icon=View.delete_kupujacy_icon)

    def button_dodaj_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_zamowienie", self.dodaj_modyfikuj_zamowienie, icon=View.add_zamowienie_icon)

    def button_modyfikuj_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_modyfikuj_zamowienie", lambda: self.dodaj_modyfikuj_zamowienie(commend="modyfikuj"), icon=View.edit_zamowienie_icon)

    def button_usun_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_zamowienie", self.usun_zamowienie, side='bottom', pady=(3,30), icon=View.delete_zamowienie_icon)

    def button_lista_artykulow(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_lista_artykulow", self.list_artykulow, pady=(30,30), icon=View.lista_artykulow_icon)

    def button_lista_sklepow(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_lista_sklepow", self.list_sklepy, icon=View.lista_sklepy_icon)

    def button_lista_firm(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_lista_firm", self.list_firmy, icon=View.lista_firmy_icon)

    def button_lista_kupujacych(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_lista_kupujacych", self.list_kupujacy, icon=View.lista_kupujacy_icon)

    def button_lista_kategorii(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_lista_kategorii", self.list_kategorie, icon=View.lista_kategorie_icon)

    def button_refresh_zamowienia(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_refresh_zamowienia", self.load_zamowienia_daemon, side='bottom', icon=View.refresh_icon)

    def button_stworz_artykul(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_stworz_artykul", self.stworz_modyfikuj_artykul, icon=View.add_artykul_icon)

    def button_modyfikuj_artykul(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_modyfikuj_artykul", lambda: self.stworz_modyfikuj_artykul(commend="modyfikuj"), icon=View.edit_artykul_icon)

    def button_zatwierdz_artykul(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zatwierdz_artykul", self.zatwierdz_nowy_modyfikuj_artykul, pady=(3,30), icon=View.add_artykul_icon)

    def button_zatwierdz_edycje_artykul(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zatwierdz_edycje_artykul", lambda: self.zatwierdz_nowy_modyfikuj_artykul(commend="modyfikuj"), pady=(3,30), icon=View.edit_artykul_icon)

    def button_zniszcz_artykul(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zniszcz_artykul", self.zniszcz_artykul, icon=View.delete_artykul_icon)

    def button_dodaj_artykul_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_dodaj_artykul_zamowienie", self.dodaj_list_artykulow, icon=View.add_artykul_zamowienie_icon)

    def button_zatwierdz_dodanie_artykulu(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zatwierdz_dodanie_artykulu", self.cena_ilosc_dodanie, icon=View.add_artykul_zamowienie_icon)

    def button_anuluj_dodanie_artykulu(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_anuluj_dodanie_artykulu", self.window.destroy, icon=View.backButton_icon)

    def button_usun_artykul_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_usun_artykul_zamowienie", self.usun_artykul_zamowienie, icon=View.delete_artykul_zamowienie_icon)

    def button_zatwierdz_edycje_zamowienie(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_zatwierdz_edycje_zamowienie", lambda: self.zatwierdz_nowy_modyfikuj_zamowienie(commend="modyfikuj"), pady=(3,30), icon=View.edit_zamowienie_icon)

    def button_ustawienia(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "button_ustawienia", self.ustawienia_programu, pady=5, side='bottom', icon=View.setting_icon)

    def buttons_zatwierdz_zamowienia(self, frame):
        self.dodaj_button = View.utworz_przycisk(frame, "buttons_zatwierdz_zamowienia", self.zatwierdz_nowy_modyfikuj_zamowienie, pady=(3,30), icon=View.add_zamowienie_icon)