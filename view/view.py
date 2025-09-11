from tkinter import ttk, messagebox, simpledialog, PhotoImage
import tkinter as tk
import datetime

from TkToolTip import ToolTip
from tkcalendar import DateEntry
import os


class View:
    def __init__(self, master, dsc=None):
        self.master = master
        self.master.geometry("1280x720+0+0")
        self.master.resizable(True, True)

        self.button_icon_pack(dsc)
        self.setup_styles(dsc)
        self.setup_frames()

    def setup_frames(self):
        self.button_frame = ttk.Frame(self.master, padding=5)

        self.main_frame = ttk.Frame(self.master, padding=5)
        self.zamowienia_frame = ttk.Frame(self.master, padding=5)
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

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

    def messagebox(self, type, language_code = None, heading = None, text = None, value = None):
        if type == "error" or type == "language" and language_code:
            return messagebox.showerror(heading, text)
        elif type == "info":
            return messagebox.showinfo(heading, text)
        elif type == "close":
            return messagebox.askokcancel(heading, text)
        elif type == "ask":
            return simpledialog.askstring(heading, text, initialvalue=value)

    def zamowienia_grid_setting(self):
        self.zamowienia_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", padx=5, pady=5)

    def artukuly_list_grid_setting(self):
        self.main_frame.grid(row=0, column=1, columnspan=1, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=0, column=2, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
    
    def start_grid_setting(self):
        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

    def inside_tree(self, parent_frame, label_text, columns_names):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_names, 
            show='headings',
            yscrollcommand=scrollbar.set
            )
        
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.pack( expand=True, fill='both')

        tree.column('id_artykul', width=50, anchor='e')
        tree.heading('id_artykul', text='ID:', anchor='e')

        tree.column(columns_names[1], width=100, anchor='e')
        tree.heading(columns_names[1], text=columns_names[1], anchor='e')

        tree.column(columns_names[2], width=100, anchor='e')
        tree.heading(columns_names[2], text=columns_names[2], anchor='e')

        tree.column(columns_names[3], width=100, anchor='e')
        tree.heading(columns_names[3], text=columns_names[3], anchor='e')

        tree.column(columns_names[4], width=100, anchor='e')
        tree.heading(columns_names[4], text=columns_names[4], anchor='e')

        tree.column(columns_names[5], width=100, anchor='e')
        tree.heading(columns_names[5], text=columns_names[5], anchor='e')     

        tree.column(columns_names[6], width=100, anchor='e')
        tree.heading(columns_names[6], text=columns_names[6], anchor='e')   

        tree.column(columns_names[7], width=300, anchor='e')
        tree.heading(columns_names[7], text=columns_names[7], anchor='e')

        tree.pack(expand=True, fill='both')

        return tree  

    def artykuly_tree(self, parent_frame, label_text, columns_names):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_names,
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
       
        return tree       

    def name_tree(self, parent_frame, label_text, status, columns_names):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container, 
            columns=columns_names, 
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

    def zamowienie_tree(self, parent_frame, label_text, columns_names):
        label = ttk.Label(parent_frame, text=label_text, font=("Arial", 12))
        label.pack(pady=5)

        container = ttk.Frame(parent_frame)
        container.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(container, orient="vertical")

        tree = ttk.Treeview(
            container,
            columns=columns_names,
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
            
            self.lista_firmy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_firmy_icon.png")).subsample(8, 8)
            self.lista_sklepy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_sklepy_icon.png")).subsample(8, 8)
            self.lista_zamowien_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_zamowien_icon.png")).subsample(8, 8)
            self.lista_kupujacy_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
            self.lista_kategorie_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
            self.lista_artykulow_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "lista_artykulow_icon.png")).subsample(8, 8)

            self.refresh_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "refresh_icon.png")).subsample(8, 8)
            self.setting_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "setting_icon.png")).subsample(8, 8)
            self.backButton_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "backButton_icon.png")).subsample(8, 8)

    def utworz_przycisk(self, frame, command, side='top', padx=1, pady=3, icon=None, leksykon_programu=None):
        przycisk = ttk.Button(
            frame,
            text=leksykon_programu["text"],
            command=command,
            width=10,
            image=icon or self.refresh_icon,
            compound="left"
        )
        przycisk.pack(side=side, padx=padx, pady=pady)
        ToolTip(przycisk, msg=leksykon_programu["toolTip"], follow=True)
        return przycisk

    def dodaj_modyfikuj_zamowienie_view(self, zamowienie_rabat_j=0, zamowienie_rabat_procentowy=0):
        self.rabat_j_var = tk.DoubleVar(value=zamowienie_rabat_j)
        self.rabat_p_var = tk.DoubleVar(value=zamowienie_rabat_procentowy)
        self.zamowienie_data = tk.StringVar()
        self.zamowienie_view()

    def dodaj_modyfikuj_artykul_view(self, nazwa_artykulu_string = None, kolor_artykulu_string = None, szczegoly_artykulu_string = None):
        self.nazwa_artykulu_string = tk.StringVar(value=nazwa_artykulu_string)
        self.kolor_artykulu_string = tk.StringVar(value=kolor_artykulu_string)
        self.szczegoly_artykulu_string = tk.StringVar(value=szczegoly_artykulu_string)
        self.artykul_view()

    def artykuly_lista_view(self):
        self.secend_frame = ttk.Frame(self.master, padding=5)
        
    def artykul_view(self):
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        nazwa_label = ttk.Label(self.third_frame, text = 'Nazwa artykułu:', font=('calibre', 10, 'bold'), anchor='center')
        kolor_label = ttk.Label(self.third_frame, text = 'Ewentualny kolor:', font=('calibre', 10, 'bold'), anchor='center')
        szczegoly_label = ttk.Label(self.third_frame, text = 'Ewentualne szczegoły:', font=('calibre', 10, 'bold'), anchor='w')

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

        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=2, column=1, columnspan=5, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def zamowienie_view(self):
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        date_label = ttk.Label(self.third_frame, text = 'Data:', font=('calibre', 10, 'bold'), anchor='w')
       
        rabat_j_label = ttk.Label(self.third_frame, text = 'Rabat jednostkowy:', font=('calibre', 10, 'bold'), anchor='w')
        rabat_p_label = ttk.Label(self.third_frame, text = 'Rabat procentowy:', font=('calibre',10, 'bold'), anchor='w')

        rabat_j_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_j_var, font=('calibre',10,'normal'), width=10)
        rabat_p_entry = ttk.Entry(self.third_frame, textvariable = self.rabat_p_var, font=('calibre',10,'normal'), width=10)

        self.date_entry = DateEntry(self.third_frame, localestr='pl_PL', date_pattern="yyyy-mm-dd", textvariable=self.zamowienie_data, width=10, set_date=datetime.date(2023,4,2))

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

        self.date_entry.grid(row=1,column=1)
        rabat_j_entry.grid(row=2,column=1)
        rabat_p_entry.grid(row=3,column=1)

        self.main_frame.grid(row=0, column=1, columnspan=5, rowspan=1, sticky="nsew", padx=5, pady=5)
        self.secend_frame.grid(row=1, column=1, columnspan=5, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.third_frame.grid(row=0, column=6, columnspan=1, rowspan=4, sticky="nsew", padx=5, pady=5)
        
    def cena_ilosc_view(self, cena_artykulu_var = 0, ilosc_artykulu_var = 1):
        self.cena_artykulu_var_old = cena_artykulu_var
        self.ilosc_artykulu_var_old = ilosc_artykulu_var

        self.button_cena_ilosc_frame = ttk.Frame(self.window, padding=5)
        self.filament_frame = ttk.Frame(self.window, padding=5)

        self.button_cena_ilosc_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.filament_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        cena_label = ttk.Label(self.filament_frame, text = 'Cena:', font=('calibre', 10, 'bold'), anchor='center')
        waluta_label = ttk.Label(self.filament_frame, text = 'PLN', font=('calibre', 10, 'bold'), anchor='e')
        ilosc_label = ttk.Label(self.filament_frame, text = 'Ilość:', font=('calibre', 10, 'bold'), anchor='w')
        
        self.cena_artykulu_var = tk.StringVar(value=cena_artykulu_var)
        self.ilosc_artykulu_var = tk.StringVar(value=ilosc_artykulu_var)

        cena_entry = ttk.Entry(self.filament_frame, textvariable = self.cena_artykulu_var, font=('calibre',10,'normal'), width=15)
        ilosc_entry = ttk.Entry(self.filament_frame, textvariable = self.ilosc_artykulu_var, font=('calibre',10,'normal'), width=15)

        cena_label.grid(row=1, column=1)
        ilosc_label.grid(row=2, column=1)

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
        self.window = tk.Toplevel(self.master)
        self.window.geometry("400x180+500+300")
        self.window.title(title)

        self.window.iconbitmap(os.path.join(dsc, "resources", "image", "icon.ico"))
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.id_artykulu = id

        self.cena_ilosc_view(cena_artykulu_var=cena, ilosc_artykulu_var=relacja)

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
