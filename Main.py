# -*- coding: utf-8 -*-
import time                         # Built-in Library
import World, Graphic         # My Own Library


class Ragnarok:
    def __init__(self):
        self.menu_title = """\n
        ================================================
        ============== Ragnarok Idle Game ==============
        ================================================

                  Press [S] to start new game           
                        [L] to load data                
                        [E] to exit                     """
        self.menu_title2 = [
            "================================================",
            "============== Ragnarok Idle Game ==============",
            "================================================",
            "                                                ",
            "         Press [S] to start new game            ",
            "               [L] to load data                 ",
            "               [E] to exit                      "
        ]
        self.window = Graphic.WindowClass()

    def run(self):
        self.window.play_bgm("Login.mp3")
        idx = True
        while idx:
            idx = self.standby()

    def standby(self):
        # print(self.menu_title)
        self.window.display_text("Ragnarok")
        while True:
            time.sleep(0.05)
            content = self.window.key_detection()
            if content == "s":
                # world_obj = World.WorldClass(self.window)
                # world_obj.run()
                return True
            elif content == "l":
                print("\n>> load game")
                return False
            elif content == "e":
                print("\n>> See ya!")
                return False


if __name__ == "__main__":
    RO = Ragnarok()
    # RO.run()
