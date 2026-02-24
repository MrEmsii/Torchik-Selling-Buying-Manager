from view.ViewMessageBox import ViewMessageBox


class ControllerMessageBox:
    """Kontroler odpowiedzialny za obsługę komunikatów (message boxów) i dźwięków."""

    def __init__(self, leksykon_messagebox=None, sound=None):
        self.leksykon_messagebox = leksykon_messagebox or {}
        self.sound = sound
        self.view = ViewMessageBox()

    # ------------------------
    # LANGUAGE ERROR
    # ------------------------
    def language_error(self, language_code: str, app=None):
        leksykon = self.leksykon_messagebox.get("language_error", {})
        if self.sound:
            self.sound.play_error_sound()
        return self.view.messagebox(
            type="error",
            heading=leksykon.get("heading", "Error"),
            text=leksykon.get(
                "text",
                f"Language file '{language_code}.json' not found. Default language 'pl_PL' loaded."
            ),
            app=app
        )

    # ------------------------
    # CLOSE INFO
    # ------------------------
    def close_info(self, app=None) -> bool:
        leksykon = self.leksykon_messagebox.get("close_messagebox", {})
        if self.sound:
            self.sound.play_info_sound()
        return self.view.messagebox(
            type="close",
            heading=leksykon.get("heading", "Exit"),
            text=leksykon.get("text", "Do you want to close the application?"),
            value=leksykon.get("buttons", ["Exit", "Cancel"]),
            app=app
        )

    # ------------------------
    # GENERIC MESSAGEBOX
    # ------------------------
    def messagebox(self, type: str, app=None, key: str = None) -> any:
        """
        Ogólny interfejs do wywoływania messageboxa.
        Typy obsługiwane: error, info, close, ask, delete
        Teksty pobierane z leksykonu, key wybiera podtekst np. 'order', 'shop'.
        """
        type = type.lower().strip()
        leksykon = self.leksykon_messagebox.get(f"{type}_messagebox", {})

        heading = leksykon.get("heading", "Information")
        text_data = leksykon.get("text", "")
        value_buttons = leksykon.get("buttons", ["OK"])

        # Pobranie tekstu z leksykonu
        if key and isinstance(text_data, dict):
            text = text_data.get(key, next(iter(text_data.values())))
        elif isinstance(text_data, str):
            text = text_data
        else:
            text = next(iter(text_data.values())) if isinstance(text_data, dict) else str(text_data)

        # Dźwięki
        if self.sound:
            if type in ["error", "delete"]:
                self.sound.play_error_sound()
            elif type in ["info", "close"]:
                self.sound.play_info_sound()

        # Mapowanie delete -> ask w widoku
        view_type = "askstring" if type == "delete" else type

        # view_type = "ask" if type == "delete" else type

        dialog = self.view.messagebox(
            type=view_type,
            heading=heading,
            text=text,
            value=value_buttons,
            app=app
        )
        if dialog in self.leksykon_messagebox.get("delete_messagebox", {}).get("buttons", []):
            return True
        else:
            return None
    # ------------------------
    # ASYNC MESSAGE
    # ------------------------
    def show_message_async(self, master):
        leksykon = self.leksykon_messagebox.get("async_messagebox", {})
        self.view.show_message_async(master=master, leksykon=leksykon)

    def hide_message_async(self, master=None):
        self.view.hide_message_async()

    def update_message_async(self, progress: float):
        self.view.update_progress(progress)