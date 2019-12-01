import os                           # Built-in Library
import Character, Battle            # 自己的Code
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來

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
        rect = self.window.set_message_box(self.window.background.get_rect().center, ["請輸入角色名稱: (英文)"])
        # return message box 的 rect address
        name = ""
        while name == "":
            name = self.window.get_cmd(Black, pygame.Rect(rect.center[0] - 126, rect.center[1] - 11, 252, 22))

        ini_ability = self.initialize_ability(name)
        self.Char_obj = Character.CharacterClass(name)

    def initialize_ability(self, name):
        create_char = pygame.image.load(os.path.join("Info_Image", "win_make.png")).convert_alpha()
        stand_char = pygame.image.load(os.path.join("Char_Image", "Novice", "Stand.png")).convert_alpha()
        rect1 = create_char.get_rect()
        rect1.center = pygame.Rect(0, 0, self.window.width, self.window.height).center
        rect2 = stand_char.get_rect()
        rect2.center = (320, 392)
        self.window.screen.blit(create_char, rect1)

        center_pos = (512, 377)
        str_, agi_, vit_, int_, dex_, luk_ = 5, 5, 5, 5, 5, 5
        vertical_bias = [0, 3, 10, 20, 30, 40, 50, 60, 70, 79]
        nonvertical_xbias = [0, 3, 8, 16, 25, 33, 41, 49, 57, 67]
        nonvertical_ybias = [0, 3, 5, 10, 15, 20, 25, 30, 35, 41]
        str_idx = [center_pos, (center_pos[0], center_pos[1] - vertical_bias[1]),
                   (center_pos[0], center_pos[1] - vertical_bias[2]), (center_pos[0], center_pos[1] - vertical_bias[3]),
                   (center_pos[0], center_pos[1] - vertical_bias[4]), (center_pos[0], center_pos[1] - vertical_bias[5]),
                   (center_pos[0], center_pos[1] - vertical_bias[6]), (center_pos[0], center_pos[1] - vertical_bias[7]),
                   (center_pos[0], center_pos[1] - vertical_bias[8]), (center_pos[0], center_pos[1] - vertical_bias[9])]
        int_idx = [center_pos, (center_pos[0], center_pos[1] + vertical_bias[1]),
                   (center_pos[0], center_pos[1] + vertical_bias[2]), (center_pos[0], center_pos[1] + vertical_bias[3]),
                   (center_pos[0], center_pos[1] + vertical_bias[4]), (center_pos[0], center_pos[1] + vertical_bias[5]),
                   (center_pos[0], center_pos[1] + vertical_bias[6]), (center_pos[0], center_pos[1] + vertical_bias[7]),
                   (center_pos[0], center_pos[1] + vertical_bias[8]), (center_pos[0], center_pos[1] + vertical_bias[9])]
        agi_idx = [center_pos,
                   (center_pos[0] - nonvertical_xbias[1], center_pos[1] - nonvertical_ybias[1]),
                   (center_pos[0] - nonvertical_xbias[2], center_pos[1] - nonvertical_ybias[2]),
                   (center_pos[0] - nonvertical_xbias[3], center_pos[1] - nonvertical_ybias[3]),
                   (center_pos[0] - nonvertical_xbias[4], center_pos[1] - nonvertical_ybias[4]),
                   (center_pos[0] - nonvertical_xbias[5], center_pos[1] - nonvertical_ybias[5]),
                   (center_pos[0] - nonvertical_xbias[6], center_pos[1] - nonvertical_ybias[6]),
                   (center_pos[0] - nonvertical_xbias[7], center_pos[1] - nonvertical_ybias[7]),
                   (center_pos[0] - nonvertical_xbias[8], center_pos[1] - nonvertical_ybias[8]),
                   (center_pos[0] - nonvertical_xbias[9], center_pos[1] - nonvertical_ybias[9])]
        vit_idx = [center_pos,
                   (center_pos[0] + nonvertical_xbias[1], center_pos[1] - nonvertical_ybias[1]),
                   (center_pos[0] + nonvertical_xbias[2], center_pos[1] - nonvertical_ybias[2]),
                   (center_pos[0] + nonvertical_xbias[3], center_pos[1] - nonvertical_ybias[3]),
                   (center_pos[0] + nonvertical_xbias[4], center_pos[1] - nonvertical_ybias[4]),
                   (center_pos[0] + nonvertical_xbias[5], center_pos[1] - nonvertical_ybias[5]),
                   (center_pos[0] + nonvertical_xbias[6], center_pos[1] - nonvertical_ybias[6]),
                   (center_pos[0] + nonvertical_xbias[7], center_pos[1] - nonvertical_ybias[7]),
                   (center_pos[0] + nonvertical_xbias[8], center_pos[1] - nonvertical_ybias[8]),
                   (center_pos[0] + nonvertical_xbias[9], center_pos[1] - nonvertical_ybias[9])]
        dex_idx = [center_pos,
                   (center_pos[0] - nonvertical_xbias[1], center_pos[1] + nonvertical_ybias[1]),
                   (center_pos[0] - nonvertical_xbias[2], center_pos[1] + nonvertical_ybias[2]),
                   (center_pos[0] - nonvertical_xbias[3], center_pos[1] + nonvertical_ybias[3]),
                   (center_pos[0] - nonvertical_xbias[4], center_pos[1] + nonvertical_ybias[4]),
                   (center_pos[0] - nonvertical_xbias[5], center_pos[1] + nonvertical_ybias[5]),
                   (center_pos[0] - nonvertical_xbias[6], center_pos[1] + nonvertical_ybias[6]),
                   (center_pos[0] - nonvertical_xbias[7], center_pos[1] + nonvertical_ybias[7]),
                   (center_pos[0] - nonvertical_xbias[8], center_pos[1] + nonvertical_ybias[8]),
                   (center_pos[0] - nonvertical_xbias[9], center_pos[1] + nonvertical_ybias[9])]
        luk_idx = [center_pos,
                   (center_pos[0] + nonvertical_xbias[1], center_pos[1] + nonvertical_ybias[1]),
                   (center_pos[0] + nonvertical_xbias[2], center_pos[1] + nonvertical_ybias[2]),
                   (center_pos[0] + nonvertical_xbias[3], center_pos[1] + nonvertical_ybias[3]),
                   (center_pos[0] + nonvertical_xbias[4], center_pos[1] + nonvertical_ybias[4]),
                   (center_pos[0] + nonvertical_xbias[5], center_pos[1] + nonvertical_ybias[5]),
                   (center_pos[0] + nonvertical_xbias[6], center_pos[1] + nonvertical_ybias[6]),
                   (center_pos[0] + nonvertical_xbias[7], center_pos[1] + nonvertical_ybias[7]),
                   (center_pos[0] + nonvertical_xbias[8], center_pos[1] + nonvertical_ybias[8]),
                   (center_pos[0] + nonvertical_xbias[9], center_pos[1] + nonvertical_ybias[9])]
        color = (123, 145, 203)
        pygame.draw.polygon(self.window.screen, color,
                            [str_idx[str_], agi_idx[agi_], dex_idx[dex_], int_idx[int_], luk_idx[luk_],
                             vit_idx[vit_]])
        self.window.screen.blit(self.window.font.render(str(str_), True, Black), (725, 253))
        self.window.screen.blit(self.window.font.render(str(agi_), True, Black), (725, 269))
        self.window.screen.blit(self.window.font.render(str(vit_), True, Black), (725, 286))
        self.window.screen.blit(self.window.font.render(str(int_), True, Black), (725, 302))
        self.window.screen.blit(self.window.font.render(str(dex_), True, Black), (725, 318))
        self.window.screen.blit(self.window.font.render(str(luk_), True, Black), (725, 334))
        self.window.screen.blit(self.window.font.render(name, True, Black), (293, 460))
        self.window.screen.blit(stand_char, rect2)
        pygame.display.update()
        while True:
            self.window.clock.tick(10)
            content = self.window.get_key()
            if content == "s":
                str_ = str_ + 1 if str_ < 9 else 9
                int_ = int_ - 1 if int_ > 1 else 1
            elif content == "a":
                agi_ = agi_ + 1 if agi_ < 9 else 9
                luk_ = luk_ - 1 if luk_ > 1 else 1
            elif content == "v":
                vit_ = vit_ + 1 if vit_ < 9 else 9
                dex_ = dex_ - 1 if dex_ > 1 else 1
            elif content == "i":
                int_ = int_ + 1 if int_ < 9 else 9
                str_ = str_ - 1 if str_ > 1 else 1
            elif content == "d":
                dex_ = dex_ + 1 if dex_ < 9 else 9
                vit_ = vit_ - 1 if vit_ > 1 else 1
            elif content == "l":
                luk_ = luk_ + 1 if luk_ < 9 else 9
                agi_ = agi_ - 1 if agi_ > 1 else 1
            if content is not None:
                self.window.screen.blit(create_char, rect1)
                pygame.draw.polygon(self.window.screen, color,
                                    [str_idx[str_], agi_idx[agi_], dex_idx[dex_], int_idx[int_], luk_idx[luk_],
                                     vit_idx[vit_]])
                self.window.screen.blit(self.window.font.render(str(str_), True, Black), (725, 253))
                self.window.screen.blit(self.window.font.render(str(agi_), True, Black), (725, 269))
                self.window.screen.blit(self.window.font.render(str(vit_), True, Black), (725, 286))
                self.window.screen.blit(self.window.font.render(str(int_), True, Black), (725, 302))
                self.window.screen.blit(self.window.font.render(str(dex_), True, Black), (725, 318))
                self.window.screen.blit(self.window.font.render(str(luk_), True, Black), (725, 334))
                self.window.screen.blit(self.window.font.render(name, True, Black), (293, 460))
                self.window.screen.blit(stand_char, rect2)
                pygame.display.update()
            if content == "esc":
                return [str_, agi_, vit_, int_, dex_, luk_]

    def run(self, city):
        idx = True
        while idx:
            self.window.set_bg_image(os.path.join("BG_Image", city + "_BG.png"), 255)
            self.window.play_bgm(os.path.join("BG_Music", city + ".mp3"))
            self.window.set_sit_char(self.Char_obj.sit_img_path, (self.window.width * 0.4, self.window.height * 0.55))
            self.window.set_status_window(self.Char_obj)
            self.window.set_text_block(self.window.screen, self.Char_obj.char_name, (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60))
            self.window.reset_chat_message()
            self.window.set_chat_window(["嗨, " + self.Char_obj.char_name,
                                         "你的位置在: " + city,
                                         "按下 [A] 到人物素質介面",
                                         "         [I] 到物品介面",
                                         "         [K] 前往戰鬥",
                                         "         [Esc] 回主畫面"], [Green, Green, Green, Green, Green, Green])
            pygame.display.update()
            idx = self.city_standby()

    def city_standby(self):
        while True:
            self.window.clock.tick(self.window.fps)
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
            self.window.create_health_bar(self.window.screen, self.Char_obj, (self.window.width * 0.4, self.window.height * 0.55 + 50))
            pygame.display.update()


