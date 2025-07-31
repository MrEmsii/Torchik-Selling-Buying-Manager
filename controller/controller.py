from model.models import SQLconnect, select, Kupujacy, Kategoria, Sklep, Firma, Zamowienie, Artykul_Lista, artykuly_relacja
from view.view import View

import os

import threading
import json
import datetime as datetime

class Controller:
    def __init__(self):
        self.dsc = os.path.dirname(os.path.abspath(__file__))
        self.view = None
        self.session = SQLconnect(self.dsc)
        self.setup_view()

    def setup_view(self):
        self.view = View()
        self.view.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.view.master.mainloop()

    def on_closing(self):
        if View.messagebox(self, type="close"):
            self.session.close()
            self.view.master.destroy()

    def json_language(self, language_code):
        try:
            with open(os.path.join(self.dsc, "language", f"{language_code}.json"), 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            View.messagebox("language", language_code)
            return {}

    def json_setting(self, status = "read", key = None, value = None):
        if status == "start":
            config = {
                "volume": 0.1, 
                "language": "pl_PL",
                "start_sound": "start_sound.wav",
                "click_sound": "click_sound.wav",
                "error_sound": "error_sound.wav"
            }

            with open("setting.json", 'w', encoding='utf-8') as settings:
                json.dump(config, settings, ensure_ascii=False, indent=4)  

        elif status == "read":
            with open("setting.json", 'r') as settings:
                config = json.load(settings)
                return config

        elif status == "edit":
            config = self.json_setting(status="read")
            config[key] = value
