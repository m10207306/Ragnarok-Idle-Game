import time, sys, os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame, keyboard
import Character


class WorldClass:
    def __init__(self):
        # Create Character
        name = input(">> Please Enter the Character Name: ")
        self.Char_obj = Character.CharacterClass(name)
        print(">> Success!")
        print(">> Character Information:")
        print(self.Char_obj)
        self.home_console()

    def home_console(self):
        interface = "=====================================================\n" + \
                    ">> Your Position: Prondra \n" + \
                    ">> Press [A] to Character Attribute Page \n" + \
                    ">>       [I] to Item Page \n" + \
                    ">>       [K] to Fight!"
        print(interface)
        play_bgm("Prondra.mp3")
        while True:
            time.sleep(0.1)
            update_print(time.strftime("Time: %Y-%m-%d   %H:%M:%S  (%a)", time.localtime()))
            if keyboard.is_pressed("a"):
                print("Character Attribute Page")
                break
            elif keyboard.is_pressed("i"):
                print("Item Page")
            elif keyboard.is_pressed("k"):
                print("Fight!")
                break


def play_bgm(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops = -1)


def update_print(content):
    sys.stdout.write("\r>> " + content)
    sys.stdout.flush()
