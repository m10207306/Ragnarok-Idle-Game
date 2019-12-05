# -*- coding: utf-8 -*-
import os                     # Built-in Library
import World, Graphic         # 自己的Code
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來

class Ragnarok:
    def __init__(self):
        self.window = Graphic.WindowClass()

    def run(self):
        idx = True
        while idx:
            self.window.play_bgm(os.path.join("BG_Music", "Login.mp3"))
            self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.png"), 200)
            self.window.set_message_box(self.window.background.get_rect().center, ["     按 [S] 開始新遊戲",
                                                                                   "          [L] 載入舊檔",
                                                                                   "          [Esc] 離開遊戲"])
            pygame.display.update()
            idx = self.standby()

    def standby(self):
        while True:
            self.window.clock.tick(self.window.fps)
            content = self.window.get_key()
            if content == "s":
                world_obj = World.WorldClass(self.window)
                self.window.interlude_black_window()
                world_obj.run("Prontera")
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
