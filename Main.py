# -*- coding: utf-8 -*-
import os                     # Built-in Library
import World, Graphic         # My Own Library


class Ragnarok:
    def __init__(self):
        self.window = Graphic.WindowClass()

    def run(self):
        idx = True
        while idx:
            self.window.play_bgm(os.path.join("BG_Music", "Login.mp3"))
            self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.png"), 200)
            self.window.set_message_box(self.window.background.get_rect(), ["     按 [S] 開始新遊戲",
                                                                            "          [L] 載入舊檔",
                                                                            "          [E] 離開遊戲"])
            idx = self.standby()

    def standby(self):
        while True:
            self.window.tick(self.window.fps)
            content = self.window.get_key()
            if content == "s":
                self.window.chat_message = []
                world_obj = World.WorldClass(self.window)
                world_obj.run("Prondra")
                print(">> Create Character")
                return True
            elif content == "l":
                print(">> Load Game")
                return False
            elif content == "e" or content == "esc":
                print(">> See Ya!")
                return False


if __name__ == "__main__":
    RO = Ragnarok()
    RO.run()
