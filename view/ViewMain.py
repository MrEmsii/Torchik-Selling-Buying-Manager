from tkinter import ttk, PhotoImage
from TkToolTip import ToolTip
import tkinter as tk

from view.ViewSound import ViewSound
from view.base_view import BaseView

import os

class ViewMain(BaseView):
    def __init__(self, master, dsc=None, leksykon = None, konfiguracja_programu = None, sound = None, refresh_icon=None):
        self.master = master
        self.master.geometry("500x200+0+0")
        self.master.resizable(True, True)

        self.leksykon = leksykon

        self.setup_styles(dsc)
        self.setup_frames()

        self.sound = ViewSound(dsc, konfiguracja_programu)
        self.sound.play_start_sound()
        self.button_icon_pack_main(dsc)

    def setup_frames(self):
        self.button_main_frame = ttk.Frame(self.master, padding=5)

        self.main_view_frame = ttk.Frame(self.master, padding=5)

        self.button_main_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.main_view_frame.grid(row=0, column=1, columnspan=5, rowspan=5, sticky="nsew", padx=5, pady=5)

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

    def button_icon_pack_main(self, dsc):
        self.order_button_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "add_firma_icon.png")).subsample(8, 8)
        self.refresh_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "refresh_icon.png")).subsample(8, 8)
        self.setting_icon = PhotoImage(file=os.path.join(dsc, "resources", "image", "setting_icon.png")).subsample(8, 8)
        

