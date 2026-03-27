from addons.ctkcomponents import *
import customtkinter as ct

# from tkinter import simpledialog


class ViewMessageBox:
    """Widok obsługujący różne typy komunikatów i popupów w aplikacji."""

    def __init__(self):
        self.my_progress = None

    # ------------------------
    # ASYNC / PROGRESS MESSAGE
    # ------------------------
    def show_message_async(self, master, leksykon):
        """Pokazuje asynchroniczny komunikat z paskiem postępu."""
        self.my_progress = CTkProgressPopup(
            master=master,
            title=leksykon.get("heading", "Background operation"),
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
                pass
            self.my_progress = None

    def update_progress(self, progress: float):
        """Aktualizuje pasek postępu (0.0–1.0)."""
        if self.my_progress:
            try:
                self.my_progress.update_progress(progress)
            except Exception:
                pass

    # ------------------------
    # GENERAL MESSAGEBOX
        # ------------------------
    def messagebox(self, type, heading=None, text=None, value=None, app=None, language_code=None, value_buttons=None):
        type = type.lower().strip()

        # ERROR
        if type == "error" or (type == "language" and language_code):
            CTkNotification(
                master=app,
                state="error",
                message=f"{heading}\n{text}",
                side="left_top"
            )
            return

        # INFO
        elif type == "info":
            CTkNotification(
                master=app,
                state="info",
                message=text,
                side="left_top"
            )
            return

        # CLOSE / ASK
        elif type == "close":
            alert = CTkAlert_Emsii_Version(
                state="warning",
                title=heading or "Dialog",
                body_text=text or "",
                btn1=value[0] if value else "OK",
                btn2=value[1] if value and len(value) > 1 else "Cancel"
            )
            return alert.get() if type == "ask" else alert.get() == (value[0] if value else "OK")

        elif type == "delete":
            alert = CTkAlert_Emsii_Version(
                state="error",
                title=heading or "Delete",
                body_text=text or "",
                btn1=value_buttons[0] if value_buttons else "Delete",
                btn2=value_buttons[1] if value_buttons and len(value_buttons) > 1 else "Cancel"
            )
            return alert.get() == (value_buttons[0] if value_buttons else "Delete")

        # ASKSTRING
        elif type in ["add", "edit"]:
            if value is None:
                text= f'{text}'
            else:
                text= f'{text} \n {value}'
                
            return ct.CTkInputDialog(
                title=heading or "Input",
                text= text or "",
                initial_value=value if type == "edit" else ""
            ).get_input()

        else:
            raise ValueError(f"Unknown messagebox type: {type}")
            
