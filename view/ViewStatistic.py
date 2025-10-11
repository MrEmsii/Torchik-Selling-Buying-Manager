import tkinter as tk
from tkinter import ttk, PhotoImage

import os

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from view.base_view import BaseView

class ViewStatistic(BaseView):
    def __init__(
            self, statistic_master, 
            dsc=None, 
            leksykon = None, 
            language_code = None, 
            konfiguracja_programu = None,
            sound = None
            ):
        
        self.statistic_master = statistic_master
        self.statistic_master.geometry("1280x720+0+0")
        self.statistic_master.resizable(True, True)

        self.leksykon = leksykon

        self.button_icon_pack(dsc)
        self.setup_frames()
        self.setup_styles(dsc)

        self.sound = sound
        self.language_code = language_code

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")

        self.tree = ttk.Treeview(self.table_frame, columns=("name", "value"), show="headings", yscrollcommand=self.scrollbar.set)
        
        self.tree.heading("name", text=leksykon["heading"]["name"])
        self.tree.heading("value", text=leksykon["heading"]["value"])

        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.tree.pack(fill="both", expand=True)

        fig = Figure(figsize=(9, 6))

        fig.text(0.5, 0.5, leksykon["charts"]["no_data"],
                ha="center", va="center", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.statistic_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def setup_styles(self, dsc):
        self.statistic_master.title("Torchik - Statistic Window")
        icon_path = os.path.join(dsc, "resources", "image", "icon.ico")
        self.statistic_master.after(1000, lambda: self.statistic_master.wm_iconbitmap(icon_path))

        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 8))
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
        self.statistic_master.grid_columnconfigure(2, weight=500)
        self.statistic_master.grid_columnconfigure(3, weight=500)
        self.statistic_master.grid_columnconfigure(4, weight=500)

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
        self.tree["columns"] = headers

        self.scrollbar.config(command=self.tree.yview)

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

        fig = Figure(figsize=(9, 6))
        ax = fig.add_subplot(111)
        ax.barh(labels, values)
        ax.set_title(title)
        ax.tick_params(axis="y", labelsize=8)

        fig.subplots_adjust(left=0.25) 

        ax.invert_yaxis()

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_chart_pie(self, labels, values, title="Wykres", master = None):
        """
        labels = etykiety (np. artykuły)
        values = wartości (np. koszty)
        """
        for widget in master.winfo_children():
            widget.destroy()

        labels = labels[:10]
        values = values[:10]

        fig = Figure(figsize=(9, 6))
        ax = fig.add_subplot(111)

        ax.pie(values, labels=labels, startangle=140, autopct=self.autopct_format(values), textprops={'fontsize': 8}, pctdistance=0.75, labeldistance=1.1)
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def autopct_format(self, values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{:.1f}%\n({v:,d} zł)'.format(pct, v=val).replace(",", " ")
        return my_format