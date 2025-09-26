import tkinter as tk
from tkinter import ttk, PhotoImage

import os

from view.base_view import BaseView

class ViewOrder(BaseView):
    def __init__(
            self, order_master, 
            dsc=None, 
            leksykon = None, 
            currency=None, 
            language_code = None, 
            konfiguracja_programu = None,
            sound = None
            ):
        
        self.order_master = order_master
        self.order_master.geometry("1280x720+0+0")
        self.order_master.resizable(True, True)

        self.leksykon = leksykon
        self.currency = currency

        self.button_icon_pack(dsc)
        self.setup_frames()
        self.setup_styles(dsc)

        self.sound = sound
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
        self.category_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
        self.buyers_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
        