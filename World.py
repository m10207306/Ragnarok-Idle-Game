import os                           # Built-in Library
import Character, Battle            # 自己的Code

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class WorldClass:
    def __init__(self, window_screen):
        self.window = window_screen
        self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.png"), 200)
        # 清理背景跟重置背景
        rect = self.window.set_message_box(self.window.background.get_rect(), ["請輸入角色名稱: (英文)"])
        # return message box 的 rect address
        rect = self.window.set_block((0, 0, 0), self.window.create_rect(rect.center[0] - 126, rect.center[1] - 11, 252, 22))
        # return block 的 rect address
        name = self.window.get_cmd(rect)
        self.Char_obj = Character.CharacterClass(name)

    def run(self, city):
        idx = True
        while idx:
            self.window.set_bg_image(os.path.join("BG_Image", city + "_BG.png"), 255)
            self.window.play_bgm(os.path.join("BG_Music", city + ".mp3"))
            self.window.set_sit_char(self.Char_obj.sit_img_path)
            self.window.set_status_window(self.Char_obj)
            self.window.reset_chat_message()
            self.window.set_chat_window(["嗨, " + self.Char_obj.char_name,
                                         "你的位置在: " + city,
                                         "按下 [A] 到人物素質介面",
                                         "         [I] 到物品介面",
                                         "         [K] 前往戰鬥",
                                         "         [Esc] 回主畫面"], [Green, Green, Green, Green, Green, Green])
            idx = self.city_standby()

    def city_standby(self):
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
                battle_scene = Battle.BattleControl(self.window, os.path.join("BG_Image", "Battle.png"), self.Char_obj)
                battle_scene.run()
                print("\n>> Fight")
                return True
            elif content == "e" or content == "esc":
                print("\n>> Exit")
                return False





