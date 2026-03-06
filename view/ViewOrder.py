import addons.customtkinter as ct
from addons.customtkinter import CTkImage

from view.base_view import BaseView

from tkinter import ttk
from PIL import Image, ImageTk
import platform
import os

class ViewOrder(BaseView):
    def __init__(
            self, order_master, 
            dsc=None, 
            leksykon = None, 
            currency=None, 
            language_code = None, 
            konfiguracja_programu = None,
            sound = None,
            style=None
            ):
        
        self.order_master = order_master
        self.order_master.geometry("1280x720+0+0")
        self.order_master.minsize(1280, 720)

        self.leksykon = leksykon
        self.style = style
        self.currency = currency
        self.sound = sound
        self.language_code = language_code
        self.dsc = dsc

        self.setup_styles(self.dsc)
        self.load_icons()
        self.setup_frames()

    def setup_styles(self, dsc):
        self.order_master.title("Torchik - Order Window")
        icon_path = os.path.join(dsc, "resources", "image", "icon.ico")

        def set_icon():
            try:
                if platform.system() == "Windows":
                    self.order_master.wm_iconbitmap(icon_path)
                else:
                    from PIL import Image, ImageTk
                    icon_image = Image.open(icon_path)
                    self.order_icon_photo = ImageTk.PhotoImage(icon_image)
                    self.order_master.wm_iconphoto(True, self.order_icon_photo)
            except Exception as e:
                print(f"Błąd ikony w OrderWindow: {e}")


        for i in range(0, 4):
            self.order_master.grid_rowconfigure(i, weight=4)

        self.order_master.grid_columnconfigure(0, weight=1)
        for i in range(1, 5):
            self.order_master.grid_columnconfigure(i, weight=2000)

        style = ttk.Style()
        # Używamy motywu 'default' lub 'clam' jako bazy, bo są najbardziej elastyczne
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
        self.button_orders_frame = ct.CTkFrame(self.order_master)

        self.realizacja_frame = ct.CTkFrame(self.order_master)
        self.order_frame = ct.CTkFrame(self.order_master)

        self.button_orders_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)

    def load_icons(self):
        """Wczytuje i buforuje wszystkie ikony."""
        img_dir = os.path.join(self.dsc, "resources", "image")
        def load_icon(name): return CTkImage(dark_image=Image.open(os.path.join(img_dir, name)))

        self.category_icon = load_icon("lista_kategorie_icon.png")
        self.buyers_icon = load_icon("lista_kategorie_icon.png")

    def order_grid_setting(self):
        self.realizacja_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.order_frame.grid(row=0, column=2, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def inside_grid_setting(self):
        self.order_frame.grid(row=0, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.realizacja_frame.grid(row=2, column=1, columnspan=5, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def order_tree(self, parent_frame, label_text):
        columns_name = self.leksykon.get("columns", {}).get("order_tree_columns")  # bezpieczne pobranie z leksykonu
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
            # bootstyle="secondary"
        )

        scrollbar.configure(command=tree.yview)
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

        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ct.CTkScrollbar(container, orientation="vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_name,
            show='headings',
            yscrollcommand=scrollbar.set,
            #bootstyle="secondary"
        )
        
        scrollbar.configure(command=tree.yview)
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

        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        # scrollbar = ct.CTkScrollbar(container, orientation= "vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_name,
            show='headings',
            # yscrollcommand=scrollbar.set,
            #bootstyle="secondary"
        )
        
        # scrollbar.configure(command=tree.yview)
        # scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')
        
        tree.heading(columns_name[0], text=columns_name[0], anchor='center')
        tree.column(columns_name[0], width=20, anchor='e')

        tree.heading(columns_name[1], text=columns_name[1], anchor='center')
        tree.column(columns_name[1], width=100, anchor='w')
        tree.pack(expand=status, fill='both')

        return tree 
    
    # def info_tree(self, parent_frame, label_text, status=True):
    #     columns_name = self.leksykon["columns"]["more_info_in_order_columns"]

    #     label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
    #     label.pack(pady=5)

    #     container = ct.CTkFrame(parent_frame)
    #     container.pack(expand=True, fill='both')

    #     scrollbar = ct.CTkScrollbar(container, orientation="vertical")

    #     tree = ttk.Treeview(
    #         container,
    #         columns=columns_name,
    #         show='headings',
    #         yscrollcommand=scrollbar.set,
    #         bootstyle="secondary"
    #     )
        
    #     scrollbar.configure(command=tree.yview)
    #     scrollbar.pack(side='right', fill='y')

    #     tree.pack( expand=True, fill='both')
        
    #     tree.heading(columns_name[0], text=columns_name[0]+ 5*" ", anchor='e')
    #     tree.column(columns_name[0], width=100, anchor='e')

    #     tree.heading(columns_name[1], text=5*" " + columns_name[1], anchor='w')
    #     tree.column(columns_name[1], width=100, anchor='w')
    #     tree.pack(expand=status, fill='both')

    #     return tree 


    def info_tree(self, parent_frame, label_text, status=True):
        label = ct.CTkLabel(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ct.CTkFrame(parent_frame)
        container.pack(expand=True, fill='both')

        table = CanvasTable(container)
        return table


class CanvasTable:
    def __init__(self, parent, row_pad=0):
        self.canvas = ct.CTkCanvas(parent, highlightthickness=0)
        self.frame = ct.CTkFrame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # proporcje kolumn
        self.col1_ratio = 0.2
        self.min_col1 = 100
        self.min_col2 = 160

        self.value_labels = []
        self.row_pad = row_pad
        self.row = 0

        # scrollbar
        # self.scrollbar = ct.CTkScrollbar(
        #     parent, orientation="vertical", command=self.canvas.yview
        # )
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(expand=True, fill="both")

        # resize i scroll
        self.canvas.bind("<Configure>", self._on_resize)
        # self.canvas.bind("<Enter>", self._bind_mousewheel)
        # self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # # aktualizacja scrollregion
        # self.frame.bind(
        #     "<Configure>",
        #     lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # )

    # ---------- RESIZE ----------
    def _on_resize(self, event):
        if event.width <= 1:
            return

        total_w = event.width
        self.canvas.itemconfigure(self.window, width=total_w)

        col1 = max(int(total_w * self.col1_ratio), self.min_col1)
        col2 = max(total_w - col1 - 20, self.min_col2)

        self.frame.grid_columnconfigure(0, minsize=col1)
        self.frame.grid_columnconfigure(1, minsize=col2)

        for v in self.value_labels:
            v.configure(wraplength=col2-300)

    # ---------- API ----------
    def clear(self):
        for w in self.frame.winfo_children():
            w.destroy()
        self.value_labels.clear()
        self.row = 0

    def insert_row(self, label, value):
        l = ct.CTkLabel(
            self.frame,
            text=label,
            anchor="e",
            justify="right"
        )
        l.grid(row=self.row, column=0, sticky="ne", padx=(2, 10), pady=self.row_pad)

        v = ct.CTkLabel(
            self.frame,
            text=value,
            anchor="w",
            justify="left"
        )
        v.grid(row=self.row, column=1, sticky="nw", padx=(0, 60), pady=self.row_pad)

        self.value_labels.append(v)
        self.row += 1

        # wymuszenie poprawnego wraplength po dodaniu
        self.canvas.after_idle(lambda: self._on_resize(
            type("E", (), {"width": self.canvas.winfo_width()})
        ))

    # ---------- SCROLL ----------
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")
