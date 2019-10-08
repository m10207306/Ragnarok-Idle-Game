import time, sys, os        # Built-in Library
import Character            # My Own Script
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library


class WorldClass:
    def __init__(self, window_screen):
        self.window = window_screen
        self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.jpg"), 200)     # clear screen and reset background
        rect = self.window.set_message_box(self.window.background.get_rect(), ["Please Enter the Character Name: (English)"])
        # return the rect address of the message box
        rect = self.window.set_block((300, 26), (0, 0, 0), (rect.center[0] - 150, rect.center[1] - 13))
        # return the rect address of the block
        name = self.window.get_cmd(rect)
        self.Char_obj = Character.CharacterClass(name)
        print(self.Char_obj)

    def run(self):
        idx = True
        while idx:
            idx = self.city_console("Prondra", True)

    def city_console(self, city, replay_bgm):
        interface = "=====================================================\n" + \
                    ">> Your Position: " + city + " \n" + \
                    ">> Press [A] to Character Attribute Page \n" + \
                    ">>       [I] to Item Page \n" + \
                    ">>       [K] to Fight! \n" + \
                    ">>       [E] to Menu \n"
        print(interface)
        if replay_bgm:
            self.window.play_bgm(os.path.join("BG_Music", city + ".mp3"))
        return self.city_standby()

    def city_standby(self):
        while True:
            self.window.tick(self.window.fps)
            update_print(time.strftime("Time: %Y-%m-%d   %H:%M:%S  (%a)", time.localtime()))
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


def update_print(content):
    sys.stdout.write("\r>> " + content)
    sys.stdout.flush()



