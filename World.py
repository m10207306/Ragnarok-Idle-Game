import os, math                                     # Built-in Library
import Character, Battle_Utility, Map_Database              # 自己的Code
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
        self.current_pos = None
        self.attack_fps = 60
        self.window.set_bg_image(os.path.join("BG_Image", "Login_BG.png"), 200)
        # 清理背景跟重置背景
        rect = self.window.set_message_box(self.window.background.get_rect().center, ["請輸入角色名稱: (英文)"])
        # return message box 的 rect address
        name = ""
        while name == "":
            name = self.window.get_cmd(Black, pygame.Rect(rect.center[0] - 126, rect.center[1] - 11, 252, 22))

        ini_ability = self.initialize_ability(name)         # 設定初始素質
        self.Char_obj = Character.CharacterClass(name, ini_ability)

    def initialize_ability(self, name):
        str_, agi_, vit_, int_, dex_, luk_ = 5, 5, 5, 5, 5, 5
        win_sur, rect = self.window.create_ability_initial_win([str_, agi_, vit_, int_, dex_, luk_], name)
        rect.center = self.window.screen.get_rect().center
        self.window.screen.blit(win_sur, rect)
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
            elif content == "esc":
                str_, agi_, vit_, int_, dex_, luk_ = 5, 5, 5, 5, 5, 5
            if content is not None:
                win_sur, _ = self.window.create_ability_initial_win([str_, agi_, vit_, int_, dex_, luk_], name)
                self.window.screen.blit(win_sur, rect)
                pygame.display.update()
            if content == "enter":
                return [str_, agi_, vit_, int_, dex_, luk_]

    def transfer_station(self, map_idx):
        # 轉運站：基本上要切換場景的時候都透過這Function，並且控制背景與BGM
        # 這邊也會判斷是否地圖有做切換，如果沒做BGM就不會重新播放
        # 如果map_idx被設定為None代表要回到主畫面
        # 這邊也會判斷接下來要前往的地圖是城市還是原野，原野具有戰鬥功能
        idx = True
        while idx:
            if map_idx is None:         # 回到主畫面
                self.window.interlude_black_window()
                break
            map_data = Map_Database.map_data[map_idx]
            if self.current_pos != map_idx:
                self.window.interlude_black_window()
                self.window.set_bg_image(os.path.join("BG_Image", map_data[0] + ".png"), 255)
                self.window.play_bgm(os.path.join("BG_Music", map_data[0] + ".mp3"))
                self.current_pos = map_idx
            if map_data[2] == 1:
                idx, map_idx = self.city_run(map_idx)
            elif map_data[2] == 2:
                idx, map_idx = self.field_run(map_idx)

    def city_run(self, map_idx):
        idx = True
        map_data = Map_Database.map_data[map_idx]
        while idx:
            self.window.set_sit_char(self.Char_obj.sit_img_path,
                                     (self.window.width * 0.4, self.window.height * 0.55))
            self.window.set_text_block(self.window.screen, self.Char_obj.char_name,
                                       (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60))
            self.window.reset_chat_message()
            self.window.set_chat_window(["嗨, " + self.Char_obj.char_name,
                                         "你的位置在: " + map_data[1],
                                         "按下 [A] 到人物素質介面",
                                         "         [I] 到物品介面",
                                         "         [M] 地圖移動",
                                         "         [Esc] 回主畫面"], [Green, Green, Green, Green, Green, Green])
            pygame.display.update()
            idx, new_idx = self.city_standby(map_idx)

            if (not idx) and (new_idx != map_idx):  # Case1: 換地圖 -> 回到transfer station並回傳新的map_idx
                return True, new_idx
            if (not idx) and (new_idx is None):     # Case2: 離開遊戲回到主畫面 -> 回到transfer station並中斷，回到更上層的Main
                return False, None
            if idx and (new_idx == map_idx):        # Case3: 保持在這個地圖，重置畫面，通常就是idx是True，new_idx等於map_idx
                continue

    def city_standby(self, map_idx):
        while True:
            self.window.clock.tick(self.window.fps)
            content = self.window.get_key()
            if content == "a":
                print("\n>> Attribute Page")
                self.ability_page()
                return True, map_idx
            elif content == "i":
                print("\n>> Item Page")
                return True, map_idx
            elif content == "m":
                print("\n>> Moving")
                return False, 1                     # 因為還沒完成地圖網路，預設切換至prt_fild08
            elif content == "esc":
                print("\n>> Exit")
                return False, None

            self.window.set_status_window(self.Char_obj)                        # 更新左上角狀態欄
            self.window.create_health_bar(self.window.screen, self.Char_obj,    # 更新hp/sp bar
                                          (self.window.width * 0.4, self.window.height * 0.55 + 50))
            pygame.display.update()

    def field_run(self, map_idx):
        idx = True
        map_data = Map_Database.map_data[map_idx]
        while idx:
            self.window.set_status_window(self.Char_obj)
            self.window.reset_chat_message()
            self.window.set_chat_window(["你的位置在: " + map_data[1],
                                         "按 [A] 開始戰鬥",
                                         "     [M] 地圖移動",
                                         "     [Esc] 回主畫面"], [Green, Green, Green, Green])
            pygame.display.update()
            idx, new_idx = self.field_standby(map_idx)
            if (not idx) and (new_idx != map_idx):      # 切換地圖
                return True, new_idx
            if (not idx) and (new_idx is None):         # 回主畫面
                return False, None
            if idx and (new_idx == map_idx):            # 保持目前地圖
                continue

    def field_standby(self, map_idx):
        char_pos = (self.window.width * 0.4, self.window.height * 0.55)
        char_name_pos = (char_pos[0], char_pos[1] - 70)
        char_health_bar_pos = (char_pos[0], char_pos[1] + 50)
        char_group = pygame.sprite.Group()
        char_animate_obj = Battle_Utility.Animate(self.window,
                                                  self.Char_obj.standby_img_path,
                                                  self.Char_obj.standby_img_path,
                                                  self.Char_obj.dead_img_path,
                                                  char_pos)
        char_group.add(char_animate_obj)
        count = 1
        while True:
            self.window.clock.tick(self.attack_fps)
            content = self.window.get_key()
            if content == "esc":
                return False, None
            elif content == "a":
                self.field_attack(map_idx)
                return True, map_idx
            elif content == "m":
                print("Map Moving in field")
                return False, 0             # 因為還沒完成地圖網路，預設回到普隆德拉
            if count % 6 == 0:
                if count == 6:              # 如果沒有這行，逃離戰鬥時動畫會有一瞬間的斷層，因為clear需要根據上一次的draw來clear，但是第一次是沒有得clear的
                    self.window.screen.blit(self.window.background.subsurface(char_animate_obj.rect), char_animate_obj.rect)
                else:
                    char_group.clear(self.window.screen, self.window.background)
                char_group.update(1, 255)
                char_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
                self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
                pygame.display.update()
            count += 1

    def field_attack(self, map_idx):
        map_data = Map_Database.map_data[map_idx]
        self.window.reset_chat_message()
        self.window.set_chat_window(["你的位置在: " + map_data[1],
                                     "按 [Esc] 逃離戰鬥"], [Green, Green])
        pygame.display.update()
        # 這裡還缺個Random怪物的部分
        monster = Character.MonsterClass(0)

        char_pos = (self.window.width * 0.4, self.window.height * 0.55)
        mons_pos = (self.window.width * 0.6, self.window.height * 0.55)
        char_name_pos = (char_pos[0], char_pos[1] - 70)
        mons_name_pos = (mons_pos[0], mons_pos[1] - 70)
        char_health_bar_pos = (char_pos[0], char_pos[1] + 50)
        char_animate_group = pygame.sprite.Group()
        mons_animate_group = pygame.sprite.Group()
        damage_group = pygame.sprite.Group()
        Battle_Utility.Damage.AllGroup = damage_group

        char_animate = Battle_Utility.Animate(self.window,
                                              self.Char_obj.standby_img_path,
                                              self.Char_obj.attack_img_path,
                                              self.Char_obj.dead_img_path,
                                              char_pos,
                                              self.Char_obj,
                                              monster,
                                              (mons_pos[0], mons_pos[1] - 110))
        char_animate_group.add(char_animate)

        mons_animate = Battle_Utility.Animate(self.window,
                                              monster.standby_img_path,
                                              monster.attack_img_path,
                                              monster.dead_img_path,
                                              mons_pos,
                                              monster,
                                              self.Char_obj,
                                              (char_pos[0], char_pos[1] - 110))
        mons_animate_group.add(mons_animate)

        # Show出戰鬥的分析數據(命中率、迴避率等)
        char_hit_percent = round(self.Char_obj.attribute.hit / (monster.attribute.flee + 100), 2) * 100
        mons_hit_percent = round(monster.attribute.hit / (self.Char_obj.attribute.flee + 100), 2) * 100
        char_defence_ratio = round((4000 + self.Char_obj.attribute.total_defence) / (4000 + self.Char_obj.attribute.total_defence * 10), 2)
        mons_defence_ratio = round((4000 + monster.attribute.total_defence) / (4000 + monster.attribute.total_defence * 10), 2)
        char_damage_range = [round(self.Char_obj.attribute.total_atk[0] * mons_defence_ratio),
                             round(self.Char_obj.attribute.total_atk[1] * mons_defence_ratio)]
        mons_damage_range = [round(monster.attribute.total_atk[0] * char_defence_ratio),
                             round(monster.attribute.total_atk[1] * char_defence_ratio)]

        self.window.set_chat_window(["角色命中率: " + str(char_hit_percent) + "%",
                                     "角色傷害範圍: " + str(char_damage_range[0]) + " - " + str(char_damage_range[1]),
                                     "魔物命中率: " + str(mons_hit_percent) + "%",
                                     "魔物傷害範圍: " + str(mons_damage_range[0]) + " - " + str(mons_damage_range[1]),
                                     "角色Base_Exp: " + str(self.Char_obj.base_exp) + ", 下一級所需: " + str(self.Char_obj.target_base_exp),
                                     "角色Job_Exp: " + str(self.Char_obj.job_exp) + ", 下一級所需: " + str(self.Char_obj.target_job_exp),
                                     "怪物Base_Exp: " + str(monster.base_exp) + ", Job_Exp: " + str(monster.job_exp)],
                                    [Green, Green, Green, Green, Green, Green, Green])

        # 怪物出場(由實轉虛)，角色待機，目標一秒完成登場
        count = 1
        alpha = 255 - 120
        mons_name_rect = None
        while True:
            self.window.clock.tick(self.attack_fps)
            self.window.get_key()
            if count > 36:
                break
            if count % 6 == 0:
                if count == 6:
                    rect = pygame.Rect(0, 0, 200, 200)
                    rect.center = char_pos
                    self.window.screen.blit(self.window.background.subsurface(pygame.Rect(rect)), rect)
                else:  # 當第一次呼叫clear時不會有動作，因為他是根據上一次draw的內容做clear，所以才需要有上面的情境
                    char_animate_group.clear(self.window.screen, self.window.background)
                char_animate_group.update(1, 255)
                char_animate_group.draw(self.window.screen)
                mons_animate_group.clear(self.window.screen, self.window.background)
                mons_animate_group.update(1, alpha)
                mons_animate_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
                mons_name_rect = self.window.set_text_block(self.window.screen, "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name, mons_name_pos)
                self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
                alpha += 20
                pygame.display.update()
            count += 1

        # 戰鬥開始
        mons_dead = False
        char_dead = False
        char_move_frq = math.floor(self.attack_fps / self.Char_obj.attribute.att_frq / char_animate.image_count)
        mons_move_frq = math.floor(self.attack_fps / monster.attribute.att_frq / mons_animate.image_count)
        count = 1
        while True:
            self.window.clock.tick(self.attack_fps)
            content = self.window.get_key()
            print(self.window.clock.get_fps())
            if content == "esc":                    # 逃離戰鬥，清除傷害數值、怪物動畫、怪物名稱
                damage_group.clear(self.window.screen, self.window.background)
                mons_animate_group.clear(self.window.screen, self.window.background)
                self.window.screen.blit(self.window.background.subsurface(mons_name_rect), mons_name_rect)
                pygame.display.update()
                return

            # 角色攻擊動畫
            if count % char_move_frq == 0:
                char_animate_group.clear(self.window.screen, self.window.background)
                char_animate_group.update(2, 255)
                char_animate_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
                self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
            # 怪物攻擊動畫
            if count % mons_move_frq == 0:
                mons_animate_group.clear(self.window.screen, self.window.background)
                mons_animate_group.update(2, 255)
                mons_animate_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name, mons_name_pos)

            # 傷害動畫
            damage_group.clear(self.window.screen, self.window.background)
            damage_group.update()
            damage_group.draw(self.window.screen)
            self.window.set_status_window(self.Char_obj)
            pygame.display.update()

            # 判斷生死
            if monster.hp <= 0:
                mons_dead = True
                break
            if self.Char_obj.hp <= 0:
                self.Char_obj.hp = 0
                char_dead = True
                break
            count += 1

        # 死亡動畫
        count = 1
        alpha = 255
        while True:
            self.window.clock.tick(self.attack_fps)  # 保持使用attack_fps是因為要確保傷害數字速率一致
            self.window.get_key()
            if count > 36:
                break
            if count % 6 == 0:
                if mons_dead:
                    mons_animate_group.clear(self.window.screen, self.window.background)
                    mons_animate_group.update(3, alpha)
                    mons_animate_group.draw(self.window.screen)
                    char_animate_group.clear(self.window.screen, self.window.background)
                    char_animate_group.update(1, 255)
                    char_animate_group.draw(self.window.screen)
                if char_dead:
                    mons_animate_group.clear(self.window.screen, self.window.background)
                    mons_animate_group.update(1, 255)
                    mons_animate_group.draw(self.window.screen)
                    char_animate_group.clear(self.window.screen, self.window.background)
                    char_animate_group.update(3, 255)
                    char_animate_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
                self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
                alpha -= 20
            damage_group.clear(self.window.screen, self.window.background)
            damage_group.update()
            damage_group.draw(self.window.screen)
            self.window.set_status_window(self.Char_obj)
            pygame.display.update()
            count += 1

        # 暫停(結算？)畫面
        center = self.window.background.get_rect().center
        count = 1
        rect = None
        if mons_dead:
            self.Char_obj.get_exp(monster.base_exp, monster.job_exp)
            rect = self.window.set_message_box((center[0], center[1] - 125),
                                               ["============== 勝利！！ ==============",
                                                " ",
                                                "                           請按任意鍵繼續"])
            self.window.screen.blit(self.window.background.subsurface(mons_name_rect), mons_name_rect)  # 清掉怪物名稱
        if char_dead:
            self.Char_obj.exp_punish()
            rect = self.window.set_message_box((center[0], center[1] - 125),
                                               ["============== 失敗！！ ==============",
                                                " ",
                                                "                           請按任意鍵繼續"])
        while True:
            self.window.clock.tick(self.attack_fps)
            content = self.window.get_key()
            if content is not None:
                if char_dead:
                    self.Char_obj.respawn()
                self.window.screen.blit(self.window.background.subsurface(rect), rect)  # 清除message_box
                pygame.display.update()
                return

            if count % 6 == 0:
                if mons_dead:
                    char_animate_group.clear(self.window.screen, self.window.background)
                    char_animate_group.update(1, 255)
                    char_animate_group.draw(self.window.screen)
                if char_dead:
                    mons_animate_group.clear(self.window.screen, self.window.background)
                    mons_animate_group.update(1, 255)
                    mons_animate_group.draw(self.window.screen)
                self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
                self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
                self.window.set_status_window(self.Char_obj)
                pygame.display.update()
            count += 1

    def ability_page(self):
        ability_sur, rect = self.window.create_equip_ability_win(self.Char_obj)
        rect.topleft = (20, 200)
        self.window.screen.blit(ability_sur, rect)
        self.window.reset_chat_message()
        self.window.set_chat_window(["---------- 人物素質與裝備操作頁面 ----------",
                                     "按下 [Esc] 回上一層"], [Green, Green])
        pygame.display.update()
        while True:
            self.window.clock.tick(self.attack_fps)
            content = self.window.get_key()
            if content == "esc":
                self.window.screen.blit(self.window.background.subsurface(rect), rect)
                pygame.display.update()
                return
