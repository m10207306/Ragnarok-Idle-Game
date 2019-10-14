import time, sys, os        # Built-in Library
import Character            # My Own Script

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

class WorldClass:
    def __init__(self, window_screen):
        self.window = window_screen
        self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.jpg"), 200)     # clear screen and reset background
        rect = self.window.set_message_box(self.window.background.get_rect(), ["Please Enter the Character Name: (English)"])
        # return the rect address of the message box
        rect = self.window.set_block((252, 28), (0, 0, 0), (rect.center[0] - 126, rect.center[1] - 14))
        # return the rect address of the block
        name = self.window.get_cmd(rect)
        self.Char_obj = Character.CharacterClass(name)

    def run(self):
        idx = True
        while idx:
            idx = self.city_standby("Prondra")

    def city_standby(self, city):
        self.window.set_bg_image(os.path.join("BG_Image", city + "_BG.png"), 255)
        self.window.play_bgm(os.path.join("BG_Music", city + ".mp3"))
        self.window.set_idle_char(self.Char_obj.job_name)
        self.window.set_status_window(self.Char_obj)
        self.window.set_chat_window(["You are at: " + city,
                                     "Press [A] to Character Attribute Page",
                                     "              [I] to Item Page",
                                     "              [K] to Fight!",
                                     "              [E] to Exit Game"], Green)

        while True:
            self.window.tick(self.window.fps)
            content = self.window.get_key()
            if content == "a":
                print("\n>> Attribute Page")
                return True
            elif content == "i":
                print("\n>> Item Page")
                return True
            elif content == "k":
                print("\n>> Fight")
                return True
            elif content == "e":
                print("\n>> Exit")
                return False





