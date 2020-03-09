import os, math, random                                     # Python Built-in Library
import Character, Animate_Utility, Map_Database             # 自己的Code
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 222, 0)


class WorldClass:
    def __init__(self, window_screen, name, ini_ability):
        self.window = window_screen
        self.current_pos = None
        self.Char_obj = Character.CharacterClass(name, ini_ability)
        # 一些幾乎必備的Animate Group存在這裏，避免每進去一個function要重做一次
        self.status_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(self.window.status_win_template, (0, 0)))
        self.mini_map_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        self.health_bar_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        self.chat_input_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        self.ptr_group = pygame.sprite.Group(Animate_Utility.PointerAnimate(self.window.pointer_template, pygame.mouse.get_pos(), 7))

        pos = [(self.window.width - 350, self.window.height -  60),
               (self.window.width - 200, self.window.height -  60),
               (self.window.width -  50, self.window.height -  60),
               (self.window.width - 350, self.window.height - 185),
               (self.window.width - 200, self.window.height - 185),
               (self.window.width -  50, self.window.height - 185)]
        pos2 = [(pos[0][0], pos[0][1] + 45),
                (pos[1][0], pos[1][1] + 45),
                (pos[2][0], pos[2][1] + 45),
                (pos[3][0], pos[3][1] + 45),
                (pos[4][0], pos[4][1] + 45),
                (pos[5][0], pos[5][1] + 45)]
        print(pos)
        print(pos2)
        self.console_btn_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[2], pos[0]))  # info
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[3], pos[1]))    # item
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[1], pos[2]))    # equip
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[0], pos[3]))    # battle
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[4], pos[4]))    # map
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[5], pos[5]))    # skill
        self.console_text_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("角色資訊", pos2[0]), pos2[0]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("物品資訊", pos2[1]), pos2[1]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("裝備資訊", pos2[2]), pos2[2]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("戰鬥開關", pos2[3]), pos2[3]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("地圖開關", pos2[4]), pos2[4]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block("技能資訊", pos2[5]), pos2[5]))

    def transfer_station(self, map_idx):
        # 轉運站：基本上要切換場景的時候都透過這Function，並且控制背景與BGM
        # 這邊也會判斷是否地圖有做切換，如果沒做BGM就不會重新播放
        # 如果map_idx被設定為None代表要回到主畫面
        # 這邊也會判斷接下來要前往的地圖是城市還是原野，原野具有戰鬥功能
        while True:
            if map_idx is None:         # 回到主畫面
                self.window.interlude_black_window()
                break
            map_data = Map_Database.map_data[map_idx]
            if self.current_pos != map_idx:                     # 換地圖時：過場、換bgm、更新目前位置
                self.window.interlude_black_window()
                if self.current_pos is None:
                    self.window.play_bgm(os.path.join("BG_Music", map_data[4] + ".mp3"))
                elif self.current_pos is not None:
                    if Map_Database.map_data[self.current_pos][4] != map_data[4]:           # 如果正在播放的BGM跟預計前往不同才重新播放
                        self.window.play_bgm(os.path.join("BG_Music", map_data[4] + ".mp3"))
                self.current_pos = map_idx
            if map_data[3] == 1:
                map_idx = self.city_standby(map_idx)
            elif map_data[3] == 2:
                map_idx = self.field_run(map_idx)

            # Case1: new_idx = current_pos 保持在這個地圖，重置畫面
            # Case2: map_idx != current_pos 換地圖 -> 回到transfer station以new_idx跑新地圖
            # Case3: new_idx = None 離開遊戲回到主畫面 -> 回到transfer station並中斷，回到更上層的Main

    def city_standby(self, map_idx):
        map_data = Map_Database.map_data[map_idx]
        self.window.set_bg_image(os.path.join("BG_Image", map_data[1] + ".png"), 255)

        text_group = pygame.sprite.Group()

        char_sit_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.image.load(self.Char_obj.sit_img_path).convert_alpha(), (self.window.width * 0.4, self.window.height * 0.55)))
        status_win = self.window.get_status_win(self.Char_obj)
        self.status_group.update(status_win, self.window.status_win_template.get_rect().center)
        mini_map_win = self.window.get_map_icon(os.path.join("Map_Image", map_data[1] + ".png"))
        self.mini_map_group.update(mini_map_win, (self.window.width - mini_map_win.get_size()[0]/2, mini_map_win.get_size()[1]/2))
        self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), (self.window.width * 0.4, self.window.height * 0.55 + 50))
        self.chat_input_group.update(self.window.chat_input_template, (self.window.chat_input_template.get_size()[0]/2, self.window.height - self.window.chat_input_template.get_size()[1]/2))
        self.ptr_group.update(pygame.mouse.get_pos())

        chat = self.window.get_chat_win(["Hi, " + self.Char_obj.char_name,
                                                       "你的位置在: " + map_data[2],
                                                       "按下 [A]ttribute 到人物素質介面",
                                                       "     [I]tem      到物品介面",
                                                       "     [M]ove      地圖移動",
                                                       "     [Esc]       回主畫面"], [Green, Green, Green, Green, Green, Green])
        chat_room_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(chat, (chat.get_size()[0] / 2, self.window.height - chat.get_size()[1] / 2)))
        name_text = self.window.get_text_block(self.Char_obj.char_name, (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60))
        text_group.add(Animate_Utility.InfoWindowAnimate(name_text, (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60)))

        while True:
            self.window.clock.tick(self.window.fps)
            print(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                return None

            char_sit_group.clear(self.window.screen, self.window.background)
            self.status_group.clear(self.window.screen, self.window.background)
            self.mini_map_group.clear(self.window.screen, self.window.background)
            self.health_bar_group.clear(self.window.screen, self.window.background)
            chat_room_group.clear(self.window.screen, self.window.background)
            self.chat_input_group.clear(self.window.screen, self.window.background)
            self.console_btn_group.clear(self.window.screen, self.window.background)
            self.ptr_group.clear(self.window.screen, self.window.background)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            self.status_group.update(self.window.get_status_win(self.Char_obj), None)
            self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
            self.console_btn_group.update(ptr_tip_pos, mouse_type)

            char_sit_group.draw(self.window.screen)
            self.status_group.draw(self.window.screen)
            self.mini_map_group.draw(self.window.screen)
            self.health_bar_group.draw(self.window.screen)
            chat_room_group.draw(self.window.screen)
            text_group.draw(self.window.screen)
            self.chat_input_group.draw(self.window.screen)
            self.console_btn_group.draw(self.window.screen)
            self.console_text_group.draw(self.window.screen)
            self.ptr_group.draw(self.window.screen)

            pygame.display.update()

    def field_run(self, map_idx):
        return map_idx

    # def transfer_station(self, map_idx):
    #     # 轉運站：基本上要切換場景的時候都透過這Function，並且控制背景與BGM
    #     # 這邊也會判斷是否地圖有做切換，如果沒做BGM就不會重新播放
    #     # 如果map_idx被設定為None代表要回到主畫面
    #     # 這邊也會判斷接下來要前往的地圖是城市還是原野，原野具有戰鬥功能
    #     idx = True
    #     while idx:
    #         if map_idx is None:         # 回到主畫面
    #             self.window.interlude_black_window()
    #             break
    #         map_data = Map_Database.map_data[map_idx]
    #         if self.current_pos != map_idx:                     # 換地圖時：過場、換bgm、更新目前位置
    #             self.window.interlude_black_window()
    #             if self.current_pos is None:
    #                 self.window.play_bgm(os.path.join("BG_Music", map_data[4] + ".mp3"))
    #             elif self.current_pos is not None:
    #                 if Map_Database.map_data[self.current_pos][4] != map_data[4]:           # 如果正在播放的BGM跟預計前往不同才重新播放
    #                     self.window.play_bgm(os.path.join("BG_Music", map_data[4] + ".mp3"))
    #             self.current_pos = map_idx
    #         self.window.set_bg_image(os.path.join("BG_Image", map_data[1] + ".png"), 255)   # 考慮到地圖移動時按esc，固定每次回來都reset背景跟map icon
    #         self.window.set_map_icon(os.path.join("Map_Image", map_data[1] + ".png"))
    #         if map_data[3] == 1:
    #             idx, map_idx = self.city_run(map_idx)
    #         elif map_data[3] == 2:
    #             idx, map_idx = self.field_run(map_idx)
    #
    # def city_run(self, map_idx):
    #     while True:
    #         new_idx = self.city_standby(map_idx)
    #         if new_idx != map_idx:          # Case1: 換地圖 -> 回到transfer station並回傳新的map_idx
    #             return True, new_idx
    #         if new_idx is None:             # Case2: 離開遊戲回到主畫面 -> 回到transfer station並中斷，回到更上層的Main
    #             return False, None
    #         if new_idx == map_idx:          # Case3: 保持在這個地圖，重置畫面，通常就是idx是True，new_idx等於map_idx
    #             return True, map_idx
    #
    # def city_standby(self, map_idx):
    #     map_data = Map_Database.map_data[map_idx]
    #     animate_group = None
    #     name_pos = (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60)
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         if content == "a":
    #             print("\n>> Attribute Page")
    #             self.ability_page(animate_group, name_pos)
    #             return map_idx
    #         elif content == "i":
    #             print("\n>> Item Page")
    #             return map_idx
    #         elif content == "m":
    #             print("\n>> Map Moving in city")
    #             mov_idx = self.moving_page()
    #             if mov_idx is not None:
    #                 map_idx = len(Map_Database.map_data)-1 if mov_idx > len(Map_Database.map_data)-1 else mov_idx
    #                 map_idx = 0 if mov_idx < 0 else mov_idx
    #                 return map_idx
    #             else:
    #                 return map_idx
    #         elif content == "esc":
    #             print("\n>> Exit")
    #             return None
    #
    #         self.window.set_sit_char(self.Char_obj.sit_img_path,
    #                                  (self.window.width * 0.4, self.window.height * 0.55))
    #         self.window.set_text_block(self.window.screen, self.Char_obj.char_name,
    #                                    (self.window.width * 0.4 - 2, self.window.height * 0.55 - 60))
    #         self.window.reset_chat_message()
    #         self.window.set_chat_window(["Hi, " + self.Char_obj.char_name,
    #                                      "你的位置在: " + map_data[2],
    #                                      "按下 [A]ttribute 到人物素質介面",
    #                                      "     [I]tem      到物品介面",
    #                                      "     [M]ove      地圖移動",
    #                                      "     [Esc]       回主畫面"], [Green, Green, Green, Green, Green, Green])
    #         self.window.set_status_window(self.Char_obj)                        # 更新左上角狀態欄
    #         self.window.create_health_bar(self.window.screen, self.Char_obj,    # 更新hp/sp bar
    #                                       (self.window.width * 0.4, self.window.height * 0.55 + 50))
    #         pygame.display.update()
    #
    # def field_run(self, map_idx):
    #     while True:
    #         new_idx = self.field_standby(map_idx)
    #         if new_idx != map_idx:      # 切換地圖
    #             return True, new_idx
    #         if new_idx is None:         # 回主畫面
    #             return False, None
    #         if new_idx == map_idx:            # 保持目前地圖，但是回到transform station重置BG與Map_icon
    #             return True, map_idx
    #
    # def field_standby(self, map_idx):
    #     map_data = Map_Database.map_data[map_idx]
    #     char_pos = (self.window.width * 0.4, self.window.height * 0.55)
    #     char_name_pos = (char_pos[0], char_pos[1] - 70)
    #     char_health_bar_pos = (char_pos[0], char_pos[1] + 50)
    #     char_group = pygame.sprite.Group()
    #     char_animate_obj = Animate_Utility.Animate(self.window,
    #                                               self.Char_obj.standby_img_path,
    #                                               self.Char_obj.standby_img_path,
    #                                               self.Char_obj.dead_img_path,
    #                                               char_pos)
    #     char_group.add(char_animate_obj)
    #     count = 1
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         if content == "esc":
    #             return None
    #         elif content == "a":
    #             self.ability_page(char_group, char_name_pos)
    #             return map_idx
    #         elif content == "f":
    #             self.field_attack(map_idx)
    #         elif content == "m":
    #             print("Map Moving in field")
    #             mov_idx = self.moving_page()
    #             if mov_idx is not None:
    #                 map_idx = len(Map_Database.map_data)-1 if mov_idx > len(Map_Database.map_data)-1 else mov_idx
    #                 map_idx = 0 if mov_idx < 0 else mov_idx
    #                 return map_idx
    #             else:
    #                 return map_idx
    #         if count % 6 == 0:
    #             if count == 6:              # 如果沒有這行，逃離戰鬥時動畫會有一瞬間的斷層，因為clear需要根據上一次的draw來clear，但是第一次是沒有得clear的
    #                 self.window.screen.blit(self.window.background.subsurface(char_animate_obj.rect), char_animate_obj.rect)
    #             else:
    #                 char_group.clear(self.window.screen, self.window.background)
    #             char_group.update(1, 255)
    #             char_group.draw(self.window.screen)
    #         self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #         self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #         self.window.reset_chat_message()
    #         self.window.set_chat_window(["你的位置在: " + map_data[2],
    #                                      "按 [F]ight      開始戰鬥",
    #                                      "   [A]ttribute  人物素質頁面",
    #                                      "   [M]ove       地圖移動",
    #                                      "   [Esc]        回主畫面"], [Green, Green, Green, Green, Green])
    #         self.window.set_status_window(self.Char_obj)
    #         pygame.display.update()
    #         count += 1
    #
    # def field_attack(self, map_idx):
    #     map_data = Map_Database.map_data[map_idx]
    #     self.window.reset_chat_message()
    #     self.window.set_chat_window(["你的位置在: " + map_data[2],
    #                                  "按 [Esc] 逃離戰鬥"], [Green, Green])
    #     pygame.display.update()
    #     monster = Character.MonsterClass(random.choice(map_data[7]))
    #
    #     char_pos = (self.window.width * 0.4, self.window.height * 0.55)
    #     mons_pos = (self.window.width * 0.6, self.window.height * 0.55)
    #     char_name_pos = (char_pos[0], char_pos[1] - 70)
    #     mons_name_pos = (mons_pos[0], mons_pos[1] - 70)
    #     char_health_bar_pos = (char_pos[0], char_pos[1] + 50)
    #     char_animate_group = pygame.sprite.Group()
    #     mons_animate_group = pygame.sprite.Group()
    #     damage_group = pygame.sprite.Group()
    #     Animate_Utility.Damage.AllGroup = damage_group
    #
    #     char_animate = Animate_Utility.Animate(self.window,
    #                                           self.Char_obj.standby_img_path,
    #                                           self.Char_obj.attack_img_path,
    #                                           self.Char_obj.dead_img_path,
    #                                           char_pos,
    #                                           self.Char_obj,
    #                                           monster,
    #                                           (mons_pos[0], mons_pos[1] - 110))
    #     char_animate_group.add(char_animate)
    #
    #     mons_animate = Animate_Utility.Animate(self.window,
    #                                           monster.standby_img_path,
    #                                           monster.attack_img_path,
    #                                           monster.dead_img_path,
    #                                           mons_pos,
    #                                           monster,
    #                                           self.Char_obj,
    #                                           (char_pos[0], char_pos[1] - 110))
    #     mons_animate_group.add(mons_animate)
    #
    #     # Show出戰鬥的分析數據(命中率、迴避率等)
    #     char_hit_percent = round(self.Char_obj.attribute.hit / (monster.attribute.flee + 100), 2) * 100
    #     mons_hit_percent = round(monster.attribute.hit / (self.Char_obj.attribute.flee + 100), 2) * 100
    #     char_defence_ratio = round((4000 + self.Char_obj.attribute.total_defence) / (4000 + self.Char_obj.attribute.total_defence * 10), 2)
    #     mons_defence_ratio = round((4000 + monster.attribute.total_defence) / (4000 + monster.attribute.total_defence * 10), 2)
    #     char_damage_range = [round(self.Char_obj.attribute.total_atk[0] * mons_defence_ratio),
    #                          round(self.Char_obj.attribute.total_atk[1] * mons_defence_ratio)]
    #     mons_damage_range = [round(monster.attribute.total_atk[0] * char_defence_ratio),
    #                          round(monster.attribute.total_atk[1] * char_defence_ratio)]
    #
    #     self.window.set_chat_window(["角色命中率: " + str(char_hit_percent) + "%",
    #                                  "角色傷害範圍: " + str(char_damage_range[0]) + " - " + str(char_damage_range[1]),
    #                                  "魔物命中率: " + str(mons_hit_percent) + "%",
    #                                  "魔物傷害範圍: " + str(mons_damage_range[0]) + " - " + str(mons_damage_range[1]),
    #                                  "角色Base_Exp: " + str(self.Char_obj.base_exp) + ", 下一級所需: " + str(self.Char_obj.target_base_exp),
    #                                  "角色Job_Exp: " + str(self.Char_obj.job_exp) + ", 下一級所需: " + str(self.Char_obj.target_job_exp),
    #                                  "怪物Base_Exp: " + str(monster.base_exp) + ", Job_Exp: " + str(monster.job_exp)],
    #                                 [Green, Green, Green, Green, Green, Green, Green])
    #
    #     # 怪物出場(由實轉虛)，角色待機，目標一秒完成登場
    #     count = 1
    #     alpha = 255 - 120
    #     mons_name_rect = None
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         self.window.get_key()
    #         if count > 36:
    #             break
    #         if count % 6 == 0:
    #             if count == 6:
    #                 rect = pygame.Rect(0, 0, 200, 200)
    #                 rect.center = char_pos
    #                 self.window.screen.blit(self.window.background.subsurface(pygame.Rect(rect)), rect)
    #             else:  # 當第一次呼叫clear時不會有動作，因為他是根據上一次draw的內容做clear，所以才需要有上面的情境
    #                 char_animate_group.clear(self.window.screen, self.window.background)
    #             char_animate_group.update(1, 255)
    #             char_animate_group.draw(self.window.screen)
    #             mons_animate_group.clear(self.window.screen, self.window.background)
    #             mons_animate_group.update(1, alpha)
    #             mons_animate_group.draw(self.window.screen)
    #             self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #             mons_name_rect = self.window.set_text_block(self.window.screen, "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name, mons_name_pos)
    #             self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #             alpha += 20
    #             pygame.display.update()
    #         count += 1
    #
    #     # 戰鬥開始
    #     mons_dead = False
    #     char_dead = False
    #     char_move_frq = math.floor(self.window.fps / self.Char_obj.attribute.att_frq / char_animate.image_count)
    #     mons_move_frq = math.floor(self.window.fps / monster.attribute.att_frq / mons_animate.image_count)
    #     count = 1
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         print(self.window.clock.get_fps())
    #         if content == "esc":                    # 逃離戰鬥，清除傷害數值、怪物動畫、怪物名稱
    #             damage_group.clear(self.window.screen, self.window.background)
    #             mons_animate_group.clear(self.window.screen, self.window.background)
    #             self.window.screen.blit(self.window.background.subsurface(mons_name_rect), mons_name_rect)
    #             pygame.display.update()
    #             return
    #
    #         # 角色攻擊動畫
    #         if count % char_move_frq == 0:
    #             char_animate_group.clear(self.window.screen, self.window.background)
    #             char_animate_group.update(2, 255)
    #             char_animate_group.draw(self.window.screen)
    #             self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #             self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #         # 怪物攻擊動畫
    #         if count % mons_move_frq == 0:
    #             mons_animate_group.clear(self.window.screen, self.window.background)
    #             mons_animate_group.update(2, 255)
    #             mons_animate_group.draw(self.window.screen)
    #             self.window.set_text_block(self.window.screen, "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name, mons_name_pos)
    #
    #         # 傷害動畫
    #         damage_group.clear(self.window.screen, self.window.background)
    #         damage_group.update()
    #         damage_group.draw(self.window.screen)
    #         self.window.set_status_window(self.Char_obj)
    #         pygame.display.update()
    #
    #         # 判斷生死
    #         if monster.hp <= 0:
    #             mons_dead = True
    #             break
    #         if self.Char_obj.hp <= 0:
    #             self.Char_obj.hp = 0
    #             char_dead = True
    #             break
    #         count += 1
    #
    #     # 死亡動畫
    #     count = 1
    #     alpha = 255
    #     while True:
    #         self.window.clock.tick(self.window.fps)  # 保持使用window.fps是因為要確保傷害數字速率一致
    #         self.window.get_key()
    #         if count > 36:
    #             break
    #         if count % 6 == 0:
    #             if mons_dead:
    #                 mons_animate_group.clear(self.window.screen, self.window.background)
    #                 mons_animate_group.update(3, alpha)
    #                 mons_animate_group.draw(self.window.screen)
    #                 char_animate_group.clear(self.window.screen, self.window.background)
    #                 char_animate_group.update(1, 255)
    #                 char_animate_group.draw(self.window.screen)
    #             if char_dead:
    #                 mons_animate_group.clear(self.window.screen, self.window.background)
    #                 mons_animate_group.update(1, 255)
    #                 mons_animate_group.draw(self.window.screen)
    #                 char_animate_group.clear(self.window.screen, self.window.background)
    #                 char_animate_group.update(3, 255)
    #                 char_animate_group.draw(self.window.screen)
    #                 self.window.set_text_block(self.window.screen,
    #                                            "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name,
    #                                            mons_name_pos)
    #             self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #             self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #             alpha -= 20
    #         damage_group.clear(self.window.screen, self.window.background)
    #         damage_group.update()
    #         damage_group.draw(self.window.screen)
    #         self.window.set_status_window(self.Char_obj)
    #         pygame.display.update()
    #         count += 1
    #
    #     # 暫停(結算？)畫面
    #     center = self.window.background.get_rect().center
    #     count = 1
    #     rect = None
    #     if mons_dead:
    #         self.Char_obj.get_exp(monster.base_exp, monster.job_exp)
    #         rect = self.window.set_message_box((center[0], center[1] - 125),
    #                                            ["============== 勝利！！ ==============",
    #                                             " ",
    #                                             "                           請按任意鍵繼續"])
    #         self.window.screen.blit(self.window.background.subsurface(mons_name_rect), mons_name_rect)  # 清掉怪物名稱
    #     if char_dead:
    #         self.Char_obj.exp_punish()
    #         rect = self.window.set_message_box((center[0], center[1] - 125),
    #                                            ["============== 失敗！！ ==============",
    #                                             " ",
    #                                             "                           請按任意鍵繼續"])
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         if content is not None:
    #             if char_dead:
    #                 self.Char_obj.respawn()
    #             self.window.screen.blit(self.window.background.subsurface(rect), rect)  # 清除message_box
    #             mons_animate_group.clear(self.window.screen, self.window.background)
    #             pygame.display.update()
    #             return
    #
    #         if count % 6 == 0:
    #             if mons_dead:
    #                 char_animate_group.clear(self.window.screen, self.window.background)
    #                 char_animate_group.update(1, 255)
    #                 char_animate_group.draw(self.window.screen)
    #             if char_dead:
    #                 mons_animate_group.clear(self.window.screen, self.window.background)
    #                 mons_animate_group.update(1, 255)
    #                 mons_animate_group.draw(self.window.screen)
    #                 self.window.set_text_block(self.window.screen,
    #                                            "Lv." + str(monster.base_level) + "   " + monster.mons_zh_name,
    #                                            mons_name_pos)
    #             self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #             self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #             self.window.set_status_window(self.Char_obj)
    #             pygame.display.update()
    #         count += 1
    #
    # def ability_page(self, animate_group, char_name_pos):   # 需要再傳入名稱位置是因為城鎮跟野外的角色高度不同
    #     ability_sur, rect = self.window.create_equip_ability_win(self.Char_obj)
    #     rect.topleft = (20, 200)
    #     ability_handle = self.Char_obj.ability
    #     char_pos = (self.window.width * 0.4, self.window.height * 0.55)
    #     char_health_bar_pos = (char_pos[0], char_pos[1] + 50)
    #     self.window.screen.blit(ability_sur, rect)
    #     self.window.reset_chat_message()
    #     self.window.set_chat_window(["---------- 人物素質與裝備操作頁面 ----------",
    #                                  "按下 [Esc] 回上一層",
    #                                  "加點按下：[S]tr, [A]gi, [V]it, [I]nt, [D]ex, [L]uk"], [Green, Green, Green])
    #     pygame.display.update()
    #     idx = None
    #     count = 1
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         if content == "s":
    #             idx = 0
    #         elif content == "a":
    #             idx = 1
    #         elif content == "v":
    #             idx = 2
    #         elif content == "i":
    #             idx = 3
    #         elif content == "d":
    #             idx = 4
    #         elif content == "l":
    #             idx = 5
    #         if (content is not None) and (idx is not None):
    #             if ability_handle.status_point > ability_handle.ability[idx].upgrade_demand:
    #                 ability_handle.status_point -= ability_handle.ability[idx].upgrade_demand
    #                 ability_handle.ability[idx].add_ability()
    #                 self.Char_obj.attribute.transform(self.Char_obj, self.Char_obj.equipment)         # 重新根據素質計算能力值
    #                 idx = None
    #         if content == "esc":
    #             self.window.screen.blit(self.window.background.subsurface(rect), rect)  # 關閉視窗
    #             pygame.display.update()
    #             return
    #
    #         ability_sur, _ = self.window.create_equip_ability_win(self.Char_obj)
    #         self.window.screen.blit(ability_sur, rect)
    #         if (animate_group is not None) and (count % 6 == 0):
    #             animate_group.clear(self.window.screen, self.window.background)
    #             animate_group.update(1, 255)
    #             animate_group.draw(self.window.screen)
    #         self.window.set_text_block(self.window.screen, self.Char_obj.char_name, char_name_pos)
    #         self.window.set_status_window(self.Char_obj)
    #         self.window.create_health_bar(self.window.screen, self.Char_obj, char_health_bar_pos)
    #         pygame.display.update()
    #         count += 1
    #
    # def moving_page(self):
    #     img = pygame.image.load(os.path.join("Map_Image", "all_map.png")).convert_alpha()
    #     map_data = Map_Database.map_data[self.current_pos]
    #     pygame.draw.rect(img, Yellow, map_data[6], 3)        # 框出目前地圖
    #
    #     next_map_list = map_data[5]
    #     next_map_name = []
    #     for i in range(len(next_map_list)):             # 框出可前往地圖
    #         next_map_data = Map_Database.map_data[next_map_list[i]]
    #         pygame.draw.rect(img, Green, next_map_data[6], 3)
    #         next_map_name.append("      No. " + str(next_map_data[0]) + "   " + next_map_data[2])
    #
    #     # 調整視野用參數
    #     height_idx = 0
    #     height_idx_list = [0, 100, 200, 300, 400, 500]
    #
    #     # key in 內容
    #     cmd = ""
    #     cmd_rect = pygame.Rect(0, 747, 680, 20)
    #     cmd_bg = self.window.create_color_surface(Black, cmd_rect, 150)
    #     while True:
    #         self.window.clock.tick(self.window.fps)
    #         content = self.window.get_key()
    #         if content in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
    #             cmd += content
    #         elif content == "backspace":
    #             cmd = cmd[:-1]
    #         elif content == "esc":
    #             return None
    #         elif content == "enter":
    #             return int(cmd)
    #             # if int(cmd) in next_map_list:
    #             #     return int(cmd)
    #             # else:
    #             #     cmd = ""
    #         elif content == "up":
    #             height_idx = height_idx - 1 if height_idx > 0 else 0
    #         elif content == "down":
    #             height_idx = height_idx + 1 if height_idx < len(height_idx_list) - 1 else len(height_idx_list) - 1
    #
    #         img_cut = img.subsurface(pygame.Rect(0, height_idx_list[height_idx], 1024, 768))
    #         self.window.screen.blit(img_cut, (0, 0))
    #         self.window.reset_chat_message()
    #         self.window.set_chat_window(["---------- 地圖移動頁面 ----------",
    #                                      "按下 [Esc] 回上一層",
    #                                      "         [方向鍵 - 上] or [方向鍵 - 下] 捲動地圖",
    #                                      "目前所在位置： No. " + str(map_data[0]) + "    " + map_data[2],
    #                                      "可前往以下地圖："] + next_map_name,
    #                                     [Green, Green, Green, Yellow, Green] + [Green] * len(next_map_name),
    #                                     bg = img_cut)
    #         self.window.screen.blit(img_cut.subsurface(cmd_rect), cmd_rect)
    #         self.window.screen.blit(cmd_bg, cmd_rect)
    #         self.window.screen.blit(self.window.font.render("預計前往地圖號碼：" + cmd, True, Green), cmd_rect)
    #         pygame.display.update()
