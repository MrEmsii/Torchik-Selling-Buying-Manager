from pygame import mixer
import os

class ViewSound:
    def __init__(self, base_path, config):
        self.base_path = base_path
        self.config = config
        mixer.init()

    def play_start_sound(self):
        self._play_sound(self.config["start_sound"])

    def play_error_sound(self):
        self._play_sound(self.config["error_sound"])

    def play_info_sound(self):
        self._play_sound(self.config["info_sound"])

    def play_confirm_sound(self):
        self._play_sound(self.config["confirm_sound"])

    def _play_sound(self, filename):
        if self.config["volume"] != 0:
            sound_path = os.path.join(self.base_path, "resources", "sounds", filename)
            mixer.music.load(sound_path)
            mixer.music.set_volume(self.config["volume"])
            mixer.music.play()