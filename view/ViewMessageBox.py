from tkinter import ttk, messagebox, simpledialog
import tkinter as tk

    
class ViewMessageBox():
    def show_message_async(self, master, leksykon):
        def pokaz_okno(master):
            self.msg_windows = tk.Toplevel(master)
            self.msg_windows.geometry("300x50+340+160")
            self.msg_windows.title(leksykon["info_initializing"]["heading"])

            label = tk.Label(self.msg_windows, text=leksykon["info_initializing"]["text"], padx=20, pady=10)
            label.pack()

        master.after(0, pokaz_okno(master))

    def ukryj_message_async(self, master):
        def zamknij_okno():
            if hasattr(self, 'msg_windows') and self.msg_windows.winfo_exists():
                self.msg_windows.destroy()

        master.after(0, zamknij_okno)


    def messagebox(self, type, language_code = None, heading = None, text = None, value = None):
        if type == "error" or type == "language" and language_code:
            self.sound.play_error_sound()
            return messagebox.showerror(heading, text)
        elif type == "info":
            self.sound.play_info_sound()
            return messagebox.showinfo(heading, text)
        elif type == "close":
            self.sound.play_info_sound()
            return messagebox.askokcancel(heading, text)
        elif type == "ask":
            self.sound.play_info_sound()
            return simpledialog.askstring(heading, text, initialvalue=value)
