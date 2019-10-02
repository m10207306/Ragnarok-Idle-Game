import time, sys, pygame
import Character


class WorldClass:
    def __init__(self):
        # Create Character
        name = input(">> Please Enter the Character Name: ")
        Char_obj = Character.CharacterClass(name)
        print(">> Success!")
        print(">> Character Information:")
        print(Char_obj)
        self.city()

    def city(self):
        interface = "=====================================================\n" + \
                    ">> Your Position: Prondra \n" + \
                    ">> Press [A] to Character Attribute Page \n" + \
                    ">>       [E] to Item Page \n" + \
                    ">>       [K] to Fight!"
        print(interface)
        play_BGM("Prondra.mp3")
        while True:
            sys.stdout.write("\r>> " + time.strftime("Time: %Y-%m-%d   %H:%M:%S  (%a)", time.localtime()))
            sys.stdout.flush()


def play_BGM(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
