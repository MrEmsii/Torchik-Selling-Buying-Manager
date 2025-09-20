from tkinter import ttk, PhotoImage
import tkinter as tk
from tkcalendar import DateEntry

import datetime
import os

from view.ViewSound import ViewSound
from view.base_view import BaseView

class ViewOrder(BaseView):
    def __init__(self, order_master, dsc=None, leksykon = None, language_code = None, konfiguracja_programu = None):
        self.order_master = order_master
        self.order_master.geometry("1280x720+0+0")
        self.order_master.resizable(True, True)

        self.leksykon = leksykon

        self.button_icon_pack(dsc)
        self.setup_frames()
        self.setup_styles(dsc)

        self.sound = ViewSound(dsc, konfiguracja_programu)
        self.language_code = language_code

    def setup_styles(self, dsc):
        self.style = ttk.Style()

        self.style.theme_use("awdark")
        self.style.configure("Treeview", background="#D8E8E8", foreground="#2F3131", rowheight=20, fieldbackground="#E7E7E7", font=('Arial', 8))
        self.style.map("Treeview", background=[('selected', "#2F3131")], foreground=[('selected', '#D8E8E8')])

        self.order_master.title("Torchik - Order Window")
        self.order_master.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))

        self.style.configure('TButton', justify="left", anchor='w')
        self.background_image = PhotoImage(file=os.path.join(dsc, "resources", "image", "background.png"))
        self.background_label = ttk.Label(self.order_master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 
        self.background_label.lower()

        self.order_master.grid_rowconfigure(0, weight=4)
        self.order_master.grid_rowconfigure(1, weight=4)
        self.order_master.grid_rowconfigure(2, weight=4)
        self.order_master.grid_rowconfigure(3, weight=4)

        self.order_master.grid_columnconfigure(0, weight=1)
        self.order_master.grid_columnconfigure(1, weight=2000)
        self.order_master.grid_columnconfigure(2, weight=2000)
        self.order_master.grid_columnconfigure(3, weight=2000)

    def setup_frames(self):
        self.button_orders_frame = ttk.Frame(self.order_master, padding=5)

        self.order_frame = ttk.Frame(self.order_master, padding=5)
        self.zamowienia_frame = ttk.Frame(self.order_master, padding=5)
        self.secend_frame = ttk.Frame(self.order_master, padding=5)
        self.third_frame = ttk.Frame(self.order_master, padding=5)

        self.button_orders_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def button_icon_pack(self, dsc):
            self.add_firma_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_firma_icon.png")).subsample(8, 8)
            self.edit_firma_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_firma_icon.png")).subsample(8, 8)
            self.delete_firma_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_firma_icon.png")).subsample(8, 8)
            
            self.add_sklep_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_sklep_icon.png")).subsample(8, 8)
            self.edit_sklep_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_sklep_icon.png")).subsample(8, 8)
            self.delete_sklep_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_sklep_icon.png")).subsample(8, 8)

            self.add_kategoria_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_kategoria_icon.png")).subsample(8, 8)
            self.edit_kategoria_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_kategoria_icon.png")).subsample(8, 8)
            self.delete_kategoria_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_kategoria_icon.png")).subsample(8, 8)
            
            self.add_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_kupujacy_icon.png")).subsample(8, 8)
            self.edit_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_kupujacy_icon.png")).subsample(8, 8)
            self.delete_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_kupujacy_icon.png")).subsample(8, 8)
            
            self.add_artykul_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_artykul_icon.png")).subsample(8, 8)
            self.edit_artykul_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_artykul_icon.png")).subsample(8, 8)
            self.delete_artykul_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_artykul_icon.png")).subsample(8, 8)
            
            self.add_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_zamowienie_icon.png")).subsample(8, 8)
            self.edit_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_zamowienie_icon.png")).subsample(8, 8)
            self.delete_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_zamowienie_icon.png")).subsample(8, 8)
            
            self.add_artykul_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_artykul_zamowienie_icon.png")).subsample(8, 8)
            self.edit_artykul_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "edit_artykul_zamowienie_icon.png")).subsample(8, 8)
            self.delete_artykul_zamowienie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "delete_artykul_zamowienie_icon.png")).subsample(8, 8)
            
            self.lista_firmy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_firmy_icon.png")).subsample(8, 8)
            self.lista_sklepy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_sklepy_icon.png")).subsample(8, 8)
            self.lista_zamowien_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_zamowien_icon.png")).subsample(8, 8)
            self.lista_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
            self.lista_kategorie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
            self.lista_artykulow_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_artykulow_icon.png")).subsample(8, 8)

            self.backButton_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "backButton_icon.png")).subsample(8, 8)
            self.refresh_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "refresh_icon.png")).subsample(8, 8)
            self.setting_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "setting_icon.png")).subsample(8, 8)
            
    def zamowienia_grid_setting(self):
        self.zamowienia_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)

    def artukuly_list_grid_setting(self):
        self.order_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=0, column=2, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
    
    def start_grid_setting(self):
        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def inside_tree(self, parent_frame, label_text):
        columns_name = self.leksykon["columns"]["inside_tree_columns"]

        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_name, 
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=50, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='e')

        tree.column(columns_name[1], width=100, anchor='e')
        tree.heading(columns_name[1], text=columns_name[1], anchor='e')

        tree.column(columns_name[2], width=100, anchor='e')
        tree.heading(columns_name[2], text=columns_name[2], anchor='e')

        tree.column(columns_name[3], width=100, anchor='e')
        tree.heading(columns_name[3], text=columns_name[3], anchor='e')

        tree.column(columns_name[4], width=100, anchor='e')
        tree.heading(columns_name[4], text=columns_name[4], anchor='e')

        tree.column(columns_name[5], width=100, anchor='e')
        tree.heading(columns_name[5], text=columns_name[5], anchor='e')     

        tree.column(columns_name[6], width=100, anchor='e')
        tree.heading(columns_name[6], text=columns_name[6], anchor='e')   

        tree.column(columns_name[7], width=300, anchor='e')
        tree.heading(columns_name[7], text=columns_name[7], anchor='e')

        tree.pack(expand=True, fill='both')

        return tree  

    def artykuly_tree(self, parent_frame, label_text):
        columns_name = self.leksykon["columns"]["artykuly_tree_columns"]

        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=20, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='e')

        tree.column(columns_name[1], width=50, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='w')

        tree.column(columns_name[2], width=50, anchor='w')
        tree.heading(columns_name[2], text=columns_name[2], anchor='w')

        tree.column(columns_name[3], width=100, anchor='w')
        tree.heading(columns_name[3], text=columns_name[3], anchor='w')        

        tree.column(columns_name[4], width=100, anchor='w')
        tree.heading(columns_name[4], text=columns_name[4], anchor='w')

        tree.column(columns_name[5], width=100, anchor='w')
        tree.heading(columns_name[5], text=columns_name[5], anchor='w')
       
        return tree       

    def name_tree(self, parent_frame, label_text, status):
        columns_name = self.leksykon["columns"]["name_tree_columns"]

        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_name, 
            show='headings', 
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')
        
        tree.column(columns_name[0], width=10, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='e')

        tree.column(columns_name[1], width=100, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='w')
        tree.pack(expand=status, fill='both')

        return tree  

    def zamowienie_tree(self, parent_frame, label_text):
        columns_name = self.leksykon["columns"]["zamowienia_tree_columns"]
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set,
        )

        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=50, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='e')

        tree.column(columns_name[1], width=100, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='w')

        tree.column(columns_name[2], width=100, anchor='w')
        tree.heading(columns_name[2], text=columns_name[2], anchor='w')

        tree.column(columns_name[3], width=100, anchor='w')
        tree.heading(columns_name[3], text=columns_name[3], anchor='w')

        tree.column(columns_name[4], width=100, anchor='e')
        tree.heading(columns_name[4], text=columns_name[4], anchor='e')        

        tree.column(columns_name[5], width=100, anchor='e')
        tree.heading(columns_name[5], text=columns_name[5], anchor='e')

        tree.column(columns_name[6], width=100, anchor='e')
        tree.heading(columns_name[6], text=columns_name[6], anchor='e')

        tree.column(columns_name[7], width=100, anchor='e')
        tree.heading(columns_name[7], text=columns_name[7], anchor='e')

        return tree    

    def dodaj_modyfikuj_zamowienie_view(self, zamowienie_rabat_j=0, zamowienie_rabat_procentowy=0):
        self.rabat_j_var = tk.StringVar(value=zamowienie_rabat_j)
        self.rabat_p_var = tk.StringVar(value=zamowienie_rabat_procentowy)
        self.zamowienie_data = tk.StringVar()
        self.zamowienie_view()

    def dodaj_modyfikuj_artykul_view(self, nazwa_artykulu_string = None, kolor_artykulu_string = None, szczegoly_artykulu_string = None):
        self.nazwa_artykulu_string = tk.StringVar(value=nazwa_artykulu_string)
        self.kolor_artykulu_string = tk.StringVar(value=kolor_artykulu_string)
        self.szczegoly_artykulu_string = tk.StringVar(value=szczegoly_artykulu_string)
        self.artykul_view()

    def artykuly_lista_view(self):
        self.secend_frame = ttk.Frame(self.order_master, padding=5)
        
    def artykul_view(self):
        label_name = self.leksykon["labels"]

        self.secend_frame = ttk.Frame(self.order_master, padding=5)
        self.third_frame = ttk.Frame(self.order_master, padding=5)

        nazwa_label = ttk.Label(self.third_frame, text = label_name["name"], font=('calibre', 10, 'bold'), anchor='center')
        kolor_label = ttk.Label(self.third_frame, text = label_name["color"], font=('calibre', 10, 'bold'), anchor='center')
        szczegoly_label = ttk.Label(self.third_frame, text = label_name["details"], font=('calibre', 10, 'bold'), anchor='w')

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
        
        nazwa_label.grid(row=1,column=0, sticky='e')
        kolor_label.grid(row=2,column=0, sticky='e')
        szczegoly_label.grid(row=3,column=0, sticky='e')

        nazwa_entry.grid(row=1,column=1)
        kolor_entry.grid(row=2,column=1)
        szczegoly_entry.grid(row=3,column=1)

        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=2, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def zamowienie_view(self):
        label_name = self.leksykon["labels"]
        
        self.secend_frame = ttk.Frame(self.order_master, padding=5)
        self.third_frame = ttk.Frame(self.order_master, padding=5)

        date_label = ttk.Label(self.third_frame, text = label_name["date"], font=('calibre', 10, 'bold'), anchor='center')
       
        rabat_j_label = ttk.Label(self.third_frame, text = label_name["unit_discount"], font=('calibre', 10, 'bold'), anchor='center')
        rabat_p_label = ttk.Label(self.third_frame, text = label_name["proc_discount"], font=('calibre',10, 'bold'), anchor='center')

        rabat_j_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_j_var, font=('calibre',10,'normal'), width=10)
        rabat_p_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_p_var, font=('calibre',10,'normal'), width=10)

        self.date_entry = DateEntry(self.third_frame, localestr=self.language_code, date_pattern="yyyy-mm-dd", textvariable=self.zamowienie_data, width=10, set_date=datetime.date(2023,4,2))

        self.third_frame.grid_rowconfigure(0, weight=80)
        self.third_frame.grid_rowconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(2, weight=1)
        self.third_frame.grid_rowconfigure(3, weight=1)
        self.third_frame.grid_rowconfigure(4, weight=80)

        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_columnconfigure(1, weight=10)

        date_label.grid(row=1,column=0, sticky='e')
        rabat_j_label.grid(row=2,column=0, sticky='e')
        rabat_p_label.grid(row=3,column=0, sticky='e')

        self.date_entry.grid(row=1,column=1)
        rabat_j_entry.grid(row=2,column=1)
        rabat_p_entry.grid(row=3,column=1)

        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=1, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=1, column=1, columnspan=5, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def cena_ilosc_view(self, cena_artykulu_var = 0, ilosc_artykulu_var = 1):
        label_name = self.leksykon["labels"]
        currency = self.leksykon["currency"]

        self.cena_artykulu_var_old = cena_artykulu_var
        self.ilosc_artykulu_var_old = ilosc_artykulu_var

        self.button_cena_ilosc_frame = ttk.Frame(self.window, padding=5)
        self.filament_frame = ttk.Frame(self.window, padding=5)

        self.button_cena_ilosc_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.filament_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        cena_label = ttk.Label(self.filament_frame, text = label_name["price"], font=('calibre', 10, 'bold'), anchor='center')
        waluta_label = ttk.Label(self.filament_frame, text = currency, font=('calibre', 10, 'bold'), anchor='e')
        ilosc_label = ttk.Label(self.filament_frame, text = label_name["amount"], font=('calibre', 10, 'bold'), anchor='w')
        
        self.cena_artykulu_var = tk.StringVar(value=cena_artykulu_var)
        self.ilosc_artykulu_var = tk.StringVar(value=ilosc_artykulu_var)

        cena_entry = ttk.Entry(self.filament_frame, textvariable = self.cena_artykulu_var, font=('calibre',10,'normal'), width=15)
        ilosc_entry = ttk.Entry(self.filament_frame, textvariable = self.ilosc_artykulu_var, font=('calibre',10,'normal'), width=15)

        cena_label.grid(row=1, column=1, sticky='e')
        ilosc_label.grid(row=2, column=1, sticky='e')

        cena_entry.grid(row=1, column=2)
        ilosc_entry.grid(row=2, column=2)

        waluta_label.grid(row=1, column=3)

        self.window.grid_rowconfigure(0, weight=4)
        self.window.grid_rowconfigure(1, weight=4)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2000)

        self.filament_frame.grid_rowconfigure(0, weight=80)
        self.filament_frame.grid_rowconfigure(1, weight=1)
        self.filament_frame.grid_rowconfigure(2, weight=1)
        self.filament_frame.grid_rowconfigure(3, weight=80)

    def cena_ilosc_window(self, dsc, title, relacja = 1, cena = 0, id = None):
        self.window = tk.Toplevel(self.order_master)
        self.window.geometry("400x180+500+300")
        self.window.title(title)

        self.window.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.id_artykulu = id

        self.cena_ilosc_view(cena_artykulu_var=cena, ilosc_artykulu_var=relacja)

