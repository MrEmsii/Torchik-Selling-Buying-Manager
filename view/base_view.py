import tkinter as tk
from tkinter import ttk
from TkToolTip import ToolTip

class BaseView:
    def __init__(self, sound):
        self.sound = sound

    def utworz_przycisk(self, frame, command, leksykon_programu, side='top', padx=1, pady=3, icon=None):
        przycisk = ttk.Button(
            frame,
            text=leksykon_programu["text"],
            command=self._click_sound(command),
            width=10,
            image=icon or None,
            compound="left"
        )
        przycisk.pack(side=side, padx=padx, pady=pady)
        ToolTip(przycisk, msg=leksykon_programu["toolTip"], follow=True)
        return przycisk

    def _click_sound(self, func):
        def wrapper(*args, **kwargs):
            self.sound.play_info_sound()
            return func(*args, **kwargs)
        return wrapper


