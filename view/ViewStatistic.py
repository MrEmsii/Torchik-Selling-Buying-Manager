import tkinter as tk
from tkinter import ttk, PhotoImage

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from view.base_view import BaseView
from view.ViewSound import ViewSound


class ViewStatistic(BaseView):
    def __init__(self, statistic_master, dsc=None, leksykon = None, language_code = None, konfiguracja_programu = None):
        self.statistic_master = statistic_master
        self.statistic_master.geometry("1280x720+0+0")
        self.statistic_master.resizable(True, True)

        self.leksykon = leksykon

        self.button_icon_pack(dsc)
        self.setup_frames()
        self.setup_styles(dsc)

        self.sound = ViewSound(dsc, konfiguracja_programu)
        self.language_code = language_code

        self.tree = ttk.Treeview(self.table_frame, columns=("name", "value"), show="headings")
        self.tree.heading("name", text="Nazwa")
        self.tree.heading("value", text="Wartość")
        self.tree.pack(fill="both", expand=True)

        # self.master = master
        # self.frame = tk.Frame(master)
        # self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # # zakładki
        # self.notebook = ttk.Notebook(self.frame)
        # self.notebook.pack(fill="both", expand=True)

        # # Tabela
        # self.table_frame = tk.Frame(self.notebook)
        # self.tree = ttk.Treeview(self.table_frame, columns=("name", "value"), show="headings")
        # self.tree.heading("name", text="Nazwa")
        # self.tree.heading("value", text="Wartość")
        # self.tree.pack(fill="both", expand=True)
        # self.notebook.add(self.table_frame, text="Tabela")

        # # Wykres
        # self.chart_frame = tk.Frame(self.notebook)
        # self.notebook.add(self.chart_frame, text="Wykres")

    def setup_styles(self, dsc):
        self.style = ttk.Style()

        self.style.theme_use("awdark")
        self.style.configure("Treeview", background="#D8E8E8", foreground="#2F3131", rowheight=20, fieldbackground="#E7E7E7", font=('Arial', 8))
        self.style.map("Treeview", background=[('selected', "#2F3131")], foreground=[('selected', '#D8E8E8')])

        self.statistic_master.title("Torchik - Statistic Window")
        self.statistic_master.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))

        self.style.configure('TButton', justify="left", anchor='w')
        self.background_image = PhotoImage(file=os.path.join(dsc, "resources", "image", "background.png"))
        self.background_label = ttk.Label(self.statistic_master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 
        self.background_label.lower()

        self.statistic_master.grid_rowconfigure(0, weight=4)
        self.statistic_master.grid_rowconfigure(1, weight=4)
        self.statistic_master.grid_rowconfigure(2, weight=4)
        self.statistic_master.grid_rowconfigure(3, weight=4)

        self.statistic_master.grid_columnconfigure(0, weight=1)
        self.statistic_master.grid_columnconfigure(1, weight=2000)
        self.statistic_master.grid_columnconfigure(2, weight=2000)
        self.statistic_master.grid_columnconfigure(3, weight=2000)
        self.statistic_master.grid_columnconfigure(4, weight=2000)

    def setup_frames(self):
        self.button_statistic_frame = ttk.Frame(self.statistic_master, padding=5)

        self.statistic_frame = ttk.Frame(self.statistic_master, padding=5)
        self.table_frame = ttk.Frame(self.statistic_master, padding=5)

        self.button_statistic_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.statistic_frame.grid(row=0, column=1, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.table_frame.grid(row=0, column=3, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)

    def button_icon_pack(self, dsc):
        self.category_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
        self.buyers_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
        self.arts_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_artykulow_icon.png")).subsample(8, 8)
        self.company_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_firmy_icon.png")).subsample(8, 8)
        self.shops_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_sklepy_icon.png")).subsample(8, 8)
            
    def update_table(self, headers, data):
        """
        headers = ["Kolumna1", "Kolumna2", ...]
        data = [(val1, val2, ...), (...), ...]
        """
        # wyczyść kolumny
        self.tree["columns"] = headers
        for col in headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # usuń stare dane
        for row in self.tree.get_children():
            self.tree.delete(row)

        # dodaj nowe
        # for row in data:
        #     self.tree.insert("", "end", values=row)

        for id, wartosc in data:
            self.tree.insert('', 'end', values=(id, f"{wartosc:,.2f} zł".replace(",", " ")))

    def show_chart(self, labels, values, title="Wykres", master = None):
        """
        labels = etykiety (np. artykuły)
        values = wartości (np. koszty)
        """
        for widget in master.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        # ax.bar(labels, values)
        ax.pie(values, labels=labels, startangle=140, autopct=self.autopct_format(values), textprops={'fontsize': 8}, pctdistance=0.75, labeldistance=1.1)
        ax.set_title(title)
        # ax.set_ylabel("Wartość")

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def autopct_format(self, values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{:.1f}%\n({v:,d} zł)'.format(pct, v=val).replace(",", " ")
        return my_format