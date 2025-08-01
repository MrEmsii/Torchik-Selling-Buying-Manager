from tkinter import ttk, messagebox, simpledialog, PhotoImage
from TkToolTip import ToolTip
from tkcalendar import DateEntry
from pygame import mixer
import os


class View:
    def __init__(self, master, dsc=None):
        self.master = master
        self.master.title("Torchik Selling-Buying Manager")
        self.master.geometry("1280x720+0+0")
        self.master.resizable(True, True)

        mixer.init()
        
        self.setup_ui_startup(dsc)


    def setup_ui_startup(self, dsc):
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

        self.button_frame = ttk.Frame(self.master, padding=5)

        self.main_frame = ttk.Frame(self.master, padding=5)
        self.zamowienia_frame = ttk.Frame(self.master, padding=5)
        self.secend_frame = ttk.Frame(self.master, padding=5)
        self.third_frame = ttk.Frame(self.master, padding=5)

        self.button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)

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
    
    def button_icon_pack(self):
            self.add_firma_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_firma_icon.png")).subsample(8, 8)
            self.edit_firma_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_firma_icon.png")).subsample(8, 8)
            self.delete_firma_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_firma_icon.png")).subsample(8, 8)
            
            self.add_sklep_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_sklep_icon.png")).subsample(8, 8)
            self.edit_sklep_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_sklep_icon.png")).subsample(8, 8)
            self.delete_sklep_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_sklep_icon.png")).subsample(8, 8)

            self.add_kategoria_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_kategoria_icon.png")).subsample(8, 8)
            self.edit_kategoria_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_kategoria_icon.png")).subsample(8, 8)
            self.delete_kategoria_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_kategoria_icon.png")).subsample(8, 8)
            
            self.add_kupujacy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_kupujacy_icon.png")).subsample(8, 8)
            self.edit_kupujacy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_kupujacy_icon.png")).subsample(8, 8)
            self.delete_kupujacy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_kupujacy_icon.png")).subsample(8, 8)
            
            self.add_artykul_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_artykul_icon.png")).subsample(8, 8)
            self.edit_artykul_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_artykul_icon.png")).subsample(8, 8)
            self.delete_artykul_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_artykul_icon.png")).subsample(8, 8)
            
            self.add_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_zamowienie_icon.png")).subsample(8, 8)
            self.edit_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_zamowienie_icon.png")).subsample(8, 8)
            self.delete_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_zamowienie_icon.png")).subsample(8, 8)
            
            self.add_artykul_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "add_artykul_zamowienie_icon.png")).subsample(8, 8)
            self.edit_artykul_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "edit_artykul_zamowienie_icon.png")).subsample(8, 8)
            self.delete_artykul_zamowienie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "delete_artykul_zamowienie_icon.png")).subsample(8, 8)
            
            self.lista_artykulow_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_artykulow_icon.png")).subsample(8, 8)
            self.lista_kategorie_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_kategorie_icon.png")).subsample(8, 8)
            self.lista_kupujacy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_kupujacy_icon.png")).subsample(8, 8)
            self.lista_zamowien_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_zamowien_icon.png")).subsample(8, 8)
            self.lista_sklepy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_sklepy_icon.png")).subsample(8, 8)
            self.lista_firmy_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "lista_firmy_icon.png")).subsample(8, 8)

            self.backButton_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "backButton_icon.png")).subsample(8, 8)
            self.refresh_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "refresh_icon.png")).subsample(8, 8)
            self.setting_icon = PhotoImage(file=os.path.join(self.dsc, "resources", "image", "setting_icon.png")).subsample(8, 8)

    def utworz_przycisk(self, frame, key, command, side='top', padx=1, pady=3, icon=None):
        leksykon = self.leksykon_programu[key]
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



