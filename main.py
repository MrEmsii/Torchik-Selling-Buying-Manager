import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, PhotoImage
from TkToolTip import ToolTip
from tkinterdnd2 import DND_FILES, TkinterDnD
from dbControler import SQLconnect, select, Kupujacy, Kategoria, Sklep, Firma, Zamowienie, Artykul_Lista, artykuly_relacja
from tkcalendar import DateEntry
import datetime as datetime
import time
import threading
import json
from pygame import mixer, mixer_music
from winsound import *

class FolderApp:
    def __init__(self, master):
        self.master = master
        self.dsc = os.path.dirname(__file__)
        
        if os.path.exists(self.dsc + "/setting.json") == False:
            self.json_setting(status = "start")
        
        self.konfiguracja_programu = self.json_setting(status="read")

        self.style = ttk.Style()
        master.tk.call('source', self.dsc + '/themes/awdark.tcl')

        self.style.theme_use("awdark")
        self.style.configure("Treeview", background="#D8E8E8", foreground="#2F3131", rowheight=20, fieldbackground="#E7E7E7", font=('Arial', 8))
        self.style.map("Treeview", background=[('selected', "#2F3131")], foreground=[('selected', '#D8E8E8')])

        master.title("Torchik")
        master.iconbitmap(os.path.join(self.dsc, "image", "icon.ico"))

        self.style.configure('TButton', justify="left", anchor='w')
        self.background_image = PhotoImage(file=os.path.join(self.dsc, "image", "background.png"))
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.db_session = SQLconnect(self.dsc)

        self.button_frame = ttk.Frame(master, padding=5)

        self.main_frame = ttk.Frame(master, padding=5)
        self.zamowienia_frame = ttk.Frame(master, padding=5)
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.button_icon_pack()
        self.start_frame()
        self.load_zamowienia_daemon()

        self.button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)

        master.grid_rowconfigure(0, weight=4)
        master.grid_rowconfigure(1, weight=4)
        master.grid_rowconfigure(2, weight=4)
        master.grid_rowconfigure(3, weight=4)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=2000)
        master.grid_columnconfigure(2, weight=2000)
        master.grid_columnconfigure(3, weight=2000)

    def json_setting(self, status = "read", key = None, value = None):
        if status == "start":
            config = {
                "volume": 0.1, 
                "language": "pl_PL",
                "start_sound": "start_sound.wav",
                "click_sound": "click_sound.wav",
                "error_sound": "error_sound.wav"
            }

            with open("setting.json", 'w', encoding='utf-8') as settings:
                json.dump(config, settings, ensure_ascii=False, indent=4)  

        elif status == "read":
            with open("setting.json", 'r') as settings:
                config = json.load(settings)
                return config

        elif status == "edit":
            config = self.json_setting(status="read")
            config[key] = value

    def start_frame(self):
        mixer.init()
        self.play_sound_on_start_demon()
        self.zamowienia_tree = self.stworz_zamowienie_tree(self.zamowienia_frame, 'Zamówienia') 
        self.button_manager(frame="main", startup = True)
        
        self.zamowienia_tree.bind("<Double-1>", self.on_double_click_otwieranie_zamowienia)
        self.zamowienia_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)

    def button_manager(self, frame, back_target = 'main', startup = False):
        if startup == False:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            for widget in self.button_frame.winfo_children():
                widget.destroy()
        
        if frame == "main":
            self.button_dodaj_zamowienie(self.button_frame)
            self.button_modyfikuj_zamowienie(self.button_frame)
            self.button_lista_artykulow(self.button_frame)
            self.button_lista_sklepow(self.button_frame)
            self.button_lista_kupujacych(self.button_frame)
            self.button_lista_kategorii(self.button_frame)
            self.button_lista_firm(self.button_frame)
            self.button_refresh_zamowienia(self.button_frame)  
            self.button_ustawienia(self.button_frame) 
            self.button_usun_zamowienie(self.button_frame)

        elif frame == "lista dodanych do zamowienia":
            self.button_dodaj_artykul_zamowienie(self.button_frame)
            self.button_usun_artykul_zamowienie(self.button_frame)

        elif frame == "kupujacy":
            self.button_dodaj_kupujacy(self.button_frame)
            self.button_zmiana_nazwa_kupujacy(self.button_frame)
            self.button_usun_kupujacy(self.button_frame)

        elif frame == "sklepy":
            self.button_dodaj_sklep(self.button_frame) 
            self.button_zmiana_nazwa_sklep(self.button_frame)
            self.button_usun_sklep(self.button_frame)

        elif frame == "firmy":
            self.button_dodaj_firma(self.button_frame) 
            self.button_zmiana_nazwa_firma(self.button_frame)
            self.button_usun_firma(self.button_frame)

        elif frame == "lista_artykuly":
            self.button_stworz_artykul(self.button_frame) 
            self.button_modyfikuj_artykul(self.button_frame) 
            self.button_zniszcz_artykul(self.button_frame)

        elif frame == "dodaj_zamowienie":
            self.buttons_zatwierdz_zamowienia(self.button_frame) 
            self.button_dodaj_kupujacy(self.button_frame)
            self.button_dodaj_sklep(self.button_frame) 

        elif frame == "modyfikuj_zamowienie":
            self.button_zatwierdz_edycje_zamowienie(self.button_frame) 
            self.button_dodaj_kupujacy(self.button_frame)
            self.button_dodaj_sklep(self.button_frame) 

        elif frame == "kategorie":
            self.button_dodaj_kategoria(self.button_frame) 
            self.button_zmiana_nazwa_kategoria(self.button_frame)
            self.button_usun_kategorie(self.button_frame)

        elif frame == 'tworzenie_artykuly':
            self.button_zatwierdz_artykul(self.button_frame)
            self.button_dodaj_firma(self.button_frame)
            self.button_dodaj_kategoria(self.button_frame) 

        elif frame == 'modyfikacja_artykuly':
            self.button_zatwierdz_edycje_artykul(self.button_frame)
            self.button_dodaj_firma(self.button_frame)
            self.button_dodaj_kategoria(self.button_frame) 

        elif frame == "wyjdź_z_cena_ilosc":
            self.button_zatwierdz_dodanie_artykulu(self.button_cena_ilosc_frame)
            self.button_anuluj_dodanie_artykulu(self.button_cena_ilosc_frame)

        if frame != 'main':
            self.button_back_pack(self.button_frame, back_target)
        self.main_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)

    def stworz_inside_tree(self, parent_frame, label_text):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=("id_artykul", 'Cena', 'Ilosc', "Kategoria", 'Marka', 'Artykul', 'Kolor', 'Szczegoly'), 
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack(side='left', expand=True, fill='both')

        tree.column('id_artykul', width=50, anchor='e')
        tree.heading('id_artykul', text='ID', anchor='center')

        tree.column('Cena', width=100, anchor='e')
        tree.heading('Cena', text='Cena', anchor='center')

        tree.column('Ilosc', width=100, anchor='e')
        tree.heading('Ilosc', text='Ilosc', anchor='center')

        tree.column('Kategoria', width=100, anchor='e')
        tree.heading('Kategoria', text='Kategoria', anchor='center')

        tree.column('Marka', width=100, anchor='e')
        tree.heading('Marka', text='Marka', anchor='center')

        tree.column('Artykul', width=100, anchor='e')
        tree.heading('Artykul', text='Artykul', anchor='center')     

        tree.column('Kolor', width=100, anchor='e')
        tree.heading('Kolor', text='Kolor', anchor='center')   

        tree.column('Szczegoly', width=300, anchor='e')
        tree.heading('Szczegoly', text='Szczegoly', anchor='center')

        tree.pack(expand=True, fill='both')

        return tree  

    def stworz_artykuly_tree(self, parent_frame, label_text):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=("id_artykułu", 'Kategoria', 'Firma', 'artykul','Kolor','szczegoly'), 
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack(side='left', expand=True, fill='both')

        tree.column('id_artykułu', width=20, anchor='e')
        tree.heading('id_artykułu', text='id_artykułu', anchor='e')

        tree.column('Kategoria', width=50, anchor='w')
        tree.heading('Kategoria', text='Kategoria', anchor='w')

        tree.column('Firma', width=50, anchor='w')
        tree.heading('Firma', text='Firma', anchor='w')

        tree.column('artykul', width=100, anchor='w')
        tree.heading('artykul', text='Artykuł', anchor='w')        

        tree.column('Kolor', width=100, anchor='w')
        tree.heading('Kolor', text='Kolor', anchor='w')

        tree.column('szczegoly', width=100, anchor='w')
        tree.heading('szczegoly', text='Szczegoly', anchor='w')
       
        tree.pack(expand=True, fill='both')

        return tree       

    def stworz_name_tree(self, parent_frame, label_text, status):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=('id', 'name'), 
            show='headings', 
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack(side='left', expand=True, fill='both')
        
        tree.column('id', width=10, anchor='e')
        tree.heading('id', text='ID', anchor='e')

        tree.column('name', width=100, anchor='w')
        tree.heading('name', text='Nazwa', anchor='w')
        tree.pack(expand=status, fill='both')

        return tree  

    def stworz_zamowienie_tree(self, parent_frame, label_text):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container,
            columns=("id_zamowiania", 'Data', 'Kupujacy', 'Sklep', 'Rabat jednostkowy', 'Rabat procentowy', 'Cena', "Cena_po_rabacie"),
            show='headings',
            yscrollcommand=scrollbar.set,
        )

        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack(side='left', expand=True, fill='both')

        tree.column('id_zamowiania', width=50, anchor='e')
        tree.heading('id_zamowiania', text='id_zamowiania', anchor='e')

        tree.column('Data', width=100, anchor='w')
        tree.heading('Data', text='Data', anchor='w')

        tree.column('Kupujacy', width=100, anchor='w')
        tree.heading('Kupujacy', text='Kupujacy', anchor='w')

        tree.column('Sklep', width=100, anchor='w')
        tree.heading('Sklep', text='Sklep', anchor='w')

        tree.column('Rabat jednostkowy', width=100, anchor='e')
        tree.heading('Rabat jednostkowy', text='Rabat jednostkowy', anchor='e')        

        tree.column('Rabat procentowy', width=100, anchor='e')
        tree.heading('Rabat procentowy', text='Rabat procentowy', anchor='e')

        tree.column('Cena', width=100, anchor='e')
        tree.heading('Cena', text='Cena', anchor='e')

        tree.column('Cena_po_rabacie', width=100, anchor='e')
        tree.heading('Cena_po_rabacie', text='Cena po rabacie', anchor='e')

        return tree

    def show_message_async_demon(self):
        threading.Thread(target=self.show_message_async, daemon=True).start()

    def play_sound_on_start_demon(self):
        if self.konfiguracja_programu["volume"] != 0:
            mixer.music.load(os.path.join(self.dsc, "sounds", self.konfiguracja_programu["start_sound"]))
            mixer.music.set_volume(self.konfiguracja_programu["volume"])
            mixer.music.play()

    def error_sound_demon(self):
        if self.konfiguracja_programu["volume"] != 0:
            mixer.music.load(os.path.join(self.dsc, "sounds", self.konfiguracja_programu["error_sound"]))
            mixer.music.set_volume(self.konfiguracja_programu["volume"])
            mixer.music.play()

    def show_message_async(self):
        self.msg_windows = tk.Toplevel(root)
        self.msg_windows.geometry("300x50+340+160")
        self.msg_windows.title("Inicjalizacja operacji")
        
        label = tk.Label(self.msg_windows, text="Inicjalizacja operacji, proszę poczekaj", padx=20, pady=10)
        label.pack()
        
        time.sleep(2)
        self.msg_windows.destroy()

    def ukryj_message_async(self):
        try:
            if self.msg_windows.winfo_exists():
                self.msg_windows.destroy()
        except AttributeError:
            pass

    def load_zamowienia_daemon(self, widok = "pokaz"):
        commend = self.load_zamowienia(widok = widok)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_zamowienia(self, widok):
        if widok == "pokaz":
            self.show_message_async_demon()

        zamowienia = self.db_session.query(Zamowienie).all()
        zamowienia_data = []

        for zamow in zamowienia:
            zamow_id = zamow.id
            zamow_data = zamow.data
            zamow_kupujacy = zamow.kupujacy.nazwa if zamow.kupujacy else " "
            zamow_sklep = zamow.sklep.nazwa if zamow.sklep else  " "
            rabat_j = f"{zamow.rabat_j:.2f} PLN"
            rabat_proc = f"{zamow.rabat_procent :.0f} %"
            zamow_cena = f"{zamow.oblicz_cene(self.db_session):,.2f} PLN".replace(",", " ")
            zamow_cena_rabat = f"{zamow.oblicz_cene_rabat(self.db_session):,.2f} PLN".replace(",", " ")
            zamowienia_data.append((zamow_id, zamow_data, zamow_kupujacy, zamow_sklep, rabat_j, rabat_proc, zamow_cena, zamow_cena_rabat))

        zamowienia_data.sort(key=lambda x:x[0], reverse=True )
        zamowienia_data.sort(key=lambda x:x[1], reverse=True)
        self.zamowienia_tree.delete(*self.zamowienia_tree.get_children())

        for z_id, data, kupujacy, sklep, rabat_1, rabat_2, cena, cena_rabat in zamowienia_data:
            self.zamowienia_tree.insert('', 'end', values=(z_id, data, kupujacy, sklep, rabat_1, rabat_2, cena, cena_rabat))

        self.ukryj_message_async()

    def load_sklepy(self):
        sklepy = self.db_session.query(Sklep).all()
        sklepy_data = []

        for sklep in sklepy:
            sklep_id = sklep.id
            sklep_nazwa = sklep.nazwa
            sklepy_data.append((sklep_id, sklep_nazwa))

        self.sklepy_tree.delete(*self.sklepy_tree.get_children())
        sklepy_data.sort(key=lambda x: x[1].lower())

        for sklep_id, sklep_nazwa in sklepy_data:
            self.sklepy_tree.insert('', 'end', values=(sklep_id, sklep_nazwa))

    def load_kupujacy(self):
        kupujacy = self.db_session.query(Kupujacy).all()
        kupujacy_data = []

        for kup in kupujacy:
            kup_id = kup.id
            kup_nazwa = kup.nazwa
            kupujacy_data.append((kup_id, kup_nazwa))

        self.kupujacy_tree.delete(*self.kupujacy_tree.get_children())
        kupujacy_data.sort(key=lambda x:x[1])

        for kup_id, kup_nazwa in kupujacy_data:
            self.kupujacy_tree.insert('', 'end', values=(kup_id, kup_nazwa))

    def load_kategorie(self):
        kategorie = self.db_session.query(Kategoria).all()
        kategorie_data = []

        for kategoria in kategorie:
            kategoria_id = kategoria.id
            kategoria_name = kategoria.nazwa
            kategorie_data.append((kategoria_id, kategoria_name))

        self.kategorie_tree.delete(*self.kategorie_tree.get_children())
        kategorie_data.sort(key=lambda x:x[1])

        for kategoria_id, kategoria_name in kategorie_data:
            self.kategorie_tree.insert('', 'end', values=(kategoria_id, kategoria_name))    

    def load_firmy(self):
        firmy = self.db_session.query(Firma).all()
        firmy_data = []

        for firma in firmy:
            firma_id = firma.id
            firma_name = firma.nazwa
            firmy_data.append((firma_id, firma_name))

        self.firma_tree.delete(*self.firma_tree.get_children())
        firmy_data.sort(key=lambda x:x[1])

        for firma_id, firma_name in firmy_data:
            self.firma_tree.insert('', 'end', values=(firma_id, firma_name))  

    def load_artykuly(self, kategoria_id = None):
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
        self.artykuly_tree.delete(*self.artykuly_tree.get_children())

        for id, kategoria, firma, nazwa, kolor, szczegoly in artykuly_data:
            self.artykuly_tree.insert('', 'end', values=(id, kategoria, firma, nazwa, kolor, szczegoly))

    def load_inside_zamowienie(self, id_zamowienia):
        self.zamowienia_frame.grid_remove()
        self.usun_all_widgets()
        self.button_manager("lista dodanych do zamowienia")
        self.inside_tree = self.stworz_inside_tree(self.main_frame, 'Lista artykułów dodatych do zamówienia') 
        self.inside_tree.delete(*self.inside_tree.get_children())

        wynik_all = self.db_session.execute(
            select(
                artykuly_relacja.c.artykul_id,
                artykuly_relacja.c.cena_jednostkowa,
                artykuly_relacja.c.ilosc_artykulu
            ).where(artykuly_relacja.c.zamowienie_id == id_zamowienia)
        ).fetchall()

        existing_iids = set(self.inside_tree.get_children())

        artykul_data = []

        for wynik in wynik_all:
            id_art = wynik.artykul_id
            cena = f"{wynik.cena_jednostkowa if wynik.cena_jednostkowa else 0:.2f} PLN"
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

    def on_double_click_otwieranie_zamowienia(self, event):
        selected_item = self.zamowienia_tree.selection()
        self.zamowienie_id = selected_item

        if selected_item:
            self.zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            self.load_inside_zamowienie(self.zamowienie_id)

    def cena_ilosc_window(self):
        self.window = tk.Toplevel(self.master)
        self.window.geometry("300x180+500+300")

        self.window.iconbitmap(os.path.join(self.dsc, "image", "icon.ico"))
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.button_cena_ilosc_frame = ttk.Frame(self.window, padding=5)
        self.filament_frame = ttk.Frame(self.window, padding=5)

        self.button_cena_ilosc_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.filament_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.button_manager(frame="wyjdź_z_cena_ilosc", back_target="wyjdź_z_cena_ilosc")

        cena_label = ttk.Label(self.filament_frame, text = 'Cena:', font=('calibre', 10, 'bold'), anchor='center')
        ilosc_label = ttk.Label(self.filament_frame, text = 'Ilość:', font=('calibre', 10, 'bold'), anchor='w')
        
        self.cena_artykulu_var = tk.StringVar(value=0.0)
        self.ilosc_artykulu_var = tk.StringVar(value=1.0)

        cena_entry = ttk.Entry(self.filament_frame, textvariable = self.cena_artykulu_var, font=('calibre',10,'normal'), width=5)
        ilosc_entry = ttk.Entry(self.filament_frame, textvariable = self.ilosc_artykulu_var, font=('calibre',10,'normal'), width=5)

        cena_label.grid(row=1, column=1)
        ilosc_label.grid(row=2, column=1)

        cena_entry.grid(row=1, column=2)
        ilosc_entry.grid(row=2, column=2)

        zamowienie_id = self.zamowienie_dodawanie_artykulu_id
        self.load_inside_zamowienie(zamowienie_id)

        self.filament_frame.grid_rowconfigure(0, weight=80)
        self.filament_frame.grid_rowconfigure(1, weight=1)
        self.filament_frame.grid_rowconfigure(2, weight=1)
        self.filament_frame.grid_rowconfigure(3, weight=80)

        self.window.grid_rowconfigure(0, weight=4)
        self.window.grid_rowconfigure(1, weight=4)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2000)
        self.window.grid_columnconfigure(2, weight=2000)

    def cena_ilosc_dodanie(self):
        try:
            cena_artykulu_var = float(self.cena_artykulu_var.get())
        except ValueError:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Nieprawidłowa wartość d! Wpisz liczbę.")
            return

        try:
            ilosc_artykulu_var =  float(self.ilosc_artykulu_var.get())
        except ValueError:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Nieprawidłowa wartość f! Wpisz liczbę.")
            return

        zamowienie_id = self.zamowienie_dodawanie_artykulu_id
        self.dodaj_artykul_do_zamowienie(zamowienie_id, self.cena_ilosc_select_item, cena_artykulu_var, ilosc_artykulu_var)
        
        self.load_zamowienia_daemon()
        self.load_inside_zamowienie(zamowienie_id)
        self.window.destroy()

    def on_double_click_dodawanie_artykulu_do_zamowienia(self, event):
        selected_item = self.artykuly_tree.selection()
        self.zamowienie_dodawanie_artykulu_id = self.zamowienie_id
        if selected_item:
            artykul_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            self.cena_ilosc_select_item = artykul_id
            self.cena_ilosc_window()

    def on_double_click_filtrowanie_kategoria(self, event):
        selected_item = self.kategorie_tree.selection()
        if selected_item:
            kategoria_id = self.kategorie_tree.item(selected_item[0], 'values')[0]
            self.load_artykuly(kategoria_id=kategoria_id)
            self.load_kategorie()

    def on_double_click_filtrowanie_kategoria_resetowanie(self, event):
        self.load_kategorie()
        self.load_artykuly()

    def wczytaj_informacje_zamowienie(self, zamowienie_id):
        zamowienie = self.db_session.query(Zamowienie).filter_by(id=zamowienie_id).first()

        self.zamowienie_data_modyfikacja = zamowienie.data
        self.zamowienie_rabat_j = zamowienie.rabat_j
        self.zamowienie_rabat_procentowy = zamowienie.rabat_procent
        self.zamowienie_kupujacy_id = zamowienie.kupujacy_id
        self.zamowienie_sklep_id = zamowienie.sklep_id

    def dodaj_modyfikuj_zamowienie(self, commend = "stworz"):
        if commend == "stworz":
            self.rabat_j_var = tk.DoubleVar()
            self.rabat_p_var = tk.DoubleVar()
            self.zamowienie_data = tk.StringVar()
            self.button_manager("dodaj_zamowienie")

        elif commend == "modyfikuj":
            selected_item = self.zamowienia_tree.selection()
            if not selected_item:
                self.error_sound_demon()
                messagebox.showerror("Błąd", "Brak wybranego zamówienia! Wybierz zamówienie.")
                return

            self.zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            
            self.wczytaj_informacje_zamowienie(self.zamowienie_id)

            self.rabat_j_var = tk.DoubleVar(value=self.zamowienie_rabat_j)
            self.rabat_p_var = tk.DoubleVar(value=self.zamowienie_rabat_procentowy)
            self.button_manager("modyfikuj_zamowienie")

        self.zamowienia_frame.grid_remove()
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=1, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=1, column=1, columnspan=5, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
                
        self.kupujacy_tree = self.stworz_name_tree(self.main_frame, "Kupujacy", True)
        self.sklepy_tree = self.stworz_name_tree(self.secend_frame, "Sklepy", True)

        date_label = ttk.Label(self.third_frame, text = 'Data:', font=('calibre', 10, 'bold'), anchor='w')
       
        rabat_j_label = ttk.Label(self.third_frame, text = 'Rabat jednostkowy:', font=('calibre', 10, 'bold'), anchor='w')
        rabat_p_label = ttk.Label(self.third_frame, text = 'Rabat procentowy:', font=('calibre',10, 'bold'), anchor='w')

        rabat_j_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_j_var, font=('calibre',10,'normal'), width=10)
        rabat_p_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_p_var, font=('calibre',10,'normal'), width=10)

        self.zamowienie_data = tk.StringVar()
        date_entry = DateEntry(self.third_frame, localestr='pl_PL', date_pattern="yyyy-mm-dd", textvariable=self.zamowienie_data, width=10, set_date=datetime.date(2023,4,2))
        if commend == "modyfikuj":
            date_entry.set_date(self.zamowienie_data_modyfikacja)

        self.third_frame.grid_rowconfigure(0, weight=80)
        self.third_frame.grid_rowconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(2, weight=1)
        self.third_frame.grid_rowconfigure(3, weight=1)
        self.third_frame.grid_rowconfigure(4, weight=80)

        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_columnconfigure(1, weight=10)

        date_label.grid(row=1,column=0)
        rabat_j_label.grid(row=2,column=0)
        rabat_p_label.grid(row=3,column=0)

        date_entry.grid(row=1,column=1)
        rabat_j_entry.grid(row=2,column=1)
        rabat_p_entry.grid(row=3,column=1)

        self.load_kupujacy()
        self.load_sklepy()

        if commend == "modyfikuj":
            self.zaznacz_wiersz_z_wartoscia(self.kupujacy_tree, 'id', self.zamowienie_kupujacy_id)
            self.zaznacz_wiersz_z_wartoscia(self.sklepy_tree, 'id', self.zamowienie_sklep_id)

    def konwersja_string_do_data(self, date):
        format = "%Y-%m-%d"
        date = datetime.datetime.strptime(date, format).date()
        return date

    def zatwierdz_nowy_modyfikuj_zamowienie(self, commend = "stworz"):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Brak wybranego kupującego! Wybierz kupującego.")
            return
        
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Brak wybranego sklepu! Wybierz sklep.")
            return

        try:
            rabat_j = self.rabat_j_var.get()
        except tk.TclError:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Nieprawidłowa wartość rabatu! Wpisz liczbę.")
            return

        try:
            rabat_procentowy = self.rabat_p_var.get()
        except tk.TclError:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Nieprawidłowa wartość rabatu! Wpisz liczbę.")
            return
       
        try:
            data = self.konwersja_string_do_data(self.zamowienie_data.get())
        except ValueError:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Nieprawidłowa data! Wpisz date.\n             RRRR-MM-DD")
            return
        
        kupujacy_id = int(self.kupujacy_tree.item(self.kupujacy_tree.selection()[0], 'values')[0])
        sklep_id = int(self.sklepy_tree.item(self.sklepy_tree.selection()[0], 'values')[0])
        
        if commend == "stworz":
            zamowienie = Zamowienie(data=data, kupujacy_id=kupujacy_id, sklep_id=sklep_id, rabat_j=rabat_j, rabat_procent=rabat_procentowy)
            self.db_session.add(zamowienie)
            
        elif commend == "modyfikuj":
            zamowienie = self.db_session.query(Zamowienie).filter_by(id=self.zamowienie_id).first()
        
            if zamowienie:
                zamowienie.data = data
                zamowienie.rabat_j = rabat_j
                zamowienie.rabat_procent = rabat_procentowy
                zamowienie.kupujacy_id = kupujacy_id
                zamowienie.sklep_id = sklep_id

        self.db_session.commit()
        self.powrot_do_glownego_okna()

    def usun_zamowienie(self):
        selected_item = self.zamowienia_tree.selection()
        if not selected_item:
            return

        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia zamówienia:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            
            self.db_session.query(Zamowienie).filter_by(id=zamowienie_id).delete(synchronize_session=False)
            self.db_session.commit()
            self.load_zamowienia_daemon()  

    def usun_artykul_zamowienie(self):
        selected_item = self.inside_tree.selection()
        if not selected_item:
            return
        
        relacja_name = self.inside_tree.item(self.inside_tree.selection()[0], 'values')
        dialog = simpledialog.askstring("Usuń folder", "Czy jesteś pewien usunięcia projektu:\n\nCzynność NIE odwracalna\n\nNapisz YES lub TAK \t\t\t")
        if dialog == "YES" or dialog == "TAK" or dialog == "tak" or dialog == "yes":
            self.db_session.execute(
                artykuly_relacja.delete()
                .where(artykuly_relacja.c.zamowienie_id == self.zamowienie_id,
                artykuly_relacja.c.artykul_id == relacja_name[0],
                artykuly_relacja.c.ilosc_artykulu == relacja_name[2]
                )
            )
            self.db_session.commit()
            self.load_inside_zamowienie(self.zamowienie_id)

        self.load_zamowienia_daemon()

    def stworz_modyfikuj_artykul(self, commend = "stworz"):
        self.zamowienia_frame.grid_remove()

        if commend == "stworz":
            self.usun_all_widgets()

            self.nazwa_artykulu_string = None
            self.kolor_artykulu_string = None
            self.szczegoly_artykulu_string = None
            self.button_manager("tworzenie_artykuly", back_target = 'lista_artykułów' )

        elif commend == "modyfikuj":
            selected_item = self.artykuly_tree.selection()
            if not selected_item:
                self.error_sound_demon()
                messagebox.showerror("Błąd", "Brak wybranego artykułu! Wybierz artykuł.")
                return
        
            self.artykul_modyfikacja_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            self.wczytaj_informacje_artykul(self.artykul_modyfikacja_id)
            self.usun_all_widgets()
            self.button_manager("modyfikacja_artykuly", back_target = 'lista_artykułów' )

        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=2, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        
        self.firma_tree = self.stworz_name_tree(self.main_frame, "Lista Firm", True)
        self.kategorie_tree = self.stworz_name_tree(self.secend_frame, "Kategorie Lista", True)

        nazwa_label = ttk.Label(self.third_frame, text = 'Nazwa artykułu:', font=('calibre', 10, 'bold'), anchor='center')
        kolor_label = ttk.Label(self.third_frame, text = 'Ewentualny kolor:', font=('calibre', 10, 'bold'), anchor='center')
        szczegoly_label = ttk.Label(self.third_frame, text = 'Ewentualne szczegoły:', font=('calibre', 10, 'bold'), anchor='w')
        
        self.nazwa_artykulu_string = tk.StringVar(value=self.nazwa_artykulu_string)
        self.kolor_artykulu_string = tk.StringVar(value=self.kolor_artykulu_string)
        self.szczegoly_artykulu_string = tk.StringVar(value=self.szczegoly_artykulu_string)

        nazwa_entry = ttk.Entry(self.third_frame, textvariable = self.nazwa_artykulu_string, font=('calibre',10,'normal'), width=30)
        kolor_entry = ttk.Entry(self.third_frame, textvariable = self.kolor_artykulu_string, font=('calibre',10,'normal'), width=30)
        szczegoly_entry = ttk.Entry(self.third_frame, textvariable = self.szczegoly_artykulu_string, font=('calibre',10,'normal'), width=30)

        self.third_frame.grid_rowconfigure(0, weight=80)
        self.third_frame.grid_rowconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(2, weight=1)
        self.third_frame.grid_rowconfigure(3, weight=1)
        self.third_frame.grid_rowconfigure(4, weight=80)

        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_columnconfigure(1, weight=10)
        
        nazwa_label.grid(row=1,column=0)
        kolor_label.grid(row=2,column=0)
        szczegoly_label.grid(row=3,column=0)

        nazwa_entry.grid(row=1,column=1)
        kolor_entry.grid(row=2,column=1)
        szczegoly_entry.grid(row=3,column=1)

        self.load_kategorie()
        self.load_firmy()

        if commend == "modyfikuj":
            self.zaznacz_wiersz_z_wartoscia(self.firma_tree, 'id', self.firma_id_artykulu)
            self.zaznacz_wiersz_z_wartoscia(self.kategorie_tree, 'id', self.kategoria_id_artykulu)

    def zaznacz_wiersz_z_wartoscia(self, treeview, kolumna, wartosc):
        for item in treeview.get_children():
            if treeview.set(item, kolumna) == str(wartosc):
                treeview.selection_set(item)
                treeview.focus(item)
                treeview.see(item)
                break

    def wczytaj_informacje_artykul(self, artykul_id):
        artykul = self.db_session.query(Artykul_Lista).filter_by(id=artykul_id).first()

        self.nazwa_artykulu_string = artykul.nazwa
        self.kolor_artykulu_string = artykul.kolor
        self.szczegoly_artykulu_string = artykul.szczegoly
        self.kategoria_id_artykulu = artykul.kategoria_id
        self.firma_id_artykulu = artykul.firma_id

    def zatwierdz_nowy_modyfikuj_artykul(self, commend = "stworz"):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Brak wybranej firmy! Wybierz firmę.")
            return
        
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Brak wybranej kategori artykulu! Wybierz kategorie.")
            return

        nazwa = self.nazwa_artykulu_string.get()
        if not nazwa:
            self.error_sound_demon()
            messagebox.showerror("Błąd", "Brak nazwy artykułu! Wpisz nazwę.")
            return
       
        firma_id = int(self.firma_tree.item(self.firma_tree.selection()[0], 'values')[0])
        kategoria_id = int(self.kategorie_tree.item(self.kategorie_tree.selection()[0], 'values')[0])
        if commend == "stworz":      
            artykul = Artykul_Lista(kategoria_id=kategoria_id, firma_id=firma_id, nazwa=nazwa, kolor = self.kolor_artykulu_string.get(), szczegoly=self.szczegoly_artykulu_string.get())
            self.db_session.add(artykul)
        elif commend == "modyfikuj":
            artykul = self.db_session.query(Artykul_Lista).filter_by(id=self.artykul_modyfikacja_id).first()
        
            if artykul:
                artykul.nazwa = nazwa 
                artykul.kolor = self.kolor_artykulu_string.get()
                artykul.szczegoly = self.szczegoly_artykulu_string.get()
                artykul.kategoria_id = kategoria_id 
                artykul.firma_id = firma_id

        self.db_session.commit()
        self.powrot_do_lista_artykulow()

    def zniszcz_artykul(self):
        selected_item = self.artykuly_tree.selection()
        if not selected_item:
            return

        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia artykułu:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            artykul_id = self.artykuly_tree.item(selected_item[0], 'values')[0]
            self.db_session.query(Artykul_Lista).filter_by(id=artykul_id).delete(synchronize_session=False)
            self.db_session.commit()
            self.powrot_do_lista_artykulow()

    def dodaj_artykul_do_zamowienie(self, zamowienie, id_art, cena, ilosc):
        self.db_session.execute(artykuly_relacja.insert().values(
            zamowienie_id = zamowienie,
            artykul_id = id_art,
            cena_jednostkowa = cena,
            ilosc_artykulu = ilosc
        ))
        self.db_session.commit()

    def stworz_kupujacy(self):
        kupujacy_name = simpledialog.askstring("Dodaj Kupującego", "Podaj nazwę KUPUJĄCEGO: \t\t\t")
        if kupujacy_name is not None:
            kupujacy = Kupujacy(nazwa=kupujacy_name)
            self.db_session.add(kupujacy)
            self.db_session.commit()
            self.load_kupujacy()    
        
    def zmien_nazwa_kupujacy(self):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            return

        element_value = self.kupujacy_tree.item(selected_item[0], 'values')
        kupujacy_id = element_value[0]
        stara_nazwa = element_value[1]

        new_value = simpledialog.askstring("Edit",'Nowa wartość\t\t\t', initialvalue=stara_nazwa)

        if new_value and new_value.strip():
            kupujacy = self.db_session.query(Kupujacy).filter_by(id=kupujacy_id).first()

            if kupujacy:
                kupujacy.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_kupujacy() 

    def usun_kupujacego(self):
        selected_item = self.kupujacy_tree.selection()
        if not selected_item:
            return
        
        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia kupującego:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            kupujacy_id = self.kupujacy_tree.item(self.kupujacy_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Kupujacy).filter_by(id=kupujacy_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_zamowienia_daemon()
            self.load_kupujacy()   

    def stworz_sklep(self):
        sklep_name = simpledialog.askstring("Dodaj Sklep", "Podaj nazwę SKLEPU: \t\t\t")
        if sklep_name is not None:
            sklep = Sklep(nazwa=sklep_name)
            self.db_session.add(sklep)
            self.db_session.commit()
            self.load_sklepy()    

    def zmien_nazwa_sklep(self):
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            return

        element_value = self.sklepy_tree.item(selected_item[0], 'values')
        sklep_id = element_value[0]
        stara_nazwa = element_value[1]

        new_value = simpledialog.askstring("Edit",'Nowa wartość\t\t\t', initialvalue=stara_nazwa)

        if new_value and new_value.strip():
            sklep = self.db_session.query(Sklep).filter_by(id=sklep_id).first()

            if sklep:
                sklep.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon(widok = "ukryj")
                self.load_sklepy() 

    def usun_sklep(self):
        selected_item = self.sklepy_tree.selection()
        if not selected_item:
            return
        
        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia sklepu:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            sklep_id = self.sklepy_tree.item(self.sklepy_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Sklep).filter_by(id=sklep_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_sklepy()    

    def stworz_firma(self):
        firma_name = simpledialog.askstring("Dodaj firme", "Podaj nazwę FIRMY: \t\t\t")
        if firma_name is not None:
            firma = Firma(nazwa=firma_name)
            self.db_session.add(firma)
            self.db_session.commit()
            self.load_firmy()    

    def zmien_nazwa_firma(self):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            return

        element_value = self.firma_tree.item(selected_item[0], 'values')
        firma_id = element_value[0]
        stara_nazwa = element_value[1]

        new_value = simpledialog.askstring("Edit",'Nowa wartość\t\t\t', initialvalue=stara_nazwa)

        if new_value and new_value.strip():
            firma = self.db_session.query(Firma).filter_by(id=firma_id).first()

            if firma:
                firma.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_firmy() 

    def usun_firma(self):
        selected_item = self.firma_tree.selection()
        if not selected_item:
            return
        
        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia firmy:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            firma_id = self.firma_tree.item(self.firma_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Firma).filter_by(id=firma_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_firmy()    

    def stworz_kategoria(self):
        kategoria_name = simpledialog.askstring("Dodaj kategorie", "Podaj nazwę KATEGORII: \t\t\t")
        if kategoria_name is not None:
            kategoria = Kategoria(nazwa=kategoria_name)
            self.db_session.add(kategoria)
            self.db_session.commit()
            self.load_kategorie()    

    def zmien_nazwa_kategoria(self):
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            return

        element_value = self.kategorie_tree.item(selected_item[0], 'values')
        kategoria_id = element_value[0]
        stara_nazwa = element_value[1]

        new_value = simpledialog.askstring("Edit",'Nowa wartość\t\t\t', initialvalue=stara_nazwa)

        if new_value and new_value.strip():
            kategoria = self.db_session.query(Kategoria).filter_by(id=kategoria_id).first()

            if kategoria:
                kategoria.nazwa = new_value 
                self.db_session.commit()
                self.load_zamowienia_daemon()
                self.load_kategorie() 

    def usun_kategorie(self):
        selected_item = self.kategorie_tree.selection()
        if not selected_item:
            return
        
        dialog = simpledialog.askstring(
            "Usuń", "Czy jesteś pewien usunięcia kategorii:\n\n"
                    "Czynność NIEodwracalna\n\n"
                    "Napisz YES lub TAK \t\t\t"
        )

        if dialog and dialog.lower() in ["yes", "tak"]:
            kategoria_id = self.kategorie_tree.item(self.kategorie_tree.selection()[0], 'values')[0]
            obj = self.db_session.query(Kategoria).filter_by(id=kategoria_id).first()
            self.db_session.delete(obj)
            self.db_session.commit()
            self.load_kategorie()    

    def dodaj_list_artykulow(self):
        self.list_artykulow(backTarget='zamówienie')

        self.artykuly_tree.bind("<Double-1>", self.on_double_click_dodawanie_artykulu_do_zamowienia)

    def list_kupujacy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager("kupujacy")
        self.kupujacy_tree = self.stworz_name_tree(self.main_frame, "Kupujacy", True)
        self.load_kupujacy()

    def list_firmy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager(frame="firmy")
        self.firma_tree = self.stworz_name_tree(self.main_frame, "Firmy", True)
        self.load_firmy()

    def list_sklepy(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager("sklepy")
        self.sklepy_tree = self.stworz_name_tree(self.main_frame, "Sklepy", True)
        self.load_sklepy()

    def list_kategorie(self):
        self.zamowienia_frame.grid_remove()
        self.button_manager(frame="kategorie")
        self.kategorie_tree = self.stworz_name_tree(self.main_frame, "Kategorie", True)

        self.load_kategorie()

    def list_artykulow(self, backTarget = 'main'):
        self.zamowienia_frame.grid_remove()
        self.secend_frame = ttk.Frame(self.master, padding=5)

        self.button_manager("lista_artykuly", back_target=backTarget)
        self.main_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=0, column=2, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
        
        self.kategorie_tree = self.stworz_name_tree(self.main_frame, "Kategorie Lista", True)
        self.artykuly_tree = self.stworz_artykuly_tree(self.secend_frame, "Artykuły Lista")
        
        self.load_kategorie()
        self.load_artykuly()
        
        self.kategorie_tree.bind("<Double-1>", self.on_double_click_filtrowanie_kategoria)
        self.kategorie_tree.bind("<Double-3>", self.on_double_click_filtrowanie_kategoria_resetowanie)

    def refresh(self):
        pass

    def ustawienia_programu(self):
        print("dodać ustawienia")

    def usun_all_widgets(self):
        if self.secend_frame:
            self.secend_frame.destroy()

        if self.third_frame:
            self.third_frame.destroy()

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def button_icon_pack(self):
        self.stworz_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)
        self.edit_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)
        self.stworz_art_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)
        self.usun_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)
        self.stworz_zamowienie_inside_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(20, 20)
        self.backButton_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)
        self.stworz_kupujacego_inside_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(20, 20)
        self.stworz_sklep_inside_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(20, 20)
        self.refresh_element_icon = PhotoImage(file=os.path.join(self.dsc, "image", "delete_project_icon.png")).subsample(8, 8)

    def button_back_pack(self, frame, commend = "main"):
        if commend == "main":
            commend = self.pokaz_main_frame
            message_tooltip = "Wróć do głównego okna"
        elif commend == "lista_artykułów":
            commend = self.powrot_do_lista_artykulow
            message_tooltip = "Wróć do listy artykułów"
        elif commend == "zamówienie":
            commend = lambda: self.load_inside_zamowienie(self.zamowienie_id)
            message_tooltip =  "Wróć do zamówienia"
        self.dodaj_button = ttk.Button(frame, text="Wróć", command=commend, width = 10, image=self.backButton_icon, compound="left")
        self.dodaj_button.pack(side='bottom', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg=message_tooltip, follow=True)

    def pokaz_main_frame(self):
        if not self.zamowienia_frame.winfo_ismapped():
            self.usun_all_widgets()
            self.zamowienia_frame.grid()
            self.button_manager(frame="main", startup=True)

    def powrot_do_glownego_okna(self):
        self.pokaz_main_frame()
        self.load_zamowienia_daemon()

    def powrot_do_lista_artykulow(self):
        self.usun_all_widgets()
        self.list_artykulow()

    def button_ustawienia(self, frame):
        print(self.konfiguracja_programu["language"])
        self.dodaj_button = ttk.Button(frame, text="Ustawienia", command=self.ustawienia_programu, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='bottom', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nzamówienie", command=self.dodaj_modyfikuj_zamowienie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_modyfikuj_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Edytuj\nzamówienie", command=lambda: self.dodaj_modyfikuj_zamowienie(commend="modyfikuj"), width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nzamówienie", command=self.usun_zamowienie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='bottom', padx=1, pady=(3,30))
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)
        
    def buttons_zatwierdz_zamowienia(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zatwierdź\nzamówienie", command=self.zatwierdz_nowy_modyfikuj_zamowienie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=(3,30))
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zatwierdz_edycje_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zatwierdź\nedycje\nzamówienia", command=lambda: self.zatwierdz_nowy_modyfikuj_zamowienie(commend="modyfikuj"), width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=(3,30))  
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_lista_artykulow(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Lista\nartykułów", command=self.list_artykulow, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=(30,30))
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_lista_sklepow(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Lista\nsklepów", command=self.list_sklepy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_lista_firm(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Lista\nfirm", command=self.list_firmy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_lista_kupujacych(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Lista\nkupujących", command=self.list_kupujacy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)    
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)
        
    def button_lista_kategorii(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Lista\nkategorii", command=self.list_kategorie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_stworz_artykul(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Stwórz\nartykuł", command=self.stworz_modyfikuj_artykul, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_modyfikuj_artykul(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Modyfikuj\nartykułu", command=lambda: self.stworz_modyfikuj_artykul(commend="modyfikuj"), width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zatwierdz_artykul(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zatwierdź\nartykuł", command=self.zatwierdz_nowy_modyfikuj_artykul, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=(3,30))       
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zatwierdz_edycje_artykul(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zatwierdź\nedycję\nartykułu", command=lambda: self.zatwierdz_nowy_modyfikuj_artykul(commend="modyfikuj"), width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=(3,30))  
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zniszcz_artykul(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nartykuł", command=self.zniszcz_artykul, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)   
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_artykul_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nartykuł do\nzamowienia", command=self.dodaj_list_artykulow, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zatwierdz_dodanie_artykulu(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nartykuł do\nzamowienia", command=self.cena_ilosc_dodanie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=2, pady=2)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_anuluj_dodanie_artykulu(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Anuluj\ndodawanie\nartykułu do\nzamówienia", command=self.window.destroy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=2, pady=2)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_artykul_zamowienie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nartykuł z\nzamówienia", command=self.usun_artykul_zamowienie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_kupujacy(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nkupującego", command=self.stworz_kupujacy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)        
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zmiana_nazwa_kupujacy(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zmień\nnazwę\nkupującego", command=self.zmien_nazwa_kupujacy, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_kupujacy(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nkupującego", command=self.usun_kupujacego, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_sklep(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nsklep", command=self.stworz_sklep, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zmiana_nazwa_sklep(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zmień\nnazwę\nsklepu", command=self.zmien_nazwa_sklep, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_sklep(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nsklep", command=self.usun_sklep, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_firma(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nfirma", command=self.stworz_firma, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zmiana_nazwa_firma(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zmień\nnazwę\nfirmy", command=self.zmien_nazwa_firma, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_firma(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nfirma", command=self.usun_firma, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_dodaj_kategoria(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Dodaj\nkategoria", command=self.stworz_kategoria, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_zmiana_nazwa_kategoria(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Zmień\nnazwę\nkategorii", command=self.zmien_nazwa_kategoria, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3) 
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_usun_kategorie(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Usuń\nkategorie", command=self.usun_kategorie, width = 10, image=self.usun_zamowienie_icon, compound="left")
        self.dodaj_button.pack(side='top', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

    def button_refresh_zamowienia(self, frame):
        self.dodaj_button = ttk.Button(frame, text="Odśwież", command=self.load_zamowienia_daemon, width = 10, image=self.refresh_element_icon, compound="left")
        self.dodaj_button.pack(side='bottom', padx=1, pady=3)
        ToolTip(self.dodaj_button, msg="Hover info", follow=True)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.geometry("1280x720+0+0")
    app = FolderApp(root)
    root.mainloop()



# comments for next project status
# dane["button_usun_firma]['text']
