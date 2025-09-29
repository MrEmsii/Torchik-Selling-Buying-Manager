from model.stock_db_model import SQLconnect, select, Kupujacy, Kategoria, Sklep, Firma, Zamowienie, Artykul_Lista, artykuly_relacja
from view.ViewStock import ViewStock

import string

from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk

import threading
import datetime as datetime

class ControllerStock():
    def __init__(
            self, master, dsc, leksykon_programu, leksykon_messagebox, konfiguracja_programu, 
            sound = None, 
            messagebox_controller = None, 
            currency = None, 
            language_code = None, 
            main_controller=None
            ):
        
        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.leksykon_messagebox = leksykon_messagebox
        self.konfiguracja_programu = konfiguracja_programu
        self.currency = currency
        self.main_controller = main_controller
        self.sound = sound

        self.stock_master = tk.Toplevel(master)
        self.db_session = SQLconnect()

        self.view = ViewStock(
            self.stock_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            currency=self.currency,
            konfiguracja_programu=konfiguracja_programu, 
            language_code=language_code,
            sound=self.sound
            )

        self.messagebox_controller = messagebox_controller 
        self.inicjalizacja_frame()
        self.list_zamowienia()

        self.stock_master.protocol("WM_DELETE_WINDOW", self.on_closing_order_window)

    def run(self):
        self.stock_master.deiconify()

    def close(self):
        if self.db_session:
            self.db_session.close()
            self.db_session = None

    def on_closing_order_window(self):
        if self.messagebox_controller.close_info():
            self.close()
            if self.stock_master.winfo_exists():
                self.stock_master.destroy()
            if self.main_controller:
                self.main_controller.close_stock_window()

    def load_zamowienia_daemon(self, widok = "pokaz"):
        print("load_zamowienia_daemon")
        commend = self.load_zamowienia(widok = widok)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_sklepy_daemon(self, widok = "pokaz", select_item = None):
        print("load_sklepy_daemon")
        commend = self.load_sklepy(widok = widok, select_item=select_item)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_kupujacy_daemon(self, widok = "pokaz", select_item = None):
        print("load_kupujacy_daemon")
        commend = self.load_kupujacy(widok = widok, select_item=select_item)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_kategorie_daemon(self, widok = "pokaz", select_item = None):
        print("load_kategorie_daemon")
        commend = self.load_kategorie(widok = widok, select_item=select_item)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_firmy_deaemon(self, widok = "pokaz", select_item = None):
        print("load_firmy_deaemon")
        commend = self.load_firmy(widok = widok, select_item=select_item)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_artykuly_deaemon(self, widok = "pokaz"):
        print("load_artykuly_deaemon")
        commend = self.load_artykuly(widok = widok)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_sklepy(self, widok, select_item):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            sklepy = self.db_session.query(Sklep).all()
            sklepy_data = []

            for sklep in sklepy:
                sklep_id = sklep.id
                sklep_nazwa = sklep.nazwa
                sklepy_data.append((sklep_id, sklep_nazwa))

            sklepy_data.sort(key=lambda x: x[1].lower())

            def update_gui():
                self.sklepy_tree.delete(*self.sklepy_tree.get_children())
                for sklep_id, sklep_nazwa in sklepy_data:
                    self.sklepy_tree.insert('', 'end', values=(sklep_id, sklep_nazwa))
                self.zaznacz_wiersz_z_wartoscia(self.sklepy_tree, 'id', select_item)
                if widok == "pokaz": self.hide_message_async()
            
            self.stock_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def load_artykuly(self, widok = None, kategoria_id = None):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            if not kategoria_id:
                artykuly = self.db_session.query(Artykul_Lista).all()
            else:
                artykuly = self.db_session.query(Artykul_Lista).filter_by(kategoria_id=kategoria_id).all()
            
            artykuly_data = []

            for art in artykuly:
                art_id = art.id
                art_kategoria = art.kategoria.nazwa if art.kategoria else  " "
                art_firma = art.firma.nazwa if art.firma else  " "
                art_nazwa = art.nazwa
                art_kolor = art.kolor if art.kolor else  " "
                art_szczegoly = art.szczegoly if art.szczegoly else  " "
                artykuly_data.append((art_id, art_kategoria, art_firma, art_nazwa, art_kolor, art_szczegoly))

            artykuly_data.sort(key=lambda x:x[3])

            def update_gui():
                self.artykuly_tree.delete(*self.artykuly_tree.get_children())
                for id, kategoria, firma, nazwa, kolor, szczegoly in artykuly_data:
                    self.artykuly_tree.insert('', 'end', values=(id, kategoria, firma, nazwa, kolor, szczegoly))
                
                if widok == "pokaz": self.hide_message_async()
            self.stock_master.after(0, update_gui)
        threading.Thread(target=task, daemon=True).start()

    def load_kupujacy(self, widok, select_item):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            kupujacy = self.db_session.query(Kupujacy).all()
            kupujacy_data = []

            for kup in kupujacy:
                kup_id = kup.id
                kup_nazwa = kup.nazwa
                kupujacy_data.append((kup_id, kup_nazwa))

            kupujacy_data.sort(key=lambda x:x[1])

            def update_gui():
                self.kupujacy_tree.delete(*self.kupujacy_tree.get_children())
                for kup_id, kup_nazwa in kupujacy_data:
                    self.kupujacy_tree.insert('', 'end', values=(kup_id, kup_nazwa))
                
                self.zaznacz_wiersz_z_wartoscia(self.kupujacy_tree, 'id', select_item)
                if widok == "pokaz": self.hide_message_async()

            self.stock_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def load_kategorie(self, widok = None, select_item = None):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            kategorie = self.db_session.query(Kategoria).all()
            kategorie_data = []

            for kategoria in kategorie:
                kategoria_id = kategoria.id
                kategoria_name = kategoria.nazwa
                kategorie_data.append((kategoria_id, kategoria_name))

            kategorie_data.sort(key=lambda x:x[1])

            def update_gui():
                self.kategorie_tree.delete(*self.kategorie_tree.get_children())
                for kategoria_id, kategoria_name in kategorie_data:
                    self.kategorie_tree.insert('', 'end', values=(kategoria_id, kategoria_name))    
                self.zaznacz_wiersz_z_wartoscia(self.kategorie_tree, 'id', select_item)
                if widok == "pokaz": self.hide_message_async()

            self.stock_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def load_firmy(self, widok, select_item):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            firmy = self.db_session.query(Firma).all()
            firmy_data = []

            for firma in firmy:
                firma_id = firma.id
                firma_name = firma.nazwa
                firmy_data.append((firma_id, firma_name))

            firmy_data.sort(key=lambda x:x[1])

            def update_gui():
                self.firma_tree.delete(*self.firma_tree.get_children())
                for firma_id, firma_name in firmy_data:
                    self.firma_tree.insert('', 'end', values=(firma_id, firma_name))  
                self.zaznacz_wiersz_z_wartoscia(self.firma_tree, 'id', select_item)
                if widok == "pokaz": self.hide_message_async()

            self.stock_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def load_zamowienia(self, widok):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            zamowienia = self.db_session.query(Zamowienie).all()
            zamowienia_data = []

            for zamow in zamowienia:
                zamow_id = zamow.id
                zamow_data = zamow.data
                faktura_id = zamow.faktura_id
                zamow_kupujacy = zamow.kupujacy.nazwa if zamow.kupujacy else " "
                zamow_sklep = zamow.sklep.nazwa if zamow.sklep else " "
                rabat_j = f"{zamow.rabat_j:.2f} {self.currency}"
                rabat_proc = f"{zamow.rabat_procent :.0f} %"
                zamow_cena = f"{zamow.oblicz_cene(self.db_session):,.2f} {self.currency}".replace(",", " ")
                zamow_cena_rabat = f"{zamow.oblicz_cene_rabat(self.db_session):,.2f} {self.currency}".replace(",", " ")
                zamowienia_data.append((zamow_id, zamow_data, faktura_id, zamow_kupujacy, zamow_sklep, rabat_j, rabat_proc, zamow_cena, zamow_cena_rabat))

            zamowienia_data.sort(key=lambda x: x[0], reverse=True)
            zamowienia_data.sort(key=lambda x: x[1], reverse=True)

            def update_gui():
                self.zamowienia_tree.delete(*self.zamowienia_tree.get_children())
                for z_id, data, faktura_id, kupujacy, sklep, rabat_1, rabat_2, cena, cena_rabat in zamowienia_data:
                    self.zamowienia_tree.insert('', 'end', values=(z_id, data, faktura_id, kupujacy, sklep, rabat_1, rabat_2, cena, cena_rabat))
                if widok == "pokaz": self.hide_message_async()

            self.stock_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def button_manager(self, frame, back_target = 'main', startup = False):
        if startup == False:
            for widget in self.stock_frame.winfo_children():
                widget.destroy()

            for widget in self.button_stock_frame.winfo_children():
                widget.destroy()
        
        if frame == "main":
            self.button_dodaj_zamowienie(self.button_stock_frame)
            self.button_modyfikuj_zamowienie(self.button_stock_frame)
            self.button_lista_artykulow(self.button_stock_frame)
            self.button_lista_sklepow(self.button_stock_frame)
            self.button_lista_kupujacych(self.button_stock_frame)
            self.button_lista_kategorii(self.button_stock_frame)
            self.button_lista_firm(self.button_stock_frame)
            self.button_refresh_zamowienia(self.button_stock_frame)  
            self.button_usun_zamowienie(self.button_stock_frame)

        elif frame == "lista dodanych do zamowienia":
            self.button_dodaj_artykul_zamowienie(self.button_stock_frame)
            self.button_edytuj_artykul_zamowienie(self.button_stock_frame)
            self.button_usun_artykul_zamowienie(self.button_stock_frame)

        elif frame == "kupujacy":
            self.button_dodaj_kupujacy(self.button_stock_frame)
            self.button_zmiana_nazwa_kupujacy(self.button_stock_frame)
            self.button_usun_kupujacy(self.button_stock_frame)

        elif frame == "sklepy":
            self.button_dodaj_sklep(self.button_stock_frame) 
            self.button_zmiana_nazwa_sklep(self.button_stock_frame)
            self.button_usun_sklep(self.button_stock_frame)

        elif frame == "firmy":
            self.button_dodaj_firma(self.button_stock_frame) 
            self.button_zmiana_nazwa_firma(self.button_stock_frame)
            self.button_usun_firma(self.button_stock_frame)

        elif frame == "lista_artykuly":
            self.button_stworz_artykul(self.button_stock_frame) 
            self.button_modyfikuj_artykul(self.button_stock_frame) 
            self.button_zniszcz_artykul(self.button_stock_frame)

        elif frame == "dodaj_zamowienie":
            self.buttons_zatwierdz_zamowienia(self.button_stock_frame) 
            self.button_dodaj_kupujacy(self.button_stock_frame)
            self.button_dodaj_sklep(self.button_stock_frame) 

        elif frame == "modyfikuj_zamowienie":
            self.button_zatwierdz_edycje_zamowienie(self.button_stock_frame) 
            self.button_dodaj_kupujacy(self.button_stock_frame)
            self.button_dodaj_sklep(self.button_stock_frame) 

        elif frame == "kategorie":
            self.button_dodaj_kategoria(self.button_stock_frame) 
            self.button_zmiana_nazwa_kategoria(self.button_stock_frame)
            self.button_usun_kategorie(self.button_stock_frame)

        elif frame == 'tworzenie_artykuly':
            self.button_zatwierdz_artykul(self.button_stock_frame)
            self.button_dodaj_firma(self.button_stock_frame)
            self.button_dodaj_kategoria(self.button_stock_frame) 

        elif frame == 'modyfikacja_artykuly':
            self.button_zatwierdz_edycje_artykul(self.button_stock_frame)
            self.button_dodaj_firma(self.button_stock_frame)
            self.button_dodaj_kategoria(self.button_stock_frame) 

        elif frame == "wyjdź_z_cena_ilosc_dodawanie":
            self.button_zatwierdz_dodanie_artykulu(self.view.button_cena_ilosc_frame)
            self.button_anuluj_dodanie_artykulu(self.view.button_cena_ilosc_frame)

        elif frame == "wyjdź_z_cena_ilosc_edycja":
            self.button_zatwierdz_edycje_artykulu(self.view.button_cena_ilosc_frame)
            self.button_anuluj_dodanie_artykulu(self.view.button_cena_ilosc_frame)

        if frame != 'main':
            self.button_back_pack(self.button_stock_frame, back_target)
        
        ViewStock.start_grid_setting(self)

    def inicjalizacja_frame(self):
        self.stock_frame = self.view.stock_frame
        self.button_stock_frame = self.view.button_stock_frame
        self.zamowienia_frame = self.view.zamowienia_frame
        self.zamowienie_id = None


    # --- ARTYKUŁY ---
    def button_stworz_artykul(self, frame):
        leksykon = self.leksykon_programu["button_stworz_artykul"]
        self.view.utworz_przycisk(frame, self.dodaj_modyfikuj_artykul, icon=self.view.add_artykul_icon, leksykon_programu=leksykon)

    def button_modyfikuj_artykul(self, frame):
        leksykon = self.leksykon_programu["button_modyfikuj_artykul"]
        self.view.utworz_przycisk(frame, lambda: self.dodaj_modyfikuj_artykul(commend="modyfikuj"), icon=self.view.edit_artykul_icon, leksykon_programu=leksykon)

    def button_zatwierdz_artykul(self, frame):
        leksykon = self.leksykon_programu["button_zatwierdz_artykul"]
        self.view.utworz_przycisk(frame, self.zatwierdz_nowy_modyfikuj_artykul, pady=(3,30), icon=self.view.add_artykul_icon, leksykon_programu=leksykon)

    def button_zatwierdz_edycje_artykul(self, frame):
        leksykon = self.leksykon_programu["button_zatwierdz_edycje_artykul"]
        self.view.utworz_przycisk(frame, lambda: self.zatwierdz_nowy_modyfikuj_artykul(commend="modyfikuj"), pady=(3,30), icon=self.view.edit_artykul_icon, leksykon_programu=leksykon)

    def button_zniszcz_artykul(self, frame):
        leksykon = self.leksykon_programu["button_zniszcz_artykul"]
        self.view.utworz_przycisk(frame, self.zniszcz_artykul, icon=self.view.delete_artykul_icon, leksykon_programu=leksykon)

    def button_dodaj_artykul_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_artykul_zamowienie"]
        self.view.utworz_przycisk(frame, self.dodaj_list_artykulow, icon=self.view.add_artykul_zamowienie_icon, leksykon_programu=leksykon)

    def button_edytuj_artykul_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_modyfikuj_artykul_zamowienie"]
        self.view.utworz_przycisk(frame, self.edytuj_artykul_zamowienie, icon=self.view.edit_artykul_zamowienie_icon, leksykon_programu=leksykon)

    def button_usun_artykul_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_usun_artykul_zamowienie"]
        self.view.utworz_przycisk(frame, self.usun_artykul_zamowienie, icon=self.view.delete_artykul_zamowienie_icon, leksykon_programu=leksykon)

    def button_zatwierdz_dodanie_artykulu(self, frame):
        leksykon = self.leksykon_programu["button_zatwierdz_dodanie_artykulu"]
        self.view.utworz_przycisk(frame, self.cena_ilosc_dodanie, icon=self.view.add_artykul_zamowienie_icon, leksykon_programu=leksykon)

    def button_zatwierdz_edycje_artykulu(self, frame):
        leksykon = self.leksykon_programu["button_modyfikuj_artykul_zamowienie"]
        self.view.utworz_przycisk(frame, self.cena_ilosc_edycja, icon=self.view.add_artykul_zamowienie_icon, leksykon_programu=leksykon)

    def button_anuluj_dodanie_artykulu(self, frame):
        leksykon = self.leksykon_programu["button_anuluj_dodanie_artykulu"]
        self.view.utworz_przycisk(frame, self.anuluj_dodanie_artykulu_zamowienie, icon=self.view.backButton_icon, leksykon_programu=leksykon)

    # --- ZAMÓWIENIA ---
    def button_dodaj_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, self.dodaj_modyfikuj_zamowienie, icon=self.view.add_zamowienie_icon, leksykon_programu=leksykon)

    def button_modyfikuj_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_modyfikuj_zamowienie"]
        self.view.utworz_przycisk(frame, lambda: self.dodaj_modyfikuj_zamowienie(commend="modyfikuj"), icon=self.view.edit_zamowienie_icon, leksykon_programu=leksykon)

    def button_zatwierdz_edycje_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_zatwierdz_edycje_zamowienie"]
        self.view.utworz_przycisk(frame, lambda: self.zatwierdz_nowy_modyfikuj_zamowienie(commend="modyfikuj"), pady=(3,30), icon=self.view.edit_zamowienie_icon, leksykon_programu=leksykon)

    def buttons_zatwierdz_zamowienia(self, frame):
        leksykon = self.leksykon_programu["buttons_zatwierdz_zamowienia"]
        self.view.utworz_przycisk(frame, self.zatwierdz_nowy_modyfikuj_zamowienie, pady=(3,30), icon=self.view.add_zamowienie_icon, leksykon_programu=leksykon)

    def button_usun_zamowienie(self, frame):
        leksykon = self.leksykon_programu["button_usun_zamowienie"]
        self.view.utworz_przycisk(frame, self.usun_zamowienie, side='bottom', pady=(3,30), icon=self.view.delete_zamowienie_icon, leksykon_programu=leksykon)

    # --- SKLEPY ---
    def button_dodaj_sklep(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_sklep"]
        self.view.utworz_przycisk(frame, self.stworz_sklep, icon=self.view.add_sklep_icon, leksykon_programu=leksykon)

    def button_zmiana_nazwa_sklep(self, frame):
        leksykon = self.leksykon_programu["button_zmiana_nazwa_sklep"]
        self.view.utworz_przycisk(frame, self.zmien_nazwa_sklep, icon=self.view.edit_sklep_icon, leksykon_programu=leksykon)

    def button_usun_sklep(self, frame):
        leksykon = self.leksykon_programu["button_usun_sklep"]
        self.view.utworz_przycisk(frame, self.usun_sklep, icon=self.view.delete_sklep_icon, leksykon_programu=leksykon)

    # --- FIRMY ---
    def button_dodaj_firma(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_firma"]
        self.view.utworz_przycisk(frame, self.stworz_firma, icon=self.view.add_firma_icon, leksykon_programu=leksykon)

    def button_zmiana_nazwa_firma(self, frame):
        leksykon = self.leksykon_programu["button_zmiana_nazwa_firma"]
        self.view.utworz_przycisk(frame, self.zmien_nazwa_firma, icon=self.view.edit_firma_icon, leksykon_programu=leksykon)

    def button_usun_firma(self, frame):
        leksykon = self.leksykon_programu["button_usun_firma"]
        self.view.utworz_przycisk(frame, self.usun_firma, icon=self.view.delete_firma_icon, leksykon_programu=leksykon)

    # --- KATEGORIE ---
    def button_dodaj_kategoria(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_kategoria"]
        self.view.utworz_przycisk(frame, self.stworz_kategoria, icon=self.view.add_kategoria_icon, leksykon_programu=leksykon)

    def button_zmiana_nazwa_kategoria(self, frame):
        leksykon = self.leksykon_programu["button_zmiana_nazwa_kategoria"]
        self.view.utworz_przycisk(frame, self.zmien_nazwa_kategoria, icon=self.view.edit_kategoria_icon, leksykon_programu=leksykon)

    def button_usun_kategorie(self, frame):
        leksykon = self.leksykon_programu["button_usun_kategorie"]
        self.view.utworz_przycisk(frame, self.usun_kategorie, icon=self.view.delete_kategoria_icon, leksykon_programu=leksykon)

    # --- KUPUJĄCY ---
    def button_dodaj_kupujacy(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_kupujacy"]
        self.view.utworz_przycisk(frame, self.stworz_kupujacy, icon=self.view.add_kupujacy_icon, leksykon_programu=leksykon)

    def button_zmiana_nazwa_kupujacy(self, frame):
        leksykon = self.leksykon_programu["button_zmiana_nazwa_kupujacy"]
        self.view.utworz_przycisk(frame, self.zmien_nazwa_kupujacy, icon=self.view.edit_kupujacy_icon, leksykon_programu=leksykon)

    def button_usun_kupujacy(self, frame):
        leksykon = self.leksykon_programu["button_usun_kupujacy"]
        self.view.utworz_przycisk(frame, self.usun_kupujacego, icon=self.view.delete_kupujacy_icon, leksykon_programu=leksykon)

    # --- LISTY / INNE ---
    def button_lista_artykulow(self, frame):
        leksykon = self.leksykon_programu["button_lista_artykulow"]
        self.view.utworz_przycisk(frame, self.list_artykuly, pady=(30,30), icon=self.view.lista_artykulow_icon, leksykon_programu=leksykon)

    def button_lista_sklepow(self, frame):
        leksykon = self.leksykon_programu["button_lista_sklepow"]
        self.view.utworz_przycisk(frame, self.list_sklepy, icon=self.view.lista_sklepy_icon, leksykon_programu=leksykon)

    def button_lista_firm(self, frame):
        leksykon = self.leksykon_programu["button_lista_firm"]
        self.view.utworz_przycisk(frame, self.list_firmy, icon=self.view.lista_firmy_icon, leksykon_programu=leksykon)

    def button_lista_kupujacych(self, frame):
        leksykon = self.leksykon_programu["button_lista_kupujacych"]
        self.view.utworz_przycisk(frame, self.list_kupujacy, icon=self.view.lista_kupujacy_icon, leksykon_programu=leksykon)

    def button_lista_kategorii(self, frame):
        leksykon = self.leksykon_programu["button_lista_kategorii"]
        self.view.utworz_przycisk(frame, self.list_kategorie, icon=self.view.lista_kategorie_icon, leksykon_programu=leksykon)

    def button_refresh_zamowienia(self, frame):
        leksykon = self.leksykon_programu["button_refresh_zamowienia"]
        self.view.utworz_przycisk(frame, self.load_zamowienia_daemon, side='bottom', icon=self.view.refresh_icon, leksykon_programu=leksykon)

    def button_back_pack(self, frame, commend = "main"):
        if commend == "main":
            commend = self.pokaz_stock_frame
        elif commend == "lista_artykułów":
            commend = self.powrot_do_lista_artykulow
        elif commend == "zamówienie":
            commend = lambda: self.load_inside_zamowienie(self.zamowienie_id)

        leksykon = self.leksykon_programu["button_back_pack"]    
        self.view.utworz_przycisk(frame, commend, side='bottom', padx=5, pady=5, leksykon_programu=leksykon, icon=self.view.backButton_icon)

    def zaznacz_wiersz_z_wartoscia(self, treeview, kolumna, wartosc):
        for item in treeview.get_children():
            if treeview.set(item, kolumna) == str(wartosc):
                treeview.selection_set(item)
                treeview.focus(item)
                treeview.see(item)
                break

    def list_artykuly(self, backTarget = 'main'):
        self.zamowienia_frame.grid_remove()
        self.view.artykuly_lista_view()
        self.button_manager("lista_artykuly", back_target=backTarget)

        self.view.artukuly_list_grid_setting()

        name = self.leksykon_programu["names_list"]

        self.artykuly_tree = self.view.artykuly_tree(parent_frame = self.view.secend_frame, label_text = name["select_art"])
        self.kategorie_tree = self.view.name_tree(self.view.stock_frame, name["category"], True)
        
        self.load_artykuly_deaemon()
        self.load_kategorie_daemon("ukryj")

        self.kategorie_tree.bind("<Double-1>", self.on_double_click_filtrowanie_kategoria)
        self.kategorie_tree.bind("<Double-3>", self.on_double_click_filtrowanie_kategoria_resetowanie)

        if self.zamowienie_id:
            self.artykuly_tree.bind("<Double-1>", self.on_double_click_dodawanie_artykulu_do_zamowienia)

    def list_zamowienia(self):
        self.view.zamowienia_grid_setting()
        self.button_manager(frame="main", startup = True)
        name = self.leksykon_programu["names_list"]["order"]
        self.zamowienia_tree = self.view.zamowienie_tree(parent_frame=self.zamowienia_frame, label_text=name) 
        self.zamowienia_tree.bind("<Double-1>", self.on_double_click_otwieranie_zamowienia)
        self.load_zamowienia_daemon()

    def list_kupujacy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager("kupujacy")
        name = self.leksykon_programu["names_list"]["buyer"]
        self.kupujacy_tree = self.view.name_tree(self.stock_frame, name, True)
        self.load_kupujacy_daemon()

    def list_firmy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager(frame="firmy")
        name = self.leksykon_programu["names_list"]["company"]
        self.firma_tree = self.view.name_tree(self.stock_frame, name, True)
        self.load_firmy_deaemon()

    def list_sklepy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager("sklepy")
        name = self.leksykon_programu["names_list"]["shop"]
        self.sklepy_tree = self.view.name_tree(self.stock_frame, name, True)
        self.load_sklepy_daemon()

    def list_kategorie(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager(frame="kategorie")
        name = self.leksykon_programu["names_list"]["category"]
        self.kategorie_tree = self.view.name_tree(self.stock_frame, name, True)
        self.load_kategorie_daemon()

    def stworz_sklep(self, value=None):
        leksykon = self.leksykon_messagebox["add_messagebox"]
        name = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["shop"]+"\t\t\t\t", value=value)
        if name == "" or self.specjalne_znaki(name) :
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.stworz_sklep(value=name)

        elif name is not None:
            obiekt = Sklep(nazwa=name)
            self.db_session.add(obiekt)
            self.db_session.commit()
            self.load_sklepy_daemon(widok="pokaz")    

            self.sound.play_confirm_sound()

    def stworz_kupujacy(self, value=None):
        leksykon = self.leksykon_messagebox["add_messagebox"]
        name = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["buyer"]+"\t\t\t\t", value=value)
        if name == "" or self.specjalne_znaki(name) :
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.stworz_kupujacy(value=name)

        elif name is not None:
            obiekt = Kupujacy(nazwa=name)
            self.db_session.add(obiekt)
            self.db_session.commit()
            self.load_kupujacy_daemon(widok="pokaz")  

            self.sound.play_confirm_sound()

    def stworz_kategoria(self, value=None):
        leksykon = self.leksykon_messagebox["add_messagebox"]
        name = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["category"]+"\t\t\t\t", value=value)
        if name == "" or self.specjalne_znaki(name):
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.stworz_kategoria(value=name)

        elif name is not None:
            obiekt = Kategoria(nazwa=name)
            self.db_session.add(obiekt)
            self.db_session.commit()
            self.load_kategorie_daemon(widok="pokaz")    

            self.sound.play_confirm_sound()

    def stworz_firma(self, value=None):
        leksykon = self.leksykon_messagebox["add_messagebox"]
        name = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["company"]+"\t\t\t\t", value=value)
        if name == "" or self.specjalne_znaki(name) :
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.stworz_firma(value=name)

        elif name is not None:
            obiekt = Firma(nazwa=name)
            self.db_session.add(obiekt)
            self.db_session.commit()
            self.load_firmy_deaemon(widok="pokaz") 

            self.sound.play_confirm_sound()

    def zmien_nazwa_kupujacy(self):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            return

        element_value = self.kupujacy_tree.item(selected_item[0], 'values')
        kupujacy_id = element_value[0]
        stara_nazwa = element_value[1]

        leksykon = self.leksykon_messagebox["edit_messagebox"]
        new_value = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["buyer"]+"\t\t\t\t", value=stara_nazwa)

        if new_value and new_value.strip() and not self.specjalne_znaki(new_value):
            kupujacy = self.db_session.query(Kupujacy).filter_by(id=kupujacy_id).first()

            if kupujacy:
                kupujacy.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_kupujacy_daemon(widok="ukryj")

                self.sound.play_confirm_sound()

        elif self.specjalne_znaki(new_value):
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.zmien_nazwa_kupujacy()

    def zmien_nazwa_sklep(self):
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            return

        element_value = self.sklepy_tree.item(selected_item[0], 'values')
        sklep_id = element_value[0]
        stara_nazwa = element_value[1]

        leksykon = self.leksykon_messagebox["edit_messagebox"]
        new_value = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["shop"]+"\t\t\t\t", value=stara_nazwa)

        if new_value and new_value.strip() and not self.specjalne_znaki(new_value):
            sklep = self.db_session.query(Sklep).filter_by(id=sklep_id).first()

            if sklep:
                sklep.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon(widok = "ukryj")
                self.load_sklepy(widok = "ukryj", select_item=sklep_id)
    
                self.sound.play_confirm_sound()

        elif self.specjalne_znaki(new_value):
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.zmien_nazwa_sklep()

    def zmien_nazwa_firma(self):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            return

        element_value = self.firma_tree.item(selected_item[0], 'values')
        firma_id = element_value[0]
        stara_nazwa = element_value[1]

        leksykon = self.leksykon_messagebox["edit_messagebox"]
        new_value = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["company"]+"\t\t\t\t", value=stara_nazwa)

        if new_value and new_value.strip():
            firma = self.db_session.query(Firma).filter_by(id=firma_id).first()

            if firma:
                firma.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_firmy_deaemon(widok = "ukryj") 

                self.sound.play_confirm_sound()

        elif self.specjalne_znaki(new_value):
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.zmien_nazwa_firma()

    def zmien_nazwa_kategoria(self):
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            return

        element_value = self.kategorie_tree.item(selected_item[0], 'values')
        kategoria_id = element_value[0]
        stara_nazwa = element_value[1]

        leksykon = self.leksykon_messagebox["edit_messagebox"]
        new_value = self.messagebox_controller.messagebox(type="ask", heading=leksykon["heading"], text=leksykon["text"]["category"]+"\t\t\t\t", value=stara_nazwa)

        if new_value and new_value.strip():
            kategoria = self.db_session.query(Kategoria).filter_by(id=kategoria_id).first()

            if kategoria:
                kategoria.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_kategorie_daemon(widok = "ukryj") 

                self.sound.play_confirm_sound()

        elif self.specjalne_znaki(new_value):
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            self.zmien_nazwa_kategoria()

    def usun_zamowienie(self):
        selected_item = self.zamowienia_tree.selection()
        if not selected_item:
            return

        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["order"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            
            self.db_session.query(Zamowienie).filter_by(id=zamowienie_id).delete(synchronize_session=False)
            self.db_session.commit()
            self.load_zamowienia_daemon()  

            self.sound.play_confirm_sound()

    def usun_artykul_zamowienie(self):
        selected_item = self.inside_tree.selection()
        if not selected_item:
            return
        
        relacja_name = self.inside_tree.item(self.inside_tree.selection()[0], 'values')

        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["order"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            self.db_session.execute(
                artykuly_relacja.delete()
                .where(artykuly_relacja.c.zamowienie_id == self.zamowienie_id,
                artykuly_relacja.c.artykul_id == relacja_name[0],
                artykuly_relacja.c.cena_jednostkowa == relacja_name[1].replace(" "+self.currency,"").replace(",","."),
                artykuly_relacja.c.ilosc_artykulu == relacja_name[2]
                )
            )
            self.db_session.commit()
            self.load_inside_zamowienie(self.zamowienie_id)

            self.sound.play_confirm_sound()

        self.load_zamowienia_daemon()

    def usun_kupujacego(self):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            return
        
        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox(
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["buyer"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            kupujacy_id = self.kupujacy_tree.item(self.kupujacy_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Kupujacy).filter_by(id=kupujacy_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_zamowienia_daemon()
            self.load_kupujacy_daemon(widok = "ukryj")  

            self.sound.play_confirm_sound()

    def usun_sklep(self):
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            return
        
        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["shop"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            sklep_id = self.sklepy_tree.item(self.sklepy_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Sklep).filter_by(id=sklep_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_sklepy_daemon(widok = "ukryj") 

            self.sound.play_confirm_sound()

    def usun_firma(self):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            return
        
        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["company"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            firma_id = self.firma_tree.item(self.firma_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Firma).filter_by(id=firma_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_firmy_deaemon(widok = "ukryj")    

            self.sound.play_confirm_sound()

    def usun_kategorie(self):
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            return
        
        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["category"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            kategoria_id = self.kategorie_tree.item(self.kategorie_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Kategoria).filter_by(id=kategoria_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_kategorie_daemon(widok = "ukryj") 

            self.sound.play_confirm_sound()

    def zniszcz_artykul(self):
        selected_item = self.artykuly_tree.selection()
        if not selected_item:
            return

        leksykon = self.leksykon_messagebox["delete_messagebox"]

        dialog = self.messagebox_controller.messagebox( 
                                 type="ask", 
                                 heading=leksykon["heading"], 
                                 text=leksykon["text"]["article"] + " lub ".join(leksykon["agree"]) + "\t\t\t\t")

        if dialog and dialog.lower() in [name.lower() for name in leksykon["agree"]]:
            artykul_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            self.db_session.query(Artykul_Lista).filter_by(id=artykul_id).delete(synchronize_session=False)
            self.db_session.commit()
            self.powrot_do_lista_artykulow()

            self.sound.play_confirm_sound()

    def dodaj_modyfikuj_artykul(self, commend = "stworz"):
        self.zamowienia_frame.grid_remove()

        if commend == "stworz":
            self.usun_all_widgets()

            self.button_manager("tworzenie_artykuly", back_target = 'lista_artykułów')
            self.view.dodaj_modyfikuj_artykul_view()
            firma_id_artykulu = None
            kategoria_id_artykulu = None

        elif commend == "modyfikuj":
            selected_item = self.artykuly_tree.selection()
            if not selected_item:
                leksykon = self.leksykon_messagebox["error_messagebox"]
                self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["select_art"])
                return
                    
            self.artykul_modyfikacja_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            info = self.wczytaj_informacje_artykul(self.artykul_modyfikacja_id)

            self.usun_all_widgets()

            self.button_manager("modyfikacja_artykuly", back_target = 'lista_artykułów' )
            self.view.dodaj_modyfikuj_artykul_view(nazwa_artykulu_string = info[0], kolor_artykulu_string = info[1], szczegoly_artykulu_string = info[2])

        self.firma_tree = self.view.name_tree(self.view.stock_frame, "Lista Firm", True)
        self.kategorie_tree = self.view.name_tree(self.view.secend_frame, "Kategorie Lista", True)

        if commend == "modyfikuj":
            firma_id_artykulu = info[4]
            kategoria_id_artykulu = info[3]

        self.sound.play_confirm_sound()

        self.load_kategorie_daemon(widok = "ukryj", select_item = kategoria_id_artykulu)
        self.load_firmy_deaemon(select_item = firma_id_artykulu)

    def wczytaj_informacje_artykul(self, artykul_id):
        artykul = self.db_session.query(Artykul_Lista).filter_by(id=artykul_id).first()

        nazwa_artykulu_string = artykul.nazwa #0
        kolor_artykulu_string = artykul.kolor #1
        szczegoly_artykulu_string = artykul.szczegoly #2
        kategoria_id_artykulu = artykul.kategoria_id #3
        firma_id_artykulu = artykul.firma_id #4

        return (nazwa_artykulu_string, kolor_artykulu_string, szczegoly_artykulu_string, kategoria_id_artykulu, firma_id_artykulu)

    def wczytaj_informacje_zamowienie(self, zamowienie_id):
        zamowienie = self.db_session.query(Zamowienie).filter_by(id=zamowienie_id).first()

        zamowienie_data_modyfikacja = zamowienie.data #0
        zamowienie_rabat_j = zamowienie.rabat_j #1
        zamowienie_rabat_procentowy = zamowienie.rabat_procent #2
        zamowienie_kupujacy_id = zamowienie.kupujacy_id #3
        zamowienie_sklep_id = zamowienie.sklep_id #4
        zamowienie_faktura_id = zamowienie.faktura_id #5

        return (zamowienie_data_modyfikacja, zamowienie_rabat_j, zamowienie_rabat_procentowy, zamowienie_kupujacy_id, zamowienie_sklep_id, zamowienie_faktura_id)

    def dodaj_modyfikuj_zamowienie(self, commend = "stworz"):
        if commend == "stworz":
            self.button_manager("dodaj_zamowienie")
            self.view.dodaj_modyfikuj_zamowienie_view()
            select_kupujacy = None
            select_sklep = None

        elif commend == "modyfikuj":
            selected_item = self.zamowienia_tree.selection()
            if not selected_item:
                leksykon = self.leksykon_messagebox["error_messagebox"]
                self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["order"])
                return

            self.zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            info = self.wczytaj_informacje_zamowienie(self.zamowienie_id)
            
            self.button_manager("modyfikuj_zamowienie")
            self.view.dodaj_modyfikuj_zamowienie_view(info[1], info[2], info[5])

            self.view.date_entry.set_date(info[0])
            select_kupujacy = info[3]
            select_sklep = info[4]

        self.zamowienia_frame.grid_remove()

        self.kupujacy_tree = self.view.name_tree(self.view.stock_frame, "Kupujacy", True)
        self.sklepy_tree = self.view.name_tree(self.view.secend_frame, "Sklepy", True)

        self.load_kupujacy_daemon(widok="ukryj", select_item = select_kupujacy)
        self.load_sklepy_daemon(widok="pokaz", select_item = select_sklep)

    def zatwierdz_nowy_modyfikuj_zamowienie(self, commend = "stworz"):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["buyer"])
            return
        
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["shop"])
            return

        try:
            rabat_j = float(self.view.rabat_j_var.get().replace(',', '.'))
        except tk.TclError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["unit_discount"])
            return
        
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["unit_discount"])
            return
        
        try:
            rabat_procentowy = float(self.view.rabat_p_var.get().replace(',', '.'))
        except tk.TclError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["proc_discount"])
            return
       
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["proc_discount"])
            return

        try:
            data = self.konwersja_string_do_data(self.view.zamowienie_data.get())
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["date"])
            return
        
        kupujacy_id = int(self.kupujacy_tree.item(self.kupujacy_tree.selection()[0], 'values')[0])
        sklep_id = int(self.sklepy_tree.item(self.sklepy_tree.selection()[0], 'values')[0])
        faktura_id = self.view.faktura_id.get() if self.view.faktura_id.get() != 0 else ""
        
        if commend == "stworz":
            zamowienie = Zamowienie(data=data, kupujacy_id=kupujacy_id, sklep_id=sklep_id, rabat_j=rabat_j, rabat_procent=rabat_procentowy, faktura_id=faktura_id)
            self.db_session.add(zamowienie)
            
        elif commend == "modyfikuj":
            zamowienie = self.db_session.query(Zamowienie).filter_by(id=self.zamowienie_id).first()
        
            if zamowienie:
                zamowienie.data = data
                zamowienie.rabat_j = rabat_j
                zamowienie.rabat_procent = rabat_procentowy
                zamowienie.kupujacy_id = kupujacy_id
                zamowienie.sklep_id = sklep_id
                zamowienie.faktura_id = faktura_id

        self.sound.play_confirm_sound()

        self.db_session.commit()
        self.powrot_do_glownego_okna()

    def zatwierdz_nowy_modyfikuj_artykul(self, commend = "stworz"):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["company"])
            return
        
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["category"])
            return

        nazwa = self.view.nazwa_artykulu_string.get()
        if not nazwa:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["name"])
            return
       
        firma_id = int(self.firma_tree.item(self.firma_tree.selection()[0], 'values')[0])
        kategoria_id = int(self.kategorie_tree.item(self.kategorie_tree.selection()[0], 'values')[0])
        if commend == "stworz":      
            artykul = Artykul_Lista(kategoria_id=kategoria_id, firma_id=firma_id, nazwa=nazwa, kolor = self.view.kolor_artykulu_string.get(), szczegoly=self.view.szczegoly_artykulu_string.get())
            self.db_session.add(artykul)

        elif commend == "modyfikuj":
            artykul = self.db_session.query(Artykul_Lista).filter_by(id=self.artykul_modyfikacja_id).first()
        
            if artykul:
                artykul.nazwa = nazwa 
                artykul.kolor = self.view.kolor_artykulu_string.get()
                artykul.szczegoly = self.view.szczegoly_artykulu_string.get()
                artykul.kategoria_id = kategoria_id 
                artykul.firma_id = firma_id

        self.sound.play_confirm_sound()

        self.db_session.commit()
        self.powrot_do_lista_artykulow()

#do poprawki
    def load_inside_zamowienie(self, id_zamowienia):
        self.zamowienia_frame.grid_remove()
        self.usun_all_widgets()
        self.button_manager("lista dodanych do zamowienia")
        self.inside_tree = self.view.inside_tree(self.stock_frame, 'Lista artykułów dodatych do zamówienia') 
        self.inside_tree.delete(*self.inside_tree.get_children())

        wynik_all = self.db_session.execute(
            select(
                artykuly_relacja.c.artykul_id,
                artykuly_relacja.c.cena_jednostkowa,
                artykuly_relacja.c.ilosc_artykulu
            )
            .where(
                artykuly_relacja.c.zamowienie_id == id_zamowienia
                )
        ).fetchall()

        existing_iids = set(self.inside_tree.get_children())

        artykul_data = []

        for wynik in wynik_all:
            id_art = wynik.artykul_id
            cena = f"{wynik.cena_jednostkowa if wynik.cena_jednostkowa else 0:.2f} {self.currency}"
            ilosc = wynik.ilosc_artykulu if wynik.ilosc_artykulu else 1

            artykul = self.db_session.query(Artykul_Lista).filter_by(id=id_art).first()
            kategoria = artykul.kategoria.nazwa if artykul.kategoria else None
            firma = artykul.firma.nazwa if artykul.firma else None
            nazwa = artykul.nazwa
            kolor = artykul.kolor
            szczegoly = artykul.szczegoly

            unique_id = f"{id_art}-{ilosc}"
            counter = 1
            while unique_id in existing_iids:
                unique_id = f"{id_art}-{ilosc}-{counter}"
                counter += 1

            existing_iids.add(unique_id)
            artykul_data.append((unique_id, id_art, cena, ilosc, kategoria, firma, nazwa, kolor, szczegoly))

        artykul_data.sort(key=lambda x: x[6].lower())

        for row in artykul_data:
            self.inside_tree.insert('', 'end', iid=row[0], values=row[1:])

    def edytuj_artykul_zamowienie(self):
        selected_item = self.inside_tree.selection()
        if not selected_item:
            return 
        
        relacja_name = self.inside_tree.item(self.inside_tree.selection()[0], 'values')
        cena = float(relacja_name[1].replace(" "+self.currency,"").replace(",","."))

        leksykon = self.leksykon_messagebox["edit_messagebox"]
        self.view.cena_ilosc_window(dsc = self.dsc, title=leksykon["heading"], id = relacja_name[0], relacja=relacja_name[2], cena = cena)
        self.button_manager("wyjdź_z_cena_ilosc_edycja", back_target = 'lista_artykułów')
        
        zamowienie_id = self.zamowienie_id
        self.load_inside_zamowienie(zamowienie_id)
        self.load_zamowienia_daemon(widok="ukryj")

    def dodaj_list_artykulow(self):
        self.list_artykuly(backTarget='zamówienie')

        self.artykuly_tree.bind("<Double-1>", self.on_double_click_dodawanie_artykulu_do_zamowienia)
    
    def cena_ilosc_edycja(self):
        try:
            cena_artykulu_var = float(self.view.cena_artykulu_var.get().replace(",", "."))
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["price"])
            return

        try:
            ilosc_artykulu_var =  float(self.view.ilosc_artykulu_var.get().replace(",", "."))
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["amount"])
            return
        
        self.db_session.execute(
            artykuly_relacja.update()
            .where(
                artykuly_relacja.c.zamowienie_id == self.zamowienie_id,
                artykuly_relacja.c.artykul_id == self.view.id_artykulu,
                artykuly_relacja.c.cena_jednostkowa == self.view.cena_artykulu_var_old,
                artykuly_relacja.c.ilosc_artykulu == self.view.ilosc_artykulu_var_old
                )
            .values(
                cena_jednostkowa = cena_artykulu_var, 
                ilosc_artykulu = ilosc_artykulu_var
                )
        )

        self.db_session.commit()

        zamowienie_id = self.zamowienie_id
        self.load_inside_zamowienie(zamowienie_id)
        self.view.window.destroy()

        return

    def anuluj_dodanie_artykulu_zamowienie(self):
        self.view.window.destroy()
        zamowienie_id = self.zamowienie_id

        self.load_inside_zamowienie(zamowienie_id)

    def cena_ilosc_dodanie(self):
        try:
            cena_artykulu_var = float(self.view.cena_artykulu_var.get().replace(",", "."))
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["price"])
            return

        try:
            ilosc_artykulu_var =  float(self.view.ilosc_artykulu_var.get().replace(",", "."))
        except ValueError:
            leksykon = self.leksykon_messagebox["error_messagebox"]
            self.messagebox_controller.messagebox(type="error", heading=leksykon["heading"], text=leksykon["text"]["amount"])
            return

        zamowienie_id = self.zamowienie_dodawanie_artykulu_id
        self.dodaj_artykul_do_zamowienie(zamowienie_id, self.cena_ilosc_select_item, cena_artykulu_var, ilosc_artykulu_var)
        
        self.load_zamowienia_daemon()
        self.load_inside_zamowienie(zamowienie_id)
        self.view.window.destroy()
    
    def dodaj_artykul_do_zamowienie(self, zamowienie, id_art, cena, ilosc):
        self.db_session.execute(
            artykuly_relacja.insert().values(
                zamowienie_id = zamowienie,
                artykul_id = id_art,
                cena_jednostkowa = cena,
                ilosc_artykulu = ilosc
            )
        )
        self.db_session.commit()

    def specjalne_znaki(self, text: str) -> bool:
        if text == None:
            return
        dozwolone_znaki = string.ascii_letters + string.digits + " .,-_/" + "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
        return any(znaki not in dozwolone_znaki for znaki in text)

    def konwersja_string_do_data(self, date):
        format = "%Y-%m-%d"
        date = datetime.datetime.strptime(date, format).date()
        return date
    
    def pokaz_stock_frame(self):
        if not self.zamowienia_frame.winfo_ismapped():
            self.usun_all_widgets()
            self.zamowienia_frame.grid()
            self.button_manager(frame="main", startup=True)

    def powrot_do_glownego_okna(self):
        self.pokaz_stock_frame()
        self.load_zamowienia_daemon()

    def powrot_do_lista_artykulow(self):
        self.usun_all_widgets()
        self.list_artykuly()

    def usun_all_widgets(self):
        try:
            if self.view.secend_frame:
                self.view.secend_frame.destroy()
            if self.view.third_frame:
                self.view.third_frame.destroy()
        except AttributeError:
            pass

        for widget in self.view.stock_frame.winfo_children():
            widget.destroy()

        for widget in self.view.button_stock_frame.winfo_children():
            widget.destroy()

    def show_message_async(self):
        self.messagebox_controller.show_message_async(master=self.stock_master)

    def hide_message_async(self):
        self.messagebox_controller.ukryj_message_async(master=self.stock_master)

    def on_double_click_dodawanie_artykulu_do_zamowienia(self, event):
        try:
            self.view.window.destroy()
        except AttributeError:
            pass
        
        selected_item = self.artykuly_tree.selection()
        self.zamowienie_dodawanie_artykulu_id = self.zamowienie_id
        if selected_item:
            artykul_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            self.cena_ilosc_select_item = artykul_id

            leksykon = self.leksykon_messagebox["add_messagebox"]
            self.view.cena_ilosc_window(dsc = self.dsc, title=leksykon["heading"])

            self.button_manager(frame="wyjdź_z_cena_ilosc_dodawanie", back_target="wyjdź_z_cena_ilosc_dodawanie")
            
            zamowienie_id = self.zamowienie_dodawanie_artykulu_id
            self.load_inside_zamowienie(zamowienie_id)
            
            self.sound.play_confirm_sound()

    def on_double_click_otwieranie_zamowienia(self, event):
        selected_item = self.zamowienia_tree.selection()
        self.zamowienie_id = selected_item

        if selected_item:
            self.zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            self.load_inside_zamowienie(self.zamowienie_id)

            self.sound.play_confirm_sound()

    def on_double_click_filtrowanie_kategoria(self, event):
        selected_item = self.kategorie_tree.selection()
        if selected_item:
            kategoria_id = self.kategorie_tree.item(selected_item[0], 'values')[0]
            self.load_artykuly(kategoria_id=kategoria_id)
            self.load_kategorie()

            self.sound.play_confirm_sound()

    def on_double_click_filtrowanie_kategoria_resetowanie(self, event):
        self.load_kategorie()
        self.load_artykuly()

        self.sound.play_confirm_sound()

