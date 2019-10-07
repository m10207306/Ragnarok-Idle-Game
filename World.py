import time, sys, os        # Built-in lLibrary
import Character            # My Own Script


class WorldClass:
    def __init__(self, window_screen):
        self.window = window_screen
        name = input(">> Please Enter the Character Name: ")
        self.Char_obj = Character.CharacterClass(name)
        print(">> Create Character Success!")
        print(">> Character Information:")
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
            self.window.play_bgm(city + ".mp3")
        return WorldClass.city_standby()

    def city_standby(self):
        while True:
            time.sleep(0.05)
            update_print(time.strftime("Time: %Y-%m-%d   %H:%M:%S  (%a)", time.localtime()))
            content = self.window.key_detection()
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



