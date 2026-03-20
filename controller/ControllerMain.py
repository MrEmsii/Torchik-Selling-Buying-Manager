import os
import json

import addons.customtkinter as ct

from view.ViewSound import ViewSound
from view.ViewMain import ViewMain

from controller.ControllerMessageBox import ControllerMessageBox

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")


class ControllerMain:
    """Główny kontroler aplikacji Torchik – zarządza oknami i konfiguracją."""

    def __init__(self):
        self.dsc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.master = ct.CTk()

        # GLOBAL STATE (WSPÓŁDZIELONY)
        self.konfiguracja_programu = self.ensure_settings_file()
        self.all_currency = self.ensure_currency_file()

        # LISTA AKTYWNYCH KONTROLERÓW
        self.open_controllers = []

        # LANGUAGE
        self.language_code = self.konfiguracja_programu.get("language_code", "pl_PL")
        self.leksykon_programu = self.load_language(self.language_code)

        # SOUND
        self.sound = ViewSound(self.dsc, self.konfiguracja_programu)

        # MESSAGEBOX (JEDNA INSTANCJA)
        self.messagebox_controller = ControllerMessageBox(
            sound=self.sound,
            leksykon_messagebox=self.leksykon_programu.get("messagebox_window", {})
        )

        # MAIN VIEW
        self.main_view = ViewMain(self.master, dsc=self.dsc, sound=self.sound)
        self.setup_main_buttons()

    # =========================
    # CONFIG
    # =========================

    def ensure_settings_file(self):
        config_path = os.path.join(self.dsc, "resources", "setting.json")

        if not os.path.exists(config_path):
            default_config = {
                "volume": 0.4,
                "language_code": "pl_PL",
                "start_sound": "start_sound.wav",
                "info_sound": "info_sound.wav",
                "error_sound": "error_sound.wav",
                "confirm_sound": "confirm_sound.wav",
                "currency_code": "PLN"
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)

            print("Utworzono plik konfiguracyjny.")
            return default_config

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def ensure_currency_file(self):
        currency_path = os.path.join(self.dsc, "resources", "currency.json")

        if not os.path.exists(currency_path):
            default_currency = {
                "PLN": {"symbol": "zł", "symbol_first": 0},
                "USD": {"symbol": "$", "symbol_first": 1},
                "EUR": {"symbol": "€", "symbol_first": 1}
            }
            with open(currency_path, "w", encoding="utf-8") as f:
                json.dump(default_currency, f, ensure_ascii=False, indent=4)

            print("Utworzono plik z danymi walut.")
            return default_currency

        with open(currency_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_language(self, language_code):
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

    # =========================
    # SETTINGS UPDATE SYSTEM
    # =========================

    def reload_settings(self):
        """Aktualizuje config i powiadamia wszystkie kontrolery."""

        new_config = self.json_setting(status="read")

        # NIE PODMIENIAMY OBIEKTU – tylko aktualizujemy
        self.konfiguracja_programu.clear()
        self.konfiguracja_programu.update(new_config)

        # UPDATE SOUND
        self.sound.config = self.konfiguracja_programu

        # UPDATE LANGUAGE
        self.language_code = self.konfiguracja_programu.get("language_code", "pl_PL")
        self.leksykon_programu = self.load_language(self.language_code)

        # UPDATE MESSAGEBOX
        self.messagebox_controller.leksykon_messagebox = self.leksykon_programu.get("messagebox_window", {})

        # POWIADOM WSZYSTKIE KONTROLERY
        for controller in self.open_controllers:
            if hasattr(controller, "on_settings_changed"):
                controller.on_settings_changed()

    # =========================
    # WINDOW MANAGEMENT
    # =========================

    def open_window(self, controller_class, **kwargs):
        controller = controller_class(
            master=self.master,
            dsc=self.dsc,
            leksykon_programu=self.leksykon_programu[kwargs["window_key"]],
            konfiguracja_programu=self.konfiguracja_programu,
            sound=self.sound,
            messagebox_controller=self.messagebox_controller,
            all_currency=self.all_currency,
            language_code=self.language_code,
            main_controller=self
        )

        self.open_controllers.append(controller)
        return controller

    def open_stock_window(self):
        from controller.ControllerStock import ControllerStock

        # jeśli istnieje i okno żyje → tylko focus
        if hasattr(self, "stock_controller") and self.stock_controller:
            if self.stock_controller.stock_master.winfo_exists():
                self.stock_controller.stock_master.lift()
                self.stock_controller.stock_master.focus_force()
                return

        # jeśli nie istnieje → twórz nowe
        self.stock_controller = self.open_window(
            ControllerStock,
            window_key="stock_window"
        )
        
    def open_order_window(self):
        from controller.ControllerOrder import ControllerOrder

        # jeśli istnieje i okno żyje → tylko focus
        if hasattr(self, "order_controller") and self.order_controller:
            if self.order_controller.order_master.winfo_exists():
                self.order_controller.order_master.lift()
                self.order_controller.order_master.focus_force()
                return

        # jeśli nie istnieje → twórz nowe
        self.order_controller = self.open_window(
            ControllerOrder,
            window_key="order_window"
        )

    def open_statistics_window(self):
        from controller.ControllerStatistic import ControllerStatistic

        # jeśli istnieje i okno żyje → tylko focus
        if hasattr(self, "stat_controller") and self.stat_controller:
            if self.stat_controller.stat_master.winfo_exists():
                self.stat_controller.stat_master.lift()
                self.stat_controller.stat_master.focus_force()
                return

        # jeśli nie istnieje → twórz nowe
        self.stat_controller = self.open_window(
            ControllerStatistic,
            window_key="statistics_window"
        )

    # =========================
    # ACTIONS
    # =========================

    def open_settings_window(self):
        """Przykładowa zmiana ustawień."""

        self.json_setting(status="edit", key="volume", value=1)

        if self.konfiguracja_programu.get("currency_code") == "USD":
            self.json_setting(status="edit", key="currency_code", value="PLN")
        else:
            self.json_setting(status="edit", key="currency_code", value="USD")

        self.reload_settings()

    # =========================
    # UI
    # =========================

    def setup_main_buttons(self):
        frame = self.main_view.main_view_frame

        buttons = [
            ("button_stan_magazynu", self.open_stock_window, 0, 0),
            ("button_zamowienia", self.open_order_window, 0, 1),
            ("button_statystyki", self.open_statistics_window, 1, 0),
            ("button_przerwa", None, 2, 0),
            ("button_ustawienia", self.open_settings_window, 3, 0),
            ("button_wyjscie", self.on_close, 4, 0)
        ]

        for key, command, row, col in buttons:
            if command is None:
                self.main_view.utworz_przerwe_frame(frame, row=row, columnspan=2, pack=False)
                continue

            leksykon = self.leksykon_programu.get("main_window", {}).get(key, {"text": key})

            self.main_view.utworz_przycisk(
                frame,
                command,
                icon=self.main_view.settings_button_icon,
                leksykon_programu=leksykon,
                row=row,
                column=col,
                pack=False,
                columnspan=2 if key in ["button_statystyki", "button_ustawienia", "button_wyjscie"] else 1
            )

    # =========================
    # APP LIFECYCLE
    # =========================

    def run(self):
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.mainloop()

    def on_close(self):
        if self.messagebox_controller.close_info():
            self.master.destroy()