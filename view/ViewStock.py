from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry

import addons.customtkinter as ct
from addons.customtkinter import CTkImage
from PIL import Image, ImageTk

import platform

import datetime
import os

from addons.ctk_date_picker import CTkDatePicker
from view.base_view import BaseView

class ViewStock(BaseView):
    def __init__(
            self, stock_master, 
            dsc=None, 
            leksykon = None, 
            language_code = None, 
            konfiguracja_programu = None,
            sound = None,
            currency = None,
            symbol_first = None
            ):
        
        self.stock_master = stock_master
        self.stock_master.geometry("1280x720+0+0")
        self.stock_master.minsize(1280, 720)
        self.stock_master.resizable(True, True)

        self.leksykon = leksykon
        self.currency = currency
        self.symbol_first = symbol_first

        self.button_icon_pack(dsc)
        self.setup_frames()
        self.setup_styles(dsc)

        self.sound = sound
        self.language_code = language_code

    def setup_styles(self, dsc):
        self.stock_master.title("Torchik - Stock Window")
        self.icon_path = os.path.join(dsc, "resources", "image", "icon.ico")

        def set_icon():
            try:
                if platform.system() == "Windows":
                    self.stock_master.wm_iconbitmap(self.icon_path)
                else:
                    from PIL import Image, ImageTk
                    icon_image = Image.open(self.icon_path)
                    self.stock_icon_photo = ImageTk.PhotoImage(icon_image)
                    self.stock_master.wm_iconphoto(True, self.stock_icon_photo)
            except Exception as e:
                print(f"Błąd ikony w StockWindow: {e}")

        self.stock_master.after(1000, set_icon)

        for i in range(0, 4):
            self.stock_master.grid_rowconfigure(i, weight=4)

        self.stock_master.grid_columnconfigure(0, weight=1)
        for i in range(1, 5):
            self.stock_master.grid_columnconfigure(i, weight=2000)

        style = ttk.Style()

        style.theme_use("classic") 

        # Konfiguracja kolorów pasujących do CustomTkinter (Dark Mode)
        style.configure("Treeview",
            background="#2b2b2b",      # Tło wierszy
            foreground="white",        # Kolor tekstu
            fieldbackground="#2b2b2b", # Tło całego pola
            rowheight=30,              # Wyższe wiersze wyglądają nowocześniej
            borderwidth=0,
            font=("Arial", 10)
        )

        # Styl nagłówków
        style.configure("Treeview.Heading",
            background="#333333", 
            foreground="white", 
            relief="flat",
            font=("Arial", 10, "bold")
        )

        # Zmiana koloru zaznaczenia (Selection)
        style.map("Treeview",
            background=[('selected', '#1f538d')], # Kolor niebieski z CTK
            foreground=[('selected', 'white')]
        )

    def setup_frames(self):
        self.button_stock_frame = ct.CTkFrame(self.stock_master)

        self.stock_frame = ct.CTkFrame(self.stock_master)
        self.zamowienia_frame = ct.CTkFrame(self.stock_master)
        self.secend_frame = ct.CTkFrame(self.stock_master)
        self.third_frame = ct.CTkFrame(self.stock_master)

        self.button_stock_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.stock_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def button_icon_pack(self, dsc):
        self.add_firma_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_firma_icon.png")))
        self.edit_firma_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_firma_icon.png")))
        self.delete_firma_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_firma_icon.png")))
        
        self.add_sklep_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_sklep_icon.png")))
        self.edit_sklep_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_sklep_icon.png")))
        self.delete_sklep_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_sklep_icon.png")))

        self.add_kategoria_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_kategoria_icon.png")))
        self.edit_kategoria_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_kategoria_icon.png")))
        self.delete_kategoria_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_kategoria_icon.png")))
        
        self.add_kupujacy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_kupujacy_icon.png")))
        self.edit_kupujacy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_kupujacy_icon.png")))
        self.delete_kupujacy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_kupujacy_icon.png")))
        
        self.add_artykul_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_artykul_icon.png")))
        self.edit_artykul_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_artykul_icon.png")))
        self.delete_artykul_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_artykul_icon.png")))
        
        self.add_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_zamowienie_icon.png")))
        self.edit_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_zamowienie_icon.png")))
        self.delete_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_zamowienie_icon.png")))
        
        self.add_artykul_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "add_artykul_zamowienie_icon.png")))
        self.edit_artykul_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "edit_artykul_zamowienie_icon.png")))
        self.delete_artykul_zamowienie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "delete_artykul_zamowienie_icon.png")))
        
        self.lista_firmy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_firmy_icon.png")))
        self.lista_sklepy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_sklepy_icon.png")))
        self.lista_zamowien_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_zamowien_icon.png")))
        self.lista_kupujacy_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")))
        self.lista_kategorie_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")))
        self.lista_artykulow_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "lista_artykulow_icon.png")))

        self.backButton_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "backButton_icon.png")))
        self.refresh_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "refresh_icon.png")))
        self.setting_icon = CTkImage(dark_image=Image.open(os.path.join(dsc, "resources", "image", "setting_icon.png")))
        
    def zamowienia_grid_setting(self):
        self.zamowienia_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def artukuly_list_grid_setting(self):
        self.stock_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=0, column=2, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)
    
    def start_grid_setting(self):
        self.stock_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def inside_tree(self, parent_frame, label_text):
        columns_name = self.leksykon["columns"]["inside_tree_columns"]

        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ct.CTkScrollbar(container, orientation="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_name, 
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.configure(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=30, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')

        tree.column(columns_name[1], width=60, anchor='e')
        tree.heading(columns_name[1], text=columns_name[1], anchor='center')

        tree.column(columns_name[2], width=30, anchor='e')
        tree.heading(columns_name[2], text=columns_name[2], anchor='center')

        tree.column(columns_name[3], width=90, anchor='e')
        tree.heading(columns_name[3], text=columns_name[3], anchor='center')

        tree.column(columns_name[4], width=100, anchor='w')
        tree.heading(columns_name[4], text=columns_name[4], anchor='center')

        tree.column(columns_name[5], width=100, anchor='w')
        tree.heading(columns_name[5], text=columns_name[5], anchor='center')

        tree.column(columns_name[6], width=200, anchor='w')
        tree.heading(columns_name[6], text=columns_name[6], anchor='center')     

        tree.column(columns_name[7], width=100, anchor='w')
        tree.heading(columns_name[7], text=columns_name[7], anchor='center')   

        tree.column(columns_name[8], width=300, anchor='w')
        tree.heading(columns_name[8], text=columns_name[8], anchor='center')

        tree.pack(expand=True, fill='both')

        return tree  

    def artykuly_tree(self, parent_frame, label_text):
        columns_name = self.leksykon.get("columns", {}).get("artykuly_tree_columns", [])

        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ct.CTkScrollbar(container, orientation="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.configure(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=10, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')

        tree.column(columns_name[1], width=100, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='center')

        tree.column(columns_name[2], width=50, anchor='w')
        tree.heading(columns_name[2], text=columns_name[2], anchor='center')

        tree.column(columns_name[3], width=150, anchor='w')
        tree.heading(columns_name[3], text=columns_name[3], anchor='center')        

        tree.column(columns_name[4], width=100, anchor='w')
        tree.heading(columns_name[4], text=columns_name[4], anchor='center')

        tree.column(columns_name[5], width=150, anchor='w')
        tree.heading(columns_name[5], text=columns_name[5], anchor='center')
       
        return tree       

    def name_tree(self, parent_frame, label_text, status):
        columns_name = self.leksykon["columns"]["name_tree_columns"]

        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ct.CTkScrollbar(container, orientation="vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.configure(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')
        
        tree.column(columns_name[0], width=10, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')

        tree.column(columns_name[1], width=200, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='center')
        tree.pack(expand=status, fill='both')

        return tree  

    def zamowienie_tree(self, parent_frame, label_text):
        columns_name = self.leksykon.get("columns", {}).get("zamowienia_tree_columns", [])
        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame, border_width=0, fg_color="transparent") 
        container.pack(expand=True, fill='both')

        scrollbar = ct.CTkScrollbar(container, orientation="vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set
        )

        scrollbar.configure(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column(columns_name[0], width=50, anchor='e')
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')

        tree.column(columns_name[1], width=100, anchor='w')
        tree.heading(columns_name[1], text=columns_name[1], anchor='center')

        tree.column(columns_name[2], width=100, anchor='w')
        tree.heading(columns_name[2], text=columns_name[2], anchor='center')

        tree.column(columns_name[3], width=100, anchor='w')
        tree.heading(columns_name[3], text=columns_name[3], anchor='center')

        tree.column(columns_name[4], width=100, anchor='e')
        tree.heading(columns_name[4], text=columns_name[4], anchor='center')        

        tree.column(columns_name[5], width=100, anchor='e')
        tree.heading(columns_name[5], text=columns_name[5], anchor='center')

        tree.column(columns_name[6], width=100, anchor='e')
        tree.heading(columns_name[6], text=columns_name[6], anchor='center')

        tree.column(columns_name[7], width=100, anchor='e')
        tree.heading(columns_name[7], text=columns_name[7], anchor='center')

        tree.column(columns_name[8], width=100, anchor='e')
        tree.heading(columns_name[8], text=columns_name[8], anchor='center')
        return tree    

    def dodaj_modyfikuj_zamowienie_view(self, zamowienie_rabat_j=None, zamowienie_rabat_procentowy=None, faktura_id=""):
        self.rabat_j_var = tk.StringVar(value=zamowienie_rabat_j)
        self.rabat_p_var = tk.StringVar(value=zamowienie_rabat_procentowy)
        self.zamowienie_data = tk.StringVar()
        self.faktura_id = tk.StringVar(value=faktura_id)
        self.zamowienie_view()

    def dodaj_modyfikuj_artykul_view(self, nazwa_artykulu_string = None, kolor_artykulu_string = None, szczegoly_artykulu_string = None):
        self.nazwa_artykulu_string = tk.StringVar(value=nazwa_artykulu_string)
        self.kolor_artykulu_string = tk.StringVar(value=kolor_artykulu_string)
        self.szczegoly_artykulu_string = tk.StringVar(value=szczegoly_artykulu_string)
        self.artykul_view()

    def artykuly_lista_view(self):
        self.secend_frame = ct.CTkFrame(self.stock_master)
        
    def artykul_view(self):
        label_name = self.leksykon.get("labels", {})

        self.secend_frame = ct.CTkFrame(self.stock_master)
        self.third_frame = ct.CTkFrame(self.stock_master)

        nazwa_label = ct.CTkLabel(self.third_frame, text = label_name["name"] + 5*" ", font=('calibre', 10, 'bold'), anchor='center', padx=(12))
        kolor_label = ct.CTkLabel(self.third_frame, text = label_name["color"] + 5*" ", font=('calibre', 10, 'bold'), anchor='center', padx=(12))
        szczegoly_label = ct.CTkLabel(self.third_frame, text = label_name["details"] + 5*" ", font=('calibre', 10, 'bold'), anchor='w', padx=(12))

        nazwa_entry = ct.CTkEntry(self.third_frame, textvariable = self.nazwa_artykulu_string, font=('calibre',10,'normal'), width=250)
        kolor_entry = ct.CTkEntry(self.third_frame, textvariable = self.kolor_artykulu_string, font=('calibre',10,'normal'), width=250)
        szczegoly_entry = ct.CTkEntry(self.third_frame, textvariable = self.szczegoly_artykulu_string, font=('calibre',10,'normal'), width=250)

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

        nazwa_entry.grid(row=1,column=1, sticky='we', padx=5)
        kolor_entry.grid(row=2,column=1, sticky='we', padx=5)
        szczegoly_entry.grid(row=3,column=1, sticky='we', padx=5)

        self.stock_frame.grid(row=0, column=1, columnspan=3, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=2, column=1, columnspan=3, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=4, columnspan=3, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def zamowienie_view(self):
        label_name = self.leksykon.get("labels", {})
        
        self.secend_frame = ct.CTkFrame(self.stock_master)
        self.third_frame = ct.CTkFrame(self.stock_master)

        date_label = ct.CTkLabel(self.third_frame, text = label_name["date"], font=('calibre', 10, 'bold'), anchor='center', padx=(12))
        rabat_j_label = ct.CTkLabel(self.third_frame, text = label_name["unit_discount"], font=('calibre', 10, 'bold'), anchor='center', padx=(12))
        rabat_p_label = ct.CTkLabel(self.third_frame, text = label_name["proc_discount"], font=('calibre',10, 'bold'), anchor='center', padx=(12))
        faktura_id_label = ct.CTkLabel(self.third_frame, text = label_name["invoice_id"], font=('calibre', 10, 'bold'), anchor='center', padx=(12))

        rabat_p_entry = self.create_entry_with_placeholder(self.third_frame, self.rabat_p_var, "0.00", font=('calibre',10,'normal'), width=20)
        if not self.rabat_p_var.get(): rabat_p_entry.configure(placeholder_text="0%")
        
        if self.symbol_first == 1:
            rabat_j_entry = self.create_entry_with_placeholder(self.third_frame, self.rabat_j_var, f"{self.currency} 0.00", font=('calibre',10,'normal'), width=20)
            if not self.rabat_j_var.get(): rabat_j_entry.configure(placeholder_text="0")
        else:
            rabat_j_entry = self.create_entry_with_placeholder(self.third_frame, self.rabat_j_var, f"00.00 {self.currency}", font=('calibre',10,'normal'), width=20)
            if not self.rabat_j_var.get(): rabat_j_entry.configure(placeholder_text="0%")        
        
        faktura_id_entry = self.create_entry_with_placeholder(self.third_frame, self.faktura_id, "FV_0000_00_00/00", font=('calibre',10,'normal'), width=20)
        if not self.faktura_id.get(): rabat_p_entry.configure(placeholder_text="0%")

        self.date_entry = CTkDatePicker(master=self.third_frame)
        self.date_entry.set_date_format("%d/%m/%Y")
        date = datetime.datetime.now()
        self.date_entry.select_date(year=date.year, day=date.day, month=date.month)

        self.third_frame.grid_rowconfigure(0, weight=80)
        self.third_frame.grid_rowconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(2, weight=1)
        self.third_frame.grid_rowconfigure(3, weight=1)
        self.third_frame.grid_rowconfigure(4, weight=1)
        self.third_frame.grid_rowconfigure(5, weight=80)

        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_columnconfigure(1, weight=10)

        date_label.grid(row=1, column=0, sticky='e')
        rabat_j_label.grid(row=2, column=0, sticky='e')
        rabat_p_label.grid(row=3, column=0, sticky='e')
        faktura_id_label.grid(row=4, column=0, sticky='e')

        self.date_entry.grid(row=1, column=1, sticky='we', padx=5)
        rabat_j_entry.grid(row=2, column=1, sticky='we', padx=5)
        rabat_p_entry.grid(row=3, column=1, sticky='we', padx=5)
        faktura_id_entry.grid(row=4, column=1, sticky='we', padx=5)

        self.stock_frame.grid(row=0, column=1, columnspan=3, rowspan=1, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=1, column=1, columnspan=3, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=4, columnspan=2, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def cena_ilosc_view(self, cena_artykulu_var = 0, ilosc_artykulu_var = 1):
        label_name = self.leksykon.get("labels", {})

        self.cena_artykulu_var_old = cena_artykulu_var
        self.ilosc_artykulu_var_old = ilosc_artykulu_var

        self.button_cena_ilosc_frame = ct.CTkFrame(self.window)
        self.filament_frame = ct.CTkFrame(self.window)

        self.button_cena_ilosc_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.filament_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        cena_label = ct.CTkLabel(self.filament_frame, text = label_name["price"], font=('calibre', 10, 'bold'), anchor='center', padx=(12))
        ilosc_label = ct.CTkLabel(self.filament_frame, text = label_name["amount"], font=('calibre', 10, 'bold'), anchor='w', padx=(12))
        
        if self.symbol_first == 1:
            self.cena_artykulu_var = tk.StringVar(value=f'{self.currency} {cena_artykulu_var}')
        else:
            self.cena_artykulu_var = tk.StringVar(value=f'{cena_artykulu_var} {self.currency}')
            
        self.ilosc_artykulu_var = tk.StringVar(value=ilosc_artykulu_var)

        cena_entry = ct.CTkEntry(self.filament_frame, textvariable = self.cena_artykulu_var, font=('calibre',10,'normal'), width=100)

        ilosc_entry = ct.CTkEntry(self.filament_frame, textvariable = self.ilosc_artykulu_var, font=('calibre',10,'normal'), width=100)

        cena_label.grid(row=1, column=1, sticky='e')
        ilosc_label.grid(row=2, column=1, sticky='e')

        cena_entry.grid(row=1, column=2, sticky='we', padx=5)
        ilosc_entry.grid(row=2, column=2, sticky='we', padx=5)

        # waluta_label.grid(row=1, column=3)

        self.window.grid_rowconfigure(0, weight=4)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2000)

        self.filament_frame.grid_rowconfigure(0, weight=80)
        self.filament_frame.grid_rowconfigure(1, weight=1)
        self.filament_frame.grid_rowconfigure(2, weight=1)
        self.filament_frame.grid_rowconfigure(3, weight=80)

    def cena_ilosc_window(self, dsc, title, relacja = 1, cena = 0, id = None):
        self.window = ct.CTkToplevel(self.stock_master)
        self.window.geometry("400x180+500+300")
        self.window.title(title)

        try:
            if platform.system() == "Windows":
                self.stock_master.wm_iconbitmap(self.icon_path)
            else:
                from PIL import Image, ImageTk
                icon_image = Image.open(self.icon_path)
                self.stock_icon_photo = ImageTk.PhotoImage(icon_image)
                self.stock_master.wm_iconphoto(True, self.stock_icon_photo)
        except Exception as e:
            print(f"Błąd ikony w StockWindow: {e}")

        self.id_artykulu = id

        self.cena_ilosc_view(cena_artykulu_var=cena, ilosc_artykulu_var=relacja)

