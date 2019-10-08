# -*- coding: utf-8 -*-
import os                     # Built-in Library
import World, Graphic         # My Own Library


class Ragnarok:
    def __init__(self):
        self.window = Graphic.WindowClass()

    def run(self):
        self.window.play_bgm(os.path.join("BG_Music", "Login.mp3"))
        idx = True
        while idx:
            idx = self.standby()

    def standby(self):
        while True:
            self.window.tick(self.window.fps)
            content = self.window.get_key()
            if content == "s":
                world_obj = World.WorldClass(self.window)
                world_obj.run()
                print(">> Create Character")
                return False
            elif content == "l":
                print(">> Load Game")
                return False
            elif content == "e":
                print(">> See Ya!")
                return False


if __name__ == "__main__":
    RO = Ragnarok()
    RO.run()
