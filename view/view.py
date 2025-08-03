from tkinter import ttk, messagebox, simpledialog, PhotoImage
import tkinter as tk
import datetime

from TkToolTip import ToolTip
from tkcalendar import DateEntry
import os


class View:
    def __init__(self, master, dsc=None):
        self.master = master
        self.master.title("Torchik Selling-Buying Manager")
        self.master.geometry("1280x720+0+0")
        self.master.resizable(True, True)

        self.button_icon_pack(dsc)
        self.setup_styles(dsc)
        self.setup_frames()

    def setup_frames(self):
        self.button_frame = ttk.Frame(self.master, padding=5)

        self.main_frame = ttk.Frame(self.master, padding=5)
        self.zamowienia_frame = ttk.Frame(self.master, padding=5)
        # self.secend_frame = ttk.Frame(self.master, padding=5)
        # self.third_frame = ttk.Frame(self.master, padding=5)

        self.button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)


    def setup_styles(self, dsc):
        self.style = ttk.Style()
        self.master.tk.call('source', dsc + '/resources/themes/awdark.tcl')

        self.style.theme_use("awdark")
        self.style.configure("Treeview", background="#D8E8E8", foreground="#2F3131", rowheight=20, fieldbackground="#E7E7E7", font=('Arial', 8))
        self.style.map("Treeview", background=[('selected', "#2F3131")], foreground=[('selected', '#D8E8E8')])

        self.master.title("Torchik")
        self.master.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))

        self.style.configure('TButton', justify="left", anchor='w')
        self.background_image = PhotoImage(file=os.path.join(dsc, "resources", "image", "background.png"))
        self.background_label = ttk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.master.grid_rowconfigure(0, weight=4)
        self.master.grid_rowconfigure(1, weight=4)
        self.master.grid_rowconfigure(2, weight=4)
        self.master.grid_rowconfigure(3, weight=4)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=2000)
        self.master.grid_columnconfigure(2, weight=2000)
        self.master.grid_columnconfigure(3, weight=2000)

    def messagebox(self, type, language_code = None):
        if type == "error":
            messagebox.showerror("Błąd", "Wystąpił błąd. Proszę spróbować ponownie.")
        elif type == "info":
            messagebox.showinfo("Informacja", "Operacja zakończona pomyślnie.")
        elif type == "warning":
            messagebox.showwarning("Ostrzeżenie", "Proszę sprawdzić wprowadzone dane.")
        elif type == "language" and language_code:
            messagebox.showerror("Błąd", f"Plik językowy '{language_code}.json' nie został znaleziony.")
        elif type == "close":
            return messagebox.askokcancel("Zamknij", "Czy na pewno chcesz zamknąć aplikację?")

    def zamowienia_grid_setting(self):
        self.zamowienia_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)


    def inside_tree(self, parent_frame, label_text):
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

        tree.pack( expand=True, fill='both')

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

    def artykuly_tree(self, parent_frame, label_text):
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

        tree.pack( expand=True, fill='both')

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

    def name_tree(self, parent_frame, label_text, status):
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

        tree.pack( expand=True, fill='both')
        
        tree.column('id', width=10, anchor='e')
        tree.heading('id', text='ID', anchor='e')

        tree.column('name', width=100, anchor='w')
        tree.heading('name', text='Nazwa', anchor='w')
        tree.pack(expand=status, fill='both')

        return tree  

    def zamowienie_tree(self, parent_frame, label_text):
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

        tree.pack( expand=True, fill='both')

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
            
            self.lista_artykulow_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_artykulow_icon.png")).subsample(8, 8)
            self.lista_kategorie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
            self.lista_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
            self.lista_zamowien_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_zamowien_icon.png")).subsample(8, 8)
            self.lista_sklepy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_sklepy_icon.png")).subsample(8, 8)
            self.lista_firmy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_firmy_icon.png")).subsample(8, 8)

            self.backButton_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "backButton_icon.png")).subsample(8, 8)
            self.refresh_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "refresh_icon.png")).subsample(8, 8)
            self.setting_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "setting_icon.png")).subsample(8, 8)

    def utworz_przycisk(self, frame, command, side='top', padx=1, pady=3, icon=None, leksykon_programu=None):
        leksykon = leksykon_programu
        przycisk = ttk.Button(
            frame,
            text=leksykon["text"],
            command=command,
            width=10,
            image=icon or self.refresh_icon,
            compound="left"
        )
        przycisk.pack(side=side, padx=padx, pady=pady)
        ToolTip(przycisk, msg=leksykon["toolTip"], follow=True)
        return przycisk

    def dodaj_zamowienie_view(self):
        self.rabat_j_var = tk.DoubleVar()
        self.rabat_p_var = tk.DoubleVar()
        self.zamowienie_data = tk.StringVar()
        self.zamowienie_view()

    def modyfikuj_zamowienie_view(self, zamowienie_rabat_j, zamowienie_rabat_procentowy):
        self.rabat_j_var = tk.DoubleVar(value=zamowienie_rabat_j)
        self.rabat_p_var = tk.DoubleVar(value=zamowienie_rabat_procentowy)
        self.zamowienie_view()

    def zamowienie_view(self ):
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.date_label = ttk.Label(self.third_frame, text = 'Data:', font=('calibre', 10, 'bold'), anchor='w')
       
        self.rabat_j_label = ttk.Label(self.third_frame, text = 'Rabat jednostkowy:', font=('calibre', 10, 'bold'), anchor='w')
        self.rabat_p_label = ttk.Label(self.third_frame, text = 'Rabat procentowy:', font=('calibre',10, 'bold'), anchor='w')

        self.rabat_j_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_j_var, font=('calibre',10,'normal'), width=10)
        self.rabat_p_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_p_var, font=('calibre',10,'normal'), width=10)

        self.zamowienie_data = tk.StringVar()

        self.date_entry = DateEntry(self.third_frame, localestr='pl_PL', date_pattern="yyyy-mm-dd", textvariable=self.zamowienie_data, width=10, set_date=datetime.date(2023,4,2))

        self.third_frame.grid_rowconfigure(0, weight=80)
        self.third_frame.grid_rowconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(2, weight=1)
        self.third_frame.grid_rowconfigure(3, weight=1)
        self.third_frame.grid_rowconfigure(4, weight=80)

        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_columnconfigure(1, weight=10)

        self.date_label.grid(row=1,column=0)
        self.rabat_j_label.grid(row=2,column=0)
        self.rabat_p_label.grid(row=3,column=0)

        self.date_entry.grid(row=1,column=1)
        self.rabat_j_entry.grid(row=2,column=1)
        self.rabat_p_entry.grid(row=3,column=1)

        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=1, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=1, column=1, columnspan=5, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        

    def show_message_async(self):
        def pokaz_okno():
            self.msg_windows = tk.Toplevel(self.master)
            self.msg_windows.geometry("300x50+340+160")
            self.msg_windows.title("Inicjalizacja operacji")

            label = tk.Label(self.msg_windows, text="Inicjalizacja operacji, proszę poczekaj", padx=20, pady=10)
            label.pack()

        self.master.after(0, pokaz_okno)

    def ukryj_message_async(self):
        def zamknij_okno():
            if hasattr(self, 'msg_windows') and self.msg_windows.winfo_exists():
                self.msg_windows.destroy()

        self.master.after(0, zamknij_okno)