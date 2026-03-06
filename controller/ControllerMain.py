import os
import json
# import ttkbootstrap as ttk
# from ttkbootstrap import utility

import addons.customtkinter as ct

from view.ViewSound import ViewSound
from view.ViewMain import ViewMain

from controller.ControllerMessageBox import ControllerMessageBox

# utility.enable_high_dpi_awareness()
ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")


class ControllerMain:
    """Główny kontroler aplikacji Torchik – zarządza oknami i konfiguracją."""

    def __init__(self):
        self.dsc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.master = ct.CTk()
        # self.style = ttk.Style()
        # self.style.theme_use("darkly")

        self.konfiguracja_programu = self.ensure_settings_file()
        self.language_code = self.konfiguracja_programu.get("language_code", "pl_PL")
        self.leksykon_programu = self.load_language(self.language_code)

        self.sound = ViewSound(self.dsc, self.konfiguracja_programu)
        self.messagebox_controller = ControllerMessageBox(sound=self.sound)
        self.messagebox_controller.leksykon_messagebox = self.leksykon_programu["messagebox_window"]

        self.main_view = ViewMain(self.master, dsc=self.dsc, sound=self.sound)
        self.setup_main_buttons()

    def ensure_settings_file(self):
        """Tworzy lub wczytuje plik konfiguracyjny."""
        config_path = os.path.join(self.dsc, "resources", "setting.json")

        if not os.path.exists(config_path):
            default_config = {
                "volume": 0.4,
                "language_code": "pl_PL",
                "start_sound": "start_sound.wav",
                "info_sound": "info_sound.wav",
                "error_sound": "error_sound.wav",
                "confirm_sound": "confirm_sound.wav"
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            print("Utworzono plik konfiguracyjny.")
            return default_config

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_language(self, language_code):
        """Wczytuje plik językowy lub przywraca domyślny."""
        path = os.path.join(self.dsc, "resources", "language", f"{language_code}.json")
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Brak pliku językowego '{language_code}.json'.")
            self.messagebox_controller.language_error(language_code)
            self.json_setting(status="edit", key="language_code", value="pl_PL")
            return self.load_language("pl_PL")

    def json_setting(self, status="read", key=None, value=None):
        """Abstrakcja nad zapisem/odczytem JSON konfiguracji."""
        path = os.path.join(self.dsc, "resources", "setting.json")

        if status == "read":
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        if status == "edit":
            config = self.json_setting(status="read")
            config[key] = value
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return config

    def run(self):
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.mainloop()

    def on_close(self):
        """Zamyka aplikację z potwierdzeniem."""
        if self.messagebox_controller.close_info():
            self.master.destroy()

    def open_window(self, controller_class, **kwargs):
        """Uniwersalna metoda otwierania nowych okien."""
        controller = controller_class(
            master=self.master,
            dsc=self.dsc,
            leksykon_programu=self.leksykon_programu[kwargs["window_key"]],
            konfiguracja_programu=self.konfiguracja_programu,
            sound=self.sound,
            messagebox_controller=ControllerMessageBox(sound=self.sound, leksykon_messagebox=self.leksykon_programu.get("messagebox_window", {})),
            currency=self.leksykon_programu.get("currency", "None"),
            language_code=self.language_code,
            main_controller=self
        )
        controller.run()
        return controller

    def open_stock_window(self):
        from controller.ControllerStock import ControllerStock
        self.stock_controller = self.open_window(ControllerStock, window_key="stock_window")

    def open_order_window(self):
        from controller.ControllerOrder import ControllerOrder
        self.order_controller = self.open_window(ControllerOrder, window_key="order_window")

    def open_statistics_window(self):
        from controller.ControllerStatistic import ControllerStatistic
        self.stat_controller = self.open_window(ControllerStatistic, window_key="statistics_window")

    def open_settings_window(self):
        """Na razie prosty przykład aktualizacji głośności."""
        self.json_setting(status="edit", key="volume", value=1)
        self.konfiguracja_programu = self.json_setting(status="read")
        self.sound.config = self.konfiguracja_programu

    def setup_main_buttons(self):
        """Tworzy główne przyciski menu."""
        frame = self.main_view.main_view_frame
        buttons = [
            ("button_stan_magazynu", self.open_stock_window, 0, 0),
            ("button_zamowienia", self.open_order_window, 0, 1),
            ("button_statystyki", self.open_statistics_window, 1, 0),
            ("button_ustawienia", self.open_settings_window, 3, 0),
            ("button_wyjscie", self.on_close, 4, 0)
        ]

        for key, command, row, col in buttons:
            leksykon = self.leksykon_programu.get("main_window", {}).get(key, {"text": key})
            self.main_view.utworz_przycisk(
                frame,
                command,
                icon=self.main_view.settings_button_icon,
                leksykon_programu=leksykon,
                row=row,
                column=col,
                pack=False,
                columnspan=2 if "statystyki" in key or "ustawienia" in key or "wyjscie" in key else 1
            )

        # self.main_view.separator(frame)
