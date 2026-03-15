from addons.CTkToolTip import CTkToolTip

import addons.customtkinter as ct


class BaseView:
    def __init__(self, sound):
        self.sound = sound

    def utworz_przycisk(self, frame, command, leksykon_programu, side='top', padx=5, pady=5, columnspan=1, icon=None, pack = True, column=0, row=0):
        try:
            text=leksykon_programu.get("text", "Button")
            toolTip=leksykon_programu.get("toolTip", "")
        except KeyError:
            text="Button"
            toolTip=""
        except AttributeError:
            text="Button"
            toolTip=""

        przycisk = ct.CTkButton(
            frame,
            text=text,
            command=self._click_sound(command),
            width=100,
            image=icon,
            compound="left",
            anchor="w",
            corner_radius=8
        )
        if pack:
            przycisk.pack(side=side, padx=padx, pady=pady, fill='x')
        else:
            przycisk.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew", columnspan=columnspan)
        CTkToolTip(przycisk, message=toolTip)
        return przycisk

    def _click_sound(self, func):
        def wrapper(*args, **kwargs):
            self.sound.play_info_sound()
            return func(*args, **kwargs)
        return wrapper


    def create_entry_with_placeholder(self, parent, textvariable, placeholder, **kwargs):
        entry = ct.CTkEntry(parent, textvariable=textvariable, **kwargs)
        if not textvariable.get():
            entry.insert(0, placeholder)
            entry.configure(fg_color="gray25")
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, "end")
                    entry.configure(fg_color="gray10")
            def on_focus_out(e):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.configure(fg_color="gray25")
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        return entry