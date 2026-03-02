from tkinter import ttk
from PIL import Image
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import addons.customtkinter as ct
from addons.customtkinter import CTkImage

from view.base_view import BaseView

import platform

DARK_BG = "#2B2B2B"
LIGHT_FG = "white"

COLOR_PALETTE = ["#4F8DD6", "#D67F4F", "#4FD69F", "#D64FD6", "#F2C94C", "#56CCF2", "#BB6BD9"]

class ViewStatistic(BaseView):
    def __init__(
            self, statistic_master, 
            dsc=None, 
            leksykon = None, 
            language_code = None, 
            konfiguracja_programu = None,
            sound = None
            ):
        
        self.dsc = dsc
        self.statistic_master = statistic_master
        self.statistic_master.geometry("1280x720+0+0")
        self.statistic_master.resizable(True, True)

        self.leksykon = leksykon

        self.load_icons()
        self.setup_frames()
        self.setup_styles(self.dsc)

        self.sound = sound
        self.language_code = language_code

        self.scrollbar = ct.CTkScrollbar(self.table_frame, orientation="vertical")

        self.tree = ttk.Treeview(self.table_frame, columns=("name", "value"), show="headings", yscrollcommand=self.scrollbar.set)
        
        self.tree.heading("name", text=leksykon["heading"]["name"])
        self.tree.heading("value", text=leksykon["heading"]["value"])

        self.scrollbar.configure(command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.tree.pack(fill="both", expand=True)

        fig = Figure(figsize=(9, 6), facecolor="#2B2B2B")

        fig.text(0.5, 0.5, leksykon["charts"]["no_data"], ha="center", va="center", fontsize=14, color="white")

        canvas = FigureCanvasTkAgg(fig, master=self.statistic_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def setup_styles(self, dsc):
        self.statistic_master.title("Torchik - Statistics Window")
        icon_path = os.path.join(dsc, "resources", "image", "icon.ico")

        def set_icon():
            try:
                if platform.system() == "Windows":
                    self.statistic_master.wm_iconbitmap(icon_path)
                else:
                    from PIL import Image, ImageTk
                    icon_image = Image.open(icon_path)
                    self.statistic_icon_photo = ImageTk.PhotoImage(icon_image)
                    self.statistic_master.wm_iconphoto(True, self.statistic_icon_photo)
            except Exception as e:
                print(f"Błąd ikony w StatisticsWindow: {e}")

        self.statistic_master.after(1000, set_icon)

        for i in range(0, 4):
            self.statistic_master.grid_rowconfigure(i, weight=4)

        self.statistic_master.grid_columnconfigure(0, weight=1)
        for i in range(1, 5):
            self.statistic_master.grid_columnconfigure(i, weight=2000)

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
        self.button_statistic_frame = ct.CTkFrame(self.statistic_master)

        self.statistic_frame = ct.CTkFrame(self.statistic_master)
        self.table_frame = ct.CTkFrame(self.statistic_master)

        self.button_statistic_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.statistic_frame.grid(row=0, column=1, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.table_frame.grid(row=0, column=3, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)         

    def load_icons(self):
        """Wczytuje i buforuje wszystkie ikony."""
        img_dir = os.path.join(self.dsc, "resources", "image")
        def load_icon(name): return CTkImage(dark_image=Image.open(os.path.join(img_dir, name)))

        self.category_icon = load_icon("lista_kategorie_icon.png")
        self.buyers_icon = load_icon("lista_kupujacy_icon.png")
        self.arts_icon = load_icon("lista_kupujacy_icon.png")
        self.company_icon = load_icon("lista_kupujacy_icon.png")
        self.shops_icon = load_icon("lista_kupujacy_icon.png")

    def update_table(self, headers, data):
        """
        headers = ["Kolumna1", "Kolumna2", ...]
        data = [(val1, val2, ...), (...), ...]
        """
        self.tree["columns"] = headers

        self.scrollbar.configure(command=self.tree.yview)

        self.tree.heading(headers[0], text=headers[0], anchor='center')
        self.tree.column(headers[0], width=60, anchor='e')

        self.tree.heading(headers[1], text=headers[1], anchor='center')
        self.tree.column(headers[1], width=30, anchor='e')

        for row in self.tree.get_children():
            self.tree.delete(row)

        for id, wartosc in data:
            self.tree.insert('', 'end', values=(id, f"{wartosc:,.2f} zł".replace(",", " ")))


    def show_chart(self, labels, values, title="Wykres", master=None):
        for widget in master.winfo_children():
            widget.destroy()

        labels = labels[:20]
        values = values[:20]

        fig = Figure(figsize=(9, 6), facecolor=DARK_BG)
        ax = fig.add_subplot(111, facecolor=DARK_BG)

        ax.barh(labels, values, color=COLOR_PALETTE[:len(values)])

        ax.set_title(title, color=LIGHT_FG)
        ax.tick_params(axis="y", labelsize=8, colors=LIGHT_FG)
        ax.tick_params(axis="x", labelsize=8, colors=LIGHT_FG)
        fig.subplots_adjust(left=0.25)
        ax.invert_yaxis()

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_chart_pie(self, labels, values, title="Wykres", master=None):
        for widget in master.winfo_children():
            widget.destroy()

        labels = labels[:10]
        values = values[:10]

        fig = Figure(figsize=(9, 6), facecolor=DARK_BG)
        ax = fig.add_subplot(111, facecolor=DARK_BG)

        ax.pie(
            values,
            labels=labels,
            startangle=140,
            autopct=self.autopct_format(values),
            textprops={'fontsize': 8, 'color': LIGHT_FG},
            pctdistance=0.75,
            labeldistance=1.1,
            colors=COLOR_PALETTE[:len(values)]
        )
        ax.set_title(title, color=LIGHT_FG)

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def autopct_format(self, values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{:.1f}%\n({v:,d} zł)'.format(pct, v=val).replace(",", " ")
        return my_format