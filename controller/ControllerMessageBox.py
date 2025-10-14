from view.ViewMessageBox import ViewMessageBox


class ControllerMessageBox:
    """Kontroler odpowiedzialny za obsługę komunikatów (message boxów) i dźwięków."""
    def __init__(self, leksykon_messagebox=None, sound=None):
        self.leksykon_messagebox = leksykon_messagebox or {}
        self.sound = sound
        self.view = ViewMessageBox()

    def language_error(self, language_code: str):
        """Wyświetla błąd, gdy plik językowy nie został znaleziony."""
        if self.sound:
            self.sound.play_error_sound()
        self.view.messagebox(
            type="error",
            language_code=language_code,
            heading="Error",
            text=f"Language file '{language_code}.json' not found. Default language 'pl_PL' loaded."
        )

    def close_info(self) -> bool:
        """Pokazuje okno potwierdzenia zamknięcia aplikacji."""
        leksykon = self.leksykon_messagebox.get("close_messagebox", {})
        if self.sound:
            self.sound.play_info_sound()
        return self.view.messagebox(
            type="close",
            heading=leksykon.get("heading", "Exit"),
            text=leksykon.get("text", "Do you want to close the application?")
        )

    def show_message_async(self, master):
        """Pokazuje asynchroniczny komunikat (np. w trakcie ładowania)."""
        self.view.show_message_async(master=master, leksykon=self.leksykon_messagebox)

    def hide_message_async(self, master):
        """Ukrywa asynchroniczny komunikat."""
        self.view.hide_message_async()

    def update_message_async(self, progress: float):
        """Aktualizuje pasek postępu komunikatu."""
        self.view.update_progress(progress)

    def messagebox(self, type, heading=None, text=None, value=None, app=None):
        """Ogólny interfejs do wywoływania okna komunikatu."""
        return self.view.messagebox(
            type=type,
            heading=heading,
            text=text,
            value=value,
            app=app
        )
