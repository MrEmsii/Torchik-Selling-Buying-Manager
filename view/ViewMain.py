import customtkinter as ct
from customtkinter import CTkImage

from view.base_view import BaseView

from PIL import Image, ImageTk
import os

import platform

class ViewMain(BaseView):
    def __init__(self, master, dsc=None, sound=None):
        super().__init__(sound)
        self.master = master
        self.dsc = dsc
        self.sound = sound

        self.setup_window()
        self.setup_background()
        self.setup_frames()
        self.load_icons()

        if self.sound:
            self.sound.play_start_sound()

    def setup_window(self):
            self.master.geometry("600x400+300+300")
            self.master.resizable(True, True)
            self.master.title("Torchik")
            
            icon_path = os.path.join(self.dsc, "resources", "image", "icon.ico")
            
            try:
                if platform.system() == "Windows":
                    self.master.iconbitmap(icon_path)
                else:
                    icon_image = Image.open(icon_path)
                    self.icon_photo = ImageTk.PhotoImage(icon_image)
                    self.master.wm_iconphoto(True, self.icon_photo)
            except Exception as e:
                print(f"Błąd ładowania ikony: {e}")

    def setup_background(self):
        bg_path = os.path.join(self.dsc, "resources", "image", "background.png")
        self.background_image = CTkImage(
            dark_image=Image.open(bg_path),
            size=(600, 400)
        )
        self.background_label = ct.CTkLabel(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def setup_frames(self):
        self.main_view_frame = ct.CTkFrame(self.master)
        self.main_view_frame.grid(row=0, column=0, padx=5, pady=5)

    def load_icons(self):
        """Wczytuje i buforuje wszystkie ikony."""
        img_dir = os.path.join(self.dsc, "resources", "image")
        def load_icon(name): return CTkImage(dark_image=Image.open(os.path.join(img_dir, name)))

        self.order_button_icon = load_icon("add_firma_icon.png")
        self.refresh_button_icon = load_icon("refresh_icon.png")
        self.settings_button_icon = load_icon("setting_icon.png")
        self.exit_button_icon = load_icon("setting_icon.png")
        self.statistics_button_icon = load_icon("setting_icon.png")

