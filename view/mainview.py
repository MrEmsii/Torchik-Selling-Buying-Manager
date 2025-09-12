from tkinter import ttk, messagebox, simpledialog, PhotoImage
import tkinter as tk

from view.soundview import SoundView

import os

class MainView:
    def __init__(self, master, dsc=None, leksykon = None, konfiguracja_programu = None):
        self.master = master
        self.master.geometry("1280x720+0+0")
        self.master.resizable(True, True)

        self.leksykon = leksykon

        self.button_icon_pack(dsc)
        self.setup_styles(dsc)
        self.setup_frames()

        self.sound = SoundView(dsc, konfiguracja_programu)
        self.sound.play_start_sound()
