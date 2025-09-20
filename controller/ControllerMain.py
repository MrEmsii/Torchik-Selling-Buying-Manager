from tkinterdnd2 import DND_FILES, TkinterDnD

from view.ViewSound import ViewSound

from view.ViewMain import ViewMain
from controller.ControllerMessageBox import ControllerMessageBox

from controller.ControllerOrder import ControllerOrder
from controller.ControllerStatistic import ControllerStatistic


import os
import json

class ControllerMain:
    def __init__(self):
        #wczytanie słowników, podzielenie słowników na elementy, 
        #uruchomienie okna głównego z możliwością wybory dalszego działania - check
        #wybór między zamówienia, statystyki

        self.dsc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.master = TkinterDnD.Tk()


        if os.path.exists(self.dsc + "/resources/setting.json") == False:
            self.json_setting(status = "create")
            print("Setting file created.")
        
        self.konfiguracja_programu = self.json_setting(status="read")
        
        self.sound = ViewSound(self.dsc, self.konfiguracja_programu)
        self.messagebox_controller = ControllerMessageBox(sound=self.sound)  # Tymczasowe przypisanie None, zostanie zaktualizowane później

        self.language_code = self.konfiguracja_programu["language_code"]
        self.leksykon_programu = self.json_language(self.language_code)

        self.leksykon_messagebox = self.leksykon_programu["messagebox_window"]
        self.messagebox_controller.leksykon_messagebox = self.leksykon_messagebox

        self.main_view = ViewMain(self.master, dsc=self.dsc, leksykon=self.leksykon_programu, konfiguracja_programu=self.konfiguracja_programu)
        self.main_view_frame = self.main_view.main_view_frame
        
        self.button_order_click(self.main_view_frame)
        self.button_statistics_click(self.main_view_frame)
        self.button_settings_click(self.main_view_frame)
        self.button_exit_click(self.main_view_frame)

    def run(self):
        self.main_view.master.protocol("WM_DELETE_WINDOW", self.on_closing_order_window)
        self.main_view.master.mainloop()

    def on_closing_order_window(self):
        if self.messagebox_controller.close_info():
            self.main_view.master.destroy() 

    def json_language(self, language_code):
        try:
            with open(os.path.join(self.dsc, "resources", "language", f"{language_code}.json"), 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Language file '{language_code}.json' not found.")
            self.messagebox_controller.language_error(language_code)

            self.json_setting(status="edit", key="language_code", value="pl_PL")
            self.konfiguracja_programu = self.json_setting(status="read")

            self.language_code = self.konfiguracja_programu["language_code"]
            self.leksykon_programu = self.json_language(self.language_code)
        
            return self.leksykon_programu

    def json_setting(self, status = "read", key = None, value = None):
        if status == "create":
            config = {
                "volume": 0.4, 
                "language_code": "pl_PL",
                "start_sound": "start_sound.wav",
                "info_sound": "info_sound.wav",
                "error_sound": "error_sound.wav",
                "confirm_sound": "confirm_sound.wav"
            }

            with open(os.path.join(self.dsc, "resources", "setting.json"), 'w', encoding='utf-8') as settings:
                json.dump(config, settings, ensure_ascii=False, indent=4)  

        elif status == "read":
            with open(os.path.join(self.dsc, "resources", "setting.json"), 'r', encoding='utf-8') as settings:
                config = json.load(settings)
                return config

        elif status == "edit":
            config = self.json_setting(status="read")
            config[key] = value

            with open("resources/setting.json", "w", encoding="utf-8") as settings:
                json.dump(config, settings, ensure_ascii=False, indent=4)

            return config
        
    def open_order_window(self):
        self.order_controller = ControllerOrder(
            master = self.master,
            dsc=self.dsc,
            leksykon_programu=self.leksykon_programu["order_window"],
            messagebox_controller = self.messagebox_controller,
            sound = self.sound,
            konfiguracja_programu=self.konfiguracja_programu,
            currency=self.leksykon_programu["currency"],
            language_code=self.language_code
        )
        self.order_controller.run()

    def open_statistics_window(self):
        self.stat_controller = ControllerStatistic(
        master = self.master,
        dsc=self.dsc,
        leksykon_programu=self.leksykon_programu["order_window"],
        messagebox_controller = self.messagebox_controller,
        sound = self.sound,
        konfiguracja_programu=self.konfiguracja_programu,
        currency=self.leksykon_programu["currency"],
        language_code=self.language_code
        )

        self.stat_controller.run()

    def open_settings_window(self):
        pass

    def button_order_click(self, frame):
        leksykon = self.leksykon_programu["main_window"]["button_zamowienia"]
        self.main_view.utworz_przycisk(frame, self.open_order_window, icon=self.main_view.order_button_icon, leksykon_programu=leksykon)

    def button_statistics_click(self, frame):
        leksykon = self.leksykon_programu["main_window"]["button_statystyki"]
        self.main_view.utworz_przycisk(frame, self.open_statistics_window, icon=self.main_view.statistics_button_icon, leksykon_programu=leksykon)

    def button_settings_click(self, frame):
        leksykon = self.leksykon_programu["main_window"]["button_ustawienia"]
        self.main_view.utworz_przycisk(frame, self.open_settings_window, icon=self.main_view.settings_button_icon, leksykon_programu=leksykon)

    def button_exit_click(self, frame):
        leksykon = self.leksykon_programu["main_window"]["button_wyjscie"]
        self.main_view.utworz_przycisk(frame, self.on_closing_order_window, icon=self.main_view.exit_button_icon, leksykon_programu=leksykon)
