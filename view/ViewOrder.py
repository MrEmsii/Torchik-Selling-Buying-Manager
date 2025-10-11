import tkinter as tk
from tkinter import ttk, PhotoImage

import os
import sv_ttk

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
        self.order_master.title("Torchik - Order Window")
        self.order_master.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))

        sv_ttk.set_theme("dark")

        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 8))
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
        self.order_master.grid_columnconfigure(2, weight=1000)
        self.order_master.grid_columnconfigure(3, weight=2000)
        self.order_master.grid_columnconfigure(4, weight=2000)

    def setup_frames(self):
        self.button_orders_frame = ttk.Frame(self.order_master, padding=5)

        self.realizacja_frame = ttk.Frame(self.order_master, padding=5)
        self.order_frame = ttk.Frame(self.order_master, padding=5)
        # self.third_frame = ttk.Frame(self.order_master, padding=5)

        self.button_orders_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)

    def button_icon_pack(self, dsc):
        self.category_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
        self.buyers_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)

    def order_grid_setting(self):
        self.realizacja_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.order_frame.grid(row=0, column=2, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)
        # self.order_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)

    def inside_grid_setting(self):
        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=4, sticky="nsew", padx=5, pady=5)
        self.realizacja_frame.grid(row=4, column=1, columnspan=5, rowspan=1, sticky="nsew", padx=5, pady=5)
        
    def order_tree(self, parent_frame, label_text):
        columns_name = self.leksykon["columns"]["order_tree_columns"]
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

        tree.heading(columns_name[0], text=columns_name[0], anchor='center')
        tree.column(columns_name[0], width=40, anchor='e')

        tree.heading(columns_name[1], text=columns_name[1], anchor='center')
        tree.column(columns_name[1], width=120, anchor='w')

        tree.heading(columns_name[2], text=columns_name[2], anchor='center')
        tree.column(columns_name[2], width=90, anchor='w')

        tree.heading(columns_name[3], text=columns_name[3], anchor='center')
        tree.column(columns_name[3], width=90, anchor='w')

        tree.heading(columns_name[4], text=columns_name[4], anchor='center')
        tree.column(columns_name[4], width=80, anchor='e')

        tree.heading(columns_name[5], text=columns_name[5], anchor='center')
        tree.column(columns_name[5], width=120, anchor='e')
   
        tree.heading(columns_name[6], text=columns_name[6], anchor='center')
        tree.column(columns_name[6], width=90, anchor='e')

        tree.heading(columns_name[7], text=columns_name[7], anchor='center')
        tree.column(columns_name[7], width=90, anchor='e')
        return tree 
    
    def inside_tree(self, parent_frame, label_text, status=True):
        columns_name = self.leksykon["columns"]["list_added_to_order_columns"]

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
        
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')
        tree.column(columns_name[0], width=50, anchor='w')

        tree.heading(columns_name[1], text=columns_name[1], anchor='center')
        tree.column(columns_name[1], width=50, anchor='e')

        tree.heading(columns_name[2], text=columns_name[2], anchor='center')
        tree.column(columns_name[2], width=40, anchor='e')

        tree.heading(columns_name[3], text=columns_name[3], anchor='center')
        tree.column(columns_name[3], width=50, anchor='e')

        tree.heading(columns_name[4], text=columns_name[4], anchor='center')
        tree.column(columns_name[4], width=50, anchor='e')

        tree.heading(columns_name[5], text=columns_name[5], anchor='center')
        tree.column(columns_name[5], width=50, anchor='e')

        tree.heading(columns_name[6], text=columns_name[6], anchor='center')     
        tree.column(columns_name[6], width=50, anchor='e')

        tree.heading(columns_name[7], text=columns_name[7], anchor='center')   
        tree.column(columns_name[7], width=50, anchor='e')

        tree.heading(columns_name[8], text=columns_name[8], anchor='center')
        tree.column(columns_name[8], width=50, anchor='e')

        tree.heading(columns_name[9], text=columns_name[9], anchor='center')
        tree.column(columns_name[9], width=50, anchor='e')

        tree.pack(expand=status, fill='both')
        return tree         

    def name_tree(self, parent_frame, label_text, status=True):
        columns_name = self.leksykon["columns"]["realizacja_tree_columns"]

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
        
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')
        tree.column(columns_name[0], width=20, anchor='e')

        tree.heading(columns_name[1], text=columns_name[1], anchor='center')
        tree.column(columns_name[1], width=100, anchor='w')
        tree.pack(expand=status, fill='both')

        return tree 
    
    def info_tree(self, parent_frame, label_text, status=True):
        columns_name = self.leksykon["columns"]["more_info_in_order_columns"]

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
        
        tree.heading(columns_name[0], text=columns_name[0]+ 5*" ", anchor='e')
        tree.column(columns_name[0], width=100, anchor='e')

        tree.heading(columns_name[1], text=5*" " + columns_name[1], anchor='w')
        tree.column(columns_name[1], width=100, anchor='w')
        tree.pack(expand=status, fill='both')

        return tree 