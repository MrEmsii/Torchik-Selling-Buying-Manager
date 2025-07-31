from tkinter import ttk, messagebox, simpledialog, PhotoImage
from TkToolTip import ToolTip
from tkcalendar import DateEntry
from pygame import mixer
from tkinterdnd2 import DND_FILES, TkinterDnD


class View:
    def __init__(self):
        master = TkinterDnD.Tk()

        self.master = master
        self.master.title("Torchik Selling-Buying Manager")
        self.master.geometry("1280x720+0+0")
        self.master.resizable(True, True)

        mixer.init()
        
        self.setup_ui()


    def setup_ui(self):
        # Set up the user interface components
        pass  # Implementation of UI setup goes here

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
