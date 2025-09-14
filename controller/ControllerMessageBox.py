from view.ViewMessageBox import ViewMessageBox
from view.ViewSound import ViewSound 

class ControllerMessageBox:
    def __init__(self, leksykon_messagebox = None, sound = None):
        self.leksykon_messagebox = leksykon_messagebox
        self.view = ViewMessageBox()
        self.sound = sound

    def language_error(self, language_code):
        self.sound.play_error_sound()
        self.view.messagebox(type="error", language_code=language_code, heading="Error",
                             text=f"Language file '{language_code}.json' not found. Default language 'pl_PL' loaded.")

    def close_info(self):
        leksykon = self.leksykon_messagebox["close_messagebox"]
        self.sound.play_info_sound()
        return self.view.messagebox(type="close", heading=leksykon["heading"], text=leksykon["text"])
    
    def show_message_async(self, master):
        self.view.show_message_async(master=master, leksykon=self.leksykon_messagebox)

    def ukryj_message_async(self, master):
        self.view.ukryj_message_async(master=master)

    def messagebox(self, type, heading=None, text=None, value=None):
        return self.view.messagebox(type=type, heading=heading, text=text, value=value)