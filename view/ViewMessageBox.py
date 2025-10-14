from tkinter import messagebox, simpledialog
from CustomTkinterMessagebox import CTkMessagebox
from ctkcomponents import *

import customtkinter as ct


class ViewMessageBox:
    """Widok obsługujący różne typy komunikatów i popupów w aplikacji."""

    def __init__(self):
        self.my_progress = None
        self.msg_window = None

    def show_message_async(self, master, leksykon):
        """Pokazuje asynchroniczny komunikat z paskiem postępu."""
        self.my_progress = CTkProgressPopup(
            master=master,
            title="Background Tasks",
            label=leksykon.get("progress_label", "Working..."),
            message=leksykon.get("progress_message", "Please wait..."),
            side="left_top"
        )

    def hide_message_async(self):
        """Zamyka asynchroniczne okno progressu, jeśli istnieje."""
        if self.my_progress:
            try:
                self.my_progress.cancel_task()
            except Exception:
                print("Error closing progress popup")
                pass
            self.my_progress = None
        else:
            print("No progress popup to close")

    def update_progress(self, progress: float):
        """Aktualizuje pasek postępu (0.0–1.0)."""
        if self.my_progress:
            try:
                self.my_progress.update_progress(progress)
            except Exception:
                print("Error updating progress popup")
                pass
        else:
            pass
        
    def messagebox(self, type, language_code=None, heading=None, text=None, value=None, app=None):
        """Obsługuje różne typy komunikatów w wersji CustomTkinter."""
        type = type.lower().strip()

        if type == "error" or type == "language" and language_code:
            return CTkNotification(master=app, state="error", message=f"{heading}\n{text}", side="left_top")

        elif type == "info":
            return CTkNotification(master=app, state="info", message=text, side="left_top")

        elif type == "close":
            alert = CTkAlert(state="info", title=heading or "Exit", body_text=text or "Do you want to exit?",
                             btn1="Exit", btn2="Cancel")
            return alert.get() == "Exit"

        elif type == "ask":
            return simpledialog.askstring(heading or "Input", text or "", initialvalue=value)

        else:
            raise ValueError(f"Unknown messagebox type: {type}")

