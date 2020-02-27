# -*- coding: utf-8 -*-
import os                                      # Python Built-in Library
import World, Graphic, Animate_Utility         # 自己的Code
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來


Black = [0, 0, 0]
White = [255, 255, 255]
Select_Color = [209, 222, 250]

class Ragnarok:
    def __init__(self):
        self.window = Graphic.WindowClass()

    def run(self):
        idx = True
        while idx:
            self.window.play_bgm(os.path.join("BG_Music", "Login.mp3"))
            idx = self.standby()

    def standby(self):
        # fps大概58-60
        self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.png"), 200)
        black_surf = pygame.Surface(self.window.background.get_size())
        black_surf.fill((0, 0, 0))

        info_group = pygame.sprite.Group()
        text_group = pygame.sprite.Group()
        btn_group = pygame.sprite.Group()
        ptr_group = pygame.sprite.Group()
        txt_win = self.window.generate_txt_win(300, 200)
        title_bar, btn_bar = self.window.generate_titlebar(300)
        self.window.set_text(title_bar, ["選擇遊戲伺服器"], [Black], (15, 0))
        window_center = self.window.background.get_rect().center

        info_group.add(Animate_Utility.InfoWindowAnimate(txt_win, self.window.background.get_rect().center))
        str1 = " 開始新遊戲 - 9487人                          "
        text_group.add(Animate_Utility.TextAnimate(self.window.font.render(str1, True, Black), str1, (window_center[0] - txt_win.get_size()[0] / 2 + 12, window_center[1] - txt_win.get_size()[1] / 2 + 5)))
        str2 = " 載入舊檔 - 9527人                            "
        text_group.add(Animate_Utility.TextAnimate(self.window.font.render(str2, True, Black), str2, (window_center[0] - txt_win.get_size()[0] / 2 + 12, window_center[1] - txt_win.get_size()[1] / 2 + 22)))
        str3 = " 離開遊戲 - 0人                               "
        text_group.add(Animate_Utility.TextAnimate(self.window.font.render(str3, True, Black), str3, (window_center[0] - txt_win.get_size()[0] / 2 + 12, window_center[1] - txt_win.get_size()[1] / 2 + 39)))
        btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_ok_template, (window_center[0] + txt_win.get_size()[0] / 2 - 32, window_center[1] + txt_win.get_size()[1] / 2 + 14)))
        ptr_group.add(Animate_Utility.PointerAnimate(self.window.pointer_template, pygame.mouse.get_pos(), 7))

        opt_select = None
        while True:
            self.window.clock.tick(self.window.fps)
            enter = None
            key, key_type, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                return False

            info_group.clear(self.window.screen, self.window.background)
            ptr_group.clear(self.window.screen, black_surf)                 # 因為登入畫面的background是半透明的，需要墊一層黑色的才可以蓋掉滑鼠
            ptr_group.clear(self.window.screen, self.window.background)

            info_group.update(None, None)
            ptr_group.update(pygame.mouse.get_pos())

            ptr_tip_pos = ptr_group.sprites()[0].rect.topleft               # 因為mouse.get_pos不等於系統中滑鼠的尖端，所以要用這比較迂迴的方法

            for idx, text in enumerate(text_group):
                if ("down" in mouse_type or "click" in mouse_type) and text.rect.collidepoint(ptr_tip_pos): # 確認是否有滑鼠左鍵按下，並且滑鼠尖端在文字sprite的區域
                    opt_select = idx
                    text.update(self.window.font.render(text.text, True, Black, Select_Color), text.text, None)
                    group2 = text_group.copy()
                    group2.remove(text)
                    for text2 in group2:                                    # 如果有其中一個sprite被按下，其他的要reset背景色
                        text2.update(self.window.font.render(text2.text, True, Black), text2.text, None)

            if len(mouse_type) == 0 and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):  # 滑鼠在按鍵上，但是沒按
                btn_group.update(2)
            elif "down" in mouse_type and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):     # 滑鼠按下按鍵
                btn_group.update(3)
            elif ("up" in mouse_type or "click" in mouse_type) and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):               # 滑鼠在按鍵上放開
                enter = True
            else:
                btn_group.update(1)

            self.window.screen.blit(title_bar, (window_center[0] - txt_win.get_size()[0] / 2, window_center[1] - txt_win.get_size()[1]/2 - 17))
            self.window.screen.blit(btn_bar, (window_center[0] - txt_win.get_size()[0] / 2, window_center[1] + txt_win.get_size()[1]/2))
            info_group.draw(self.window.screen)
            text_group.draw(self.window.screen)
            btn_group.draw(self.window.screen)
            ptr_group.draw(self.window.screen)
            pygame.display.update()

            if opt_select == 0 and enter:
                name, ability_list = self.initialize_ability()
                world_obj = World.WorldClass(self.window, name, ability_list)
                self.window.interlude_black_window()
                world_obj.transfer_station(0)       # 預設前往普隆德拉
                print(">> Create Character")
                return True
            elif opt_select == 1 and enter:
                print(">> Load Game")
                return False
            elif opt_select == 2 and enter:
                print(">> See Ya!")
                return False

    def initialize_ability(self):
        # fps大概50...應該是因為每次要把整個視窗重新貼上去，所以會變慢，除非clear不再對整個win_make做
        # 如果哪天有空弄的話: 反過來不clear整個win_make，反過來對裡面的小sprite做clear，然後用win_make當背景去clear
        ability_list = [5, 5, 5, 5, 5, 5]         # str, agi, dex, vit, luk, int
        win_sur = self.window.create_ability_initial_win(ability_list)
        black_surf = pygame.Surface(self.window.screen.get_size())
        black_surf.fill(Black)
        name_topleft = (288, 457)
        str_btn = [pygame.image.load(os.path.join("Info_Image", "arw-str0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-str1.png")).convert_alpha()]
        agi_btn = [pygame.image.load(os.path.join("Info_Image", "arw-agi0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-agi1.png")).convert_alpha()]
        vit_btn = [pygame.image.load(os.path.join("Info_Image", "arw-vit0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-vit1.png")).convert_alpha()]
        dex_btn = [pygame.image.load(os.path.join("Info_Image", "arw-dex0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-dex1.png")).convert_alpha()]
        int_btn = [pygame.image.load(os.path.join("Info_Image", "arw-int0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-int1.png")).convert_alpha()]
        luk_btn = [pygame.image.load(os.path.join("Info_Image", "arw-luk0.png")).convert_alpha(), None,
                   pygame.image.load(os.path.join("Info_Image", "arw-luk1.png")).convert_alpha()]

        info_group = pygame.sprite.Group()
        text_group = pygame.sprite.Group()
        ptr_group = pygame.sprite.Group()
        btn_group = pygame.sprite.Group()
        ability_btn_group = pygame.sprite.Group()

        info_group.add(Animate_Utility.InfoWindowAnimate(win_sur, self.window.screen.get_rect().center))
        text_group.add(Animate_Utility.TextAnimate(self.window.font.render("Key in", True, Black), "Key in", name_topleft))
        ptr_group.add(Animate_Utility.PointerAnimate(self.window.pointer_template, pygame.mouse.get_pos(), 7))
        btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_ok_template, (760, 541)))
        str_pos = (512, 278)
        ability_btn_group.add(Animate_Utility.ButtonAnimate(str_btn, str_pos))
        ability_btn_group.add(Animate_Utility.ButtonAnimate(agi_btn, (str_pos[0] - 81, str_pos[1] + 55)))
        ability_btn_group.add(Animate_Utility.ButtonAnimate(dex_btn, (str_pos[0] - 81, str_pos[1] + 145)))
        ability_btn_group.add(Animate_Utility.ButtonAnimate(vit_btn, (str_pos[0] + 80, str_pos[1] + 55)))
        ability_btn_group.add(Animate_Utility.ButtonAnimate(luk_btn, (str_pos[0] + 80, str_pos[1] + 145)))
        ability_btn_group.add(Animate_Utility.ButtonAnimate(int_btn, (str_pos[0],      str_pos[1] + 200)))

        name = "Key in"
        while True:
            self.window.clock.tick(60)
            enter = None
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                return False

            for c in key:
                if name == "Key in":
                    name = ""
                if c == "backspace":
                    name = name[:-1]
                elif len(c) > 1:        # 迴避掉一些非單字元的東西 (比如return, up, down之類東東)
                    continue
                else:
                    if len(name) < 16:
                        name += c

            info_group.clear(self.window.screen, self.window.background)
            ptr_group.clear(self.window.screen, black_surf)  # 因為登入畫面的background是半透明的，需要墊一層黑色的才可以蓋掉滑鼠
            ptr_group.clear(self.window.screen, self.window.background)

            ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = ptr_group.sprites()[0].rect.topleft

            text_group.update(self.window.font.render(name, True, Black), name, name_topleft)
            for idx, abi_btn in enumerate(ability_btn_group.sprites()):
                if ("click" in mouse_type or "down" in mouse_type) and abi_btn.rect.collidepoint(ptr_tip_pos):
                    abi_btn.update(3)
                    ability_list[idx] = ability_list[idx] + 1 if ability_list[idx] < 9 else 9
                    ability_list[5-idx] = ability_list[5-idx] - 1 if ability_list[5-idx] > 1 else 1
                else:
                    abi_btn.update(1)
            win_sur = self.window.create_ability_initial_win(ability_list)
            info_group.update(win_sur, None)

            if len(mouse_type) == 0 and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):  # 滑鼠在按鍵上，但是沒按
                btn_group.update(2)
            elif "down" in mouse_type and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):     # 滑鼠按下按鍵
                btn_group.update(3)
            elif ("up" in mouse_type or "click" in mouse_type) and btn_group.sprites()[0].rect.collidepoint(ptr_tip_pos):               # 滑鼠在按鍵上放開
                enter = True
            else:
                btn_group.update(1)

            info_group.draw(self.window.screen)
            text_group.draw(self.window.screen)
            btn_group.draw(self.window.screen)
            ability_btn_group.draw(self.window.screen)
            ptr_group.draw(self.window.screen)

            pygame.display.update()

            if enter:
                return name, ability_list


if __name__ == "__main__":
    RO = Ragnarok()
    RO.run()
