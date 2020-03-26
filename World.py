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
Orange = (255, 170, 0)
Battle_Meg_Color = (0, 196, 255)


class WorldClass:
    def __init__(self, window_screen, name, ini_ability):
        self.window = window_screen
        self.current_pos = None
        self.Char_obj = Character.CharacterClass(name, ini_ability)

        # 一些幾乎必備的Animate Group存在這裏，避免每進去一個function要重做一次
        self.char_pos = (self.window.width * 0.4, self.window.height * 0.55)    # center pos
        self.mons_pos = (self.window.width * 0.6, self.window.height * 0.55)
        self.char_name_pos = (self.char_pos[0], self.char_pos[1] - 70)
        self.mons_name_pos = (self.mons_pos[0], self.mons_pos[1] - 70)
        self.char_damage_pos = (self.mons_pos[0], self.mons_pos[1] - 110)
        self.mons_damage_pos = (self.char_pos[0], self.char_pos[1] - 110)
        self.status_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(self.window.status_win_template, (0, 0)))
        self.mini_map_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        self.health_bar_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        self.chat_input_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.Surface((1, 1)), (0, 0)))
        name_text = self.window.get_text_block(self.Char_obj.char_name, self.char_name_pos)
        self.name_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(name_text, self.char_name_pos))
        chat = self.window.get_chat_win([], [])
        self.chat_pos = (chat.get_size()[0] / 2, self.window.height - chat.get_size()[1] / 2 - self.window.chat_input_template.get_size()[1])
        self.chat_input_pos = (self.window.chat_input_template.get_size()[0] / 2, self.window.height - self.window.chat_input_template.get_size()[1] / 2)
        self.chat_room_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(chat, self.chat_pos))
        self.ptr_group = pygame.sprite.Group(Animate_Utility.PointerAnimate(self.window.pointer_template, pygame.mouse.get_pos(), 7))

        pos = [(self.window.width - 350, self.window.height -  70),
               (self.window.width - 200, self.window.height -  70),
               (self.window.width -  50, self.window.height -  70),
               (self.window.width - 352, self.window.height - 195),
               (self.window.width - 200, self.window.height - 195),
               (self.window.width -  50, self.window.height - 195)]
        self.pos2 = [(pos[0][0], pos[0][1] + 45),
                     (pos[1][0], pos[1][1] + 45),
                     (pos[2][0], pos[2][1] + 45),
                     (pos[3][0] + 2, pos[3][1] + 45),
                     (pos[4][0], pos[4][1] + 45),
                     (pos[5][0], pos[5][1] + 45)]
        self.console_text = ["角色資訊", "物品資訊", "裝備資訊", "戰鬥開關", "地圖開關", "技能資訊"]
        self.console_btn_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[2], pos[0]))  # info
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[3], pos[1]))    # item
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[1], pos[2]))    # equip
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[0], pos[3]))    # battle
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[4], pos[4]))    # map
        self.console_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_inter_template[5], pos[5]))    # skill
        self.console_text_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[0], self.pos2[0]), self.pos2[0]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[1], self.pos2[1]), self.pos2[1]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[2], self.pos2[2]), self.pos2[2]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[3], self.pos2[3]), self.pos2[3]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[4], self.pos2[4]), self.pos2[4]))
        self.console_text_group.add(Animate_Utility.InfoWindowAnimate(self.window.get_text_block(self.console_text[5], self.pos2[5]), self.pos2[5]))

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
        # fps 54-59
        map_data = Map_Database.map_data[map_idx]
        self.window.set_bg_image(os.path.join("BG_Image", map_data[1] + ".png"), 255)

        char_sit_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(self.Char_obj.sit_img, self.char_pos))
        self.common_group_update()
        chat = self.window.get_chat_win(["[系統訊息] 目前所在位置 - " + map_data[2]], [Green])
        self.chat_room_group.update(chat, None)

        all_group = self.window.combine_sprite(char_sit_group, self.status_group, self.mini_map_group,
                                               self.health_bar_group, self.chat_room_group, self.name_group,
                                               self.chat_input_group, self.console_btn_group, self.console_text_group,
                                               self.ptr_group)

        for sprite in self.console_btn_group.sprites():
            sprite.freeze = False
        self.console_btn_group.sprites()[3].freeze = True   # Battel btn disable

        fps_list = []
        enter = False
        opt_select = None
        while True:
            self.window.clock.tick(self.window.fps)
            fps_list.append(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                print("City Standby")
                self.window.fps_analysis(fps_list)
                return None

            all_group.clear(self.window.screen, self.window.background)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            self.status_group.update(self.window.get_status_win(self.Char_obj), None)
            self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
            for idx, btn in enumerate(self.console_btn_group.sprites()):
                if btn.update(ptr_tip_pos, mouse_type):
                    opt_select = idx
                    enter = True

            all_group.draw(self.window.screen)
            pygame.display.update()

            if enter and opt_select is not None:
                if opt_select == 0:
                    return self.info_page(map_idx)
                elif opt_select == 1:
                    return self.item_page(map_idx)
                elif opt_select == 2:
                    print("裝備")
                elif opt_select == 3:
                    print("戰鬥")
                elif opt_select == 4:
                    return self.moving_page(map_idx)
                elif opt_select == 5:
                    print("技能")

    def field_run(self, map_idx):
        map_data = Map_Database.map_data[map_idx]
        self.window.set_bg_image(os.path.join("BG_Image", map_data[1] + ".png"), 255)
        self.common_group_update()

        chat = self.window.get_chat_win(["[系統訊息] 目前所在位置：" + map_data[2]], [Green])
        self.chat_room_group.update(chat, None)

        char_group = pygame.sprite.Group(Animate_Utility.CharAnimate(self.window, self.Char_obj, None, self.char_pos, self.char_damage_pos, None))
        for sprite in self.console_btn_group.sprites():     # 所有按鍵都可以使用
            sprite.freeze = False

        all_group = self.window.combine_sprite(char_group, self.status_group, self.mini_map_group,
                                               self.health_bar_group, self.chat_room_group, self.name_group,
                                               self.chat_input_group, self.console_btn_group,
                                               self.console_text_group, self.ptr_group)

        fps_list = []
        enter = False
        opt_select = None
        while True:
            self.window.clock.tick(self.window.fps)
            fps_list.append(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                print("Field Standby")
                self.window.fps_analysis(fps_list)
                return None

            all_group.clear(self.window.screen, self.window.background)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            self.status_group.update(self.window.get_status_win(self.Char_obj), None)
            self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
            char_group.update(1, 255)
            for idx, btn in enumerate(self.console_btn_group.sprites()):
                if btn.update(ptr_tip_pos, mouse_type):
                    opt_select = idx
                    enter = True

            all_group.draw(self.window.screen)
            pygame.display.update()

            if enter and opt_select is not None:
                if opt_select == 0:
                    return self.info_page(map_idx)
                elif opt_select == 1:
                    return self.item_page(map_idx)
                elif opt_select == 2:
                    print("裝備")
                elif opt_select == 3:
                    return self.fight_run(map_idx)
                elif opt_select == 4:
                    return self.moving_page(map_idx)
                elif opt_select == 5:
                    print("技能")

    def fight_run(self, map_idx):
        map_data = Map_Database.map_data[map_idx]
        self.common_group_update()
        chat = self.window.get_chat_win(["[系統訊息] 循環戰鬥 - 按下 ESC 逃離戰鬥"], [Green])
        self.chat_room_group.update(chat, None)

        for sprite in self.console_btn_group.sprites():
            sprite.freeze = True

        while True:
            mons_obj = Character.MonsterClass(random.choice(map_data[7]))
            char_dmg_group = Animate_Utility.DamageAnimate.char_damage
            mons_dmg_group = Animate_Utility.DamageAnimate.mons_damage
            char_group = pygame.sprite.Group(Animate_Utility.CharAnimate(self.window, self.Char_obj, mons_obj, self.char_pos, self.char_damage_pos, char_dmg_group))
            mons_group = pygame.sprite.Group(Animate_Utility.CharAnimate(self.window, mons_obj, self.Char_obj, self.mons_pos, self.mons_damage_pos, mons_dmg_group))

            mons_name = self.window.get_text_block("Lv." + str(mons_obj.base_level) + " " + mons_obj.mons_zh_name, self.mons_name_pos)
            self.name_group.add(Animate_Utility.InfoWindowAnimate(mons_name, self.mons_name_pos))

            all_group = self.window.combine_sprite(char_group, mons_group, self.status_group,
                                                   self.mini_map_group, self.health_bar_group, self.chat_room_group,
                                                   self.name_group, self.chat_input_group, self.console_btn_group,
                                                   self.console_text_group, self.ptr_group)
            # 怪物漸進登場
            count = 0
            frame_limit = char_group.sprites()[0].standby_frame_interval
            animate_count = char_group.sprites()[0].image_count
            alpha_step = 20
            alpha = 255 - (alpha_step * frame_limit / animate_count)
            self.console_btn_group.sprites()[3].image = self.console_btn_group.sprites()[3].btn_list[0]  # 按鍵動畫恢復按下去之前
            self.console_btn_group.sprites()[3].freeze = True  # 動畫時間不跳出
            fps_list = []
            while True:
                self.window.clock.tick(self.window.fps)
                fps_list.append(self.window.clock.get_fps())
                _, _, _, _ = self.window.input_detect()
                if count >= frame_limit * 2:
                    break

                all_group.clear(self.window.screen, self.window.background)

                self.ptr_group.update(pygame.mouse.get_pos())
                char_group.sprites()[0].update(1, 255)
                mons_group.sprites()[0].update(1, alpha)
                if count % mons_group.sprites()[0].min_std_interval == 0:
                    alpha += alpha_step

                all_group.draw(self.window.screen)
                pygame.display.update()
                count += 1

            print("Monster Come Out Stage")
            self.window.fps_analysis(fps_list)

            # 正式戰鬥
            # 如果加入即時更新戰報fps會降到45-50，不加入則大概55-60，優化後可以加入訊息還是保持在55-60
            # 攻速最快190的情況下fps大概在50-55
            char_group.sprites()[0].reset_frame_animate()
            mons_group.sprites()[0].reset_frame_animate()
            mons_dead = False
            char_dead = False
            fps_list = []
            self.console_btn_group.sprites()[3].freeze = False  # 正式戰鬥可以跳出
            chat_update = False
            while True:
                self.window.clock.tick(self.window.fps)
                fps_list.append(self.window.clock.get_fps())
                key, key_id, mouse, mouse_type = self.window.input_detect()

                all_group.clear(self.window.screen, self.window.background)
                char_dmg_group.clear(self.window.screen, self.window.background)
                mons_dmg_group.clear(self.window.screen, self.window.background)
                # 因為damage_group會動態增加sprite跟減少，所以沒辦法在外面一次塞進去all_group裡

                self.ptr_group.update(pygame.mouse.get_pos())
                ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
                self.status_group.update(self.window.get_status_win(self.Char_obj), None)
                self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)

                if "escape" in key:
                    char_dmg_group.empty()      # 調離戰鬥時清除傷害紀錄
                    mons_dmg_group.empty()
                    print("Battle Stage")
                    self.window.fps_analysis(fps_list)
                    return map_idx

                char_group.update(2, 255)
                if len(char_dmg_group.sprites()) != 0 and (char_dmg_group.sprites()[-1].life == 0):
                    self.window.get_chat_win([char_dmg_group.sprites()[-1].get_battle_msg()], [Battle_Meg_Color], True)
                    chat_update = True
                mons_group.update(2, 255)
                if len(mons_dmg_group.sprites()) != 0 and (mons_dmg_group.sprites()[-1].life == 0):
                    self.window.get_chat_win([mons_dmg_group.sprites()[-1].get_battle_msg()], [Battle_Meg_Color], True)
                    chat_update = True
                char_dmg_group.update()
                mons_dmg_group.update()
                if chat_update:             # 有更新訊息才update chat room，不然fps會降到45
                    chat = self.window.get_chat_win([], [])
                    self.chat_room_group.update(chat, None)
                    chat_update = False

                char_dmg_group.draw(self.window.screen)
                mons_dmg_group.draw(self.window.screen)
                all_group.draw(self.window.screen)
                pygame.display.update()

                if mons_obj.hp <= 0:
                    mons_dead = True
                    break
                elif self.Char_obj.hp <= 0:
                    self.Char_obj.hp = 0
                    char_dead = True
                    break

            print("Battle Stage")
            self.window.fps_analysis(fps_list)

            # 死亡動畫
            char_group.sprites()[0].reset_frame_animate()
            mons_group.sprites()[0].reset_frame_animate()
            count = 0
            self.console_btn_group.sprites()[3].freeze = True  # 死亡與總結階段無法跳出
            fps_list = []
            while True:
                self.window.clock.tick(self.window.fps)
                fps_list.append(self.window.clock.get_fps())
                _, _, _, _ = self.window.input_detect()

                if count >= frame_limit and len(char_dmg_group.sprites()) == 0 and len(mons_dmg_group.sprites()) == 0:
                    break

                all_group.clear(self.window.screen, self.window.background)
                char_dmg_group.clear(self.window.screen, self.window.background)
                mons_dmg_group.clear(self.window.screen, self.window.background)

                self.ptr_group.update(pygame.mouse.get_pos())
                self.status_group.update(self.window.get_status_win(self.Char_obj), None)
                self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
                char_dmg_group.update()
                mons_dmg_group.update()

                if mons_dead:
                    char_group.sprites()[0].update(1, 255)      # 勝者會持續待機動畫
                    if count < frame_limit:
                        mons_group.sprites()[0].update(3, 255)  # 播過一次死亡動畫就會定格在最後一張動畫
                elif char_dead:
                    mons_group.sprites()[0].update(1, 255)
                    if count < frame_limit:
                        char_group.sprites()[0].update(3, 255)

                char_dmg_group.draw(self.window.screen)
                mons_dmg_group.draw(self.window.screen)
                all_group.draw(self.window.screen)

                pygame.display.update()
                count += 1

            print("Dead Animate Stage")
            self.window.fps_analysis(fps_list)

            # 戰鬥結果總結（經驗值處理）
            count = 0
            self.console_btn_group.sprites()[3].freeze = False  # 死亡與總結階段無法跳出
            sys_message = "[戰鬥結果] - "
            lv_up_message = "[系統訊息] "
            if mons_dead:
                base_lv_up, job_lv_up = self.Char_obj.get_exp(mons_obj.base_exp, mons_obj.job_exp)
                sys_message += "勝利！ 獲得 Base Exp " + str(mons_obj.base_exp) + ", Job Exp " + str(mons_obj.job_exp)
                if base_lv_up:
                    lv_up_message += "Base Level Up! " + str(self.Char_obj.base_level - 1) + " -> " + str(self.Char_obj.base_level)
                if base_lv_up and job_lv_up:
                    lv_up_message += " | "
                if job_lv_up:
                    lv_up_message += "Job Level Up! " + str(self.Char_obj.job_level - 1) + " -> " + str(self.Char_obj.job_level)
            elif char_dead:
                self.Char_obj.exp_punish()
                sys_message += "失敗！ 損失 2% Base / Job Exp"
            chat_list = [sys_message]
            if lv_up_message != "[系統訊息] ":
                chat_list.append(lv_up_message)
            chat = self.window.get_chat_win(chat_list, [Green] * len(chat_list))
            self.chat_room_group.update(chat, None)
            while True:
                self.window.clock.tick(self.window.fps)
                _, _, _, _ = self.window.input_detect()

                if count >= frame_limit:
                    if mons_dead:
                        break
                    elif char_dead:
                        self.Char_obj.respawn()
                        return map_idx
                all_group.clear(self.window.screen, self.window.background)

                self.ptr_group.update(pygame.mouse.get_pos())
                self.status_group.update(self.window.get_status_win(self.Char_obj), None)
                self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
                if mons_dead:
                    char_group.sprites()[0].update(1, 255)
                elif char_dead:
                    mons_group.sprites()[0].update(1, 255)

                all_group.draw(self.window.screen)
                pygame.display.update()
                count += 1

            self.name_group.remove(mons_name)

    def item_page(self, map_idx):
        char_sit_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.image.load(self.Char_obj.sit_img_path).convert_alpha(), self.char_pos))
        self.common_group_update()
        chat = self.window.get_chat_win(["[系統訊息] 物品資訊頁面 - 按下 ESC 退出"], [Green])
        self.chat_room_group.update(chat, None)
        window_center = (0.80 * self.window.width, 0.55 * self.window.height)

        transparent_btn = [self.window.create_color_surface(White, pygame.Rect(0, 0, 15, 23), 0)] * 3
        type_btn_w_bias, type_btn_h_bias, h_step = 118, 58, 26
        # 物品欄中切換顯示不同物品的按鍵
        usable_switch_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(transparent_btn, (window_center[0] - type_btn_w_bias, window_center[1] - type_btn_h_bias)))
        equip_switch_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(transparent_btn, (window_center[0] - type_btn_w_bias, window_center[1] - type_btn_h_bias + h_step)))
        collect_switch_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(transparent_btn, (window_center[0] - type_btn_w_bias, window_center[1] - type_btn_h_bias + 2 * h_step)))

        win_base = self.window.get_item_base_win(0)
        # 物品欄的基礎背景，並且輸入參數來決定這是哪種類型物品(不包含具體物品)
        item_win_base_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(win_base, window_center))
        item_list_width, item_list_height = 32, 32
        show_width, show_height = 40 * 2 + 32 * 5, item_list_height * 4
        height_start, scroll_step = 0, 2
        border_list = [int(window_center[1]) - 69, int(window_center[1]) + 59, int(window_center[0]) - 110, int(window_center[0]) + 130]
        # 秀出不同類型物品的物品列表（如果項目較多可上下滾動）
        win_list, item_btn_group = self.window.get_item_list_win(self.Char_obj.item.all_list[0], border_list)
        item_win_list_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(win_list.subsurface(pygame.Rect(0, height_start, show_width, show_height)), (window_center[0] + 10, window_center[1] - 5)))
        all_group = self.window.combine_sprite(char_sit_group, usable_switch_group, equip_switch_group, collect_switch_group,
                                               item_win_base_group, item_win_list_group,
                                               self.status_group, self.mini_map_group,
                                               self.health_bar_group, self.chat_room_group, self.name_group,
                                               self.chat_input_group, self.console_btn_group, self.console_text_group,
                                               self.ptr_group)

        for btn in self.console_btn_group.sprites():
            btn.freeze = True
        self.console_btn_group.sprites()[1].freeze = False

        fps_list = []
        scroll_history = height_start
        while True:
            self.window.clock.tick(self.window.fps)
            fps_list.append(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                print("Item Page")
                self.window.fps_analysis(fps_list)
                return map_idx

            all_group.clear(self.window.screen, self.window.background)
            item_btn_group.clear(self.window.screen, self.window.background)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            self.status_group.update(self.window.get_status_win(self.Char_obj), None)
            self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)
            for idx, btn in enumerate(self.window.combine_sprite(usable_switch_group, equip_switch_group, collect_switch_group)):
                if btn.update(ptr_tip_pos, mouse_type):
                    item_win_base_group.update(self.window.get_item_base_win(idx), None)
                    height_start = 0
                    win_list, item_btn_group = self.window.get_item_list_win(self.Char_obj.item.all_list[idx], border_list)
                    item_win_list_group.update(win_list.subsurface(pygame.Rect(0, height_start, show_width, show_height)), None)

            if item_win_list_group.sprites()[0].rect.collidepoint(ptr_tip_pos):
                if 4 in mouse:
                    height_start = height_start - scroll_step if height_start >= 0 + scroll_step else height_start
                    item_win_list_group.update(win_list.subsurface(pygame.Rect(0, height_start, show_width, show_height)), None)
                    if scroll_history != height_start:
                        item_btn_group.update(2, ptr_tip_pos, mouse_type)
                        scroll_history = height_start
                elif 5 in mouse:
                    height_start = height_start + scroll_step if height_start <= win_list.get_size()[1] - show_height - scroll_step else height_start
                    item_win_list_group.update(win_list.subsurface(pygame.Rect(0, height_start, show_width, show_height)), None)
                    if scroll_history != height_start:
                        item_btn_group.update(1, ptr_tip_pos, mouse_type)
                        scroll_history = height_start
                else:
                    item_btn_group.update(0, ptr_tip_pos, mouse_type)
            all_group.draw(self.window.screen)
            item_btn_group.draw(self.window.screen)
            pygame.display.update()

    def info_page(self, map_idx):
        # fps 48-52，看起來跟Ability Initialization一樣慢，可能是對多個按鍵進行偵測並做對應處置
        # map_data = Map_Database.map_data[map_idx]
        char_sit_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(pygame.image.load(self.Char_obj.sit_img_path).convert_alpha(), self.char_pos))
        self.common_group_update()
        chat = self.window.get_chat_win(["[系統訊息] 角色資訊頁面 - 按下 ESC 退出"], [Green])
        self.chat_room_group.update(chat, None)

        ability_list = ["str", "agi", "vit", "int", "dex", "luk"]
        _, ability_page = self.window.create_equip_ability_win(self.Char_obj)
        page_center = (self.window.width * 0.15, self.window.height * 0.55)
        ability_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(ability_page, page_center))
        ability_btn_group = pygame.sprite.Group()   # 要看升級點來確認是否有btn
        btn_width, btn_height = self.window.btn_r_arw_template[0].get_size()[0], self.window.btn_r_arw_template[0].get_size()[1]
        transparent_btn_list = [self.window.create_color_surface(Black, pygame.Rect(0, 0, btn_width, btn_height), 0)] * 3
        btn_pos_width = page_center[0] - 47
        btn_pos_height = [page_center[1] - 32, page_center[1] - 16, page_center[1], page_center[1] + 16, page_center[1] + 32, page_center[1] + 48, page_center[1] + 64]
        for i in range(len(ability_list)):
            if self.Char_obj.ability.status_point >= self.Char_obj.ability.get_ability(ability_list[i]).upgrade_demand:
                ability_btn_group.add(Animate_Utility.ButtonAnimate(self.window.btn_r_arw_template, (btn_pos_width, btn_pos_height[i])))
            else:
                obj = Animate_Utility.ButtonAnimate(transparent_btn_list, (btn_pos_width, btn_pos_height[i]))   # 不該有箭頭，按下去也不該有反應
                obj.freeze = True
                ability_btn_group.add(obj)

        all_group = self.window.combine_sprite(char_sit_group, self.status_group, self.mini_map_group,
                                               self.health_bar_group, self.chat_room_group, self.name_group,
                                               self.chat_input_group, self.console_btn_group, self.console_text_group,
                                               ability_group, ability_btn_group, self.ptr_group)

        for btn in self.console_btn_group.sprites():
            btn.freeze = True

        fps_list = []
        while True:
            self.window.clock.tick(self.window.fps)
            fps_list.append(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                print("Ability Page")
                self.window.fps_analysis(fps_list)
                return map_idx

            all_group.clear(self.window.screen, self.window.background)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            self.status_group.update(self.window.get_status_win(self.Char_obj), None)
            self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), None)

            for idx, btn in enumerate(ability_btn_group.sprites()):
                if btn.update(ptr_tip_pos, mouse_type):
                    self.Char_obj.ability.status_point -= self.Char_obj.ability.ability[idx].upgrade_demand
                    self.Char_obj.ability.ability[idx].add_ability()
                    self.Char_obj.attribute.transform(self.Char_obj, self.Char_obj.equipment)   # 重新根據素質計算能力值

            for idx, btn in enumerate(ability_btn_group.sprites()):     # 確認是否還能加點，不能就消除按鈕
                if self.Char_obj.ability.status_point < self.Char_obj.ability.ability[idx].upgrade_demand:
                    # 轉為透明，且凍結
                    btn.image = transparent_btn_list[0]
                    btn.freeze = True

            _, ability_page = self.window.create_equip_ability_win(self.Char_obj)
            ability_group.update(ability_page, None)

            all_group.draw(self.window.screen)

            pygame.display.update()

    def moving_page(self, map_idx):
        # fps 50 - 56
        img = pygame.image.load(os.path.join("Map_Image", "all_map.png")).convert_alpha()
        map_data = Map_Database.map_data[self.current_pos]
        curr_btn_list = [self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size),
                         self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size),
                         self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size)]
        pygame.draw.rect(curr_btn_list[0], Blue, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 4)
        pygame.draw.rect(curr_btn_list[1], Blue, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 8)
        pygame.draw.rect(curr_btn_list[2], Blue, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 2)

        next_btn_list = [self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size),
                         self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size),
                         self.window.create_transparent_surface(Map_Database.map_size, Map_Database.map_size)]
        pygame.draw.rect(next_btn_list[0], Green, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 4)
        pygame.draw.rect(next_btn_list[1], Green, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 8)
        pygame.draw.rect(next_btn_list[2], Green, pygame.Rect(0, 0, Map_Database.map_size, Map_Database.map_size), 2)

        btn_group = pygame.sprite.Group(Animate_Utility.ButtonAnimate(curr_btn_list, map_data[6].center))
        next_map_list = list(map_data[5]).copy()
        next_map_name = ["[系統訊息] 地圖移動頁面 - 按下 ESC 退出", "[系統訊息] 此地可移動前往以下地點："]
        for i in range(len(next_map_list)):             # 框出可前往地圖
            next_map_data = Map_Database.map_data[next_map_list[i]]
            next_map_name.append("  No. " + str(next_map_data[0]) + " " + next_map_data[2])
            btn_group.add(Animate_Utility.ButtonAnimate(next_btn_list, next_map_data[6].center))
        next_map_list.insert(0, map_idx)                # 對應到整個btn的順序(目前位置, 可前往地圖編碼1, 可前往地圖編碼2...)
        self.window.get_chat_win(next_map_name, [Orange] * len(next_map_name), True)

        sub_height, height_record = 0, 0
        scroll_step = 10
        max_height = img.get_size()[1] - 1 - self.window.height - 1 - scroll_step
        self.window.set_bg_by_surface(img.subsurface(pygame.Rect(0, sub_height, self.window.width, self.window.height)), 255)
        self.common_group_update()
        chat = self.window.get_chat_win([], [])
        self.chat_room_group.update(chat, None)
        all_group = self.window.combine_sprite([btn_group, self.chat_room_group, self.chat_input_group,
                                                self.console_btn_group, self.console_text_group, self.ptr_group])
        for btn in self.console_btn_group.sprites():
            btn.freeze = True
        fps_list = []
        while True:
            self.window.clock.tick(self.window.fps)
            fps_list.append(self.window.clock.get_fps())
            key, key_id, mouse, mouse_type = self.window.input_detect()
            if "escape" in key:
                print("Map Moving Stage")
                self.window.fps_analysis(fps_list)
                return map_idx

            scroll = False
            if "click" in mouse_type or "down" in mouse_type:
                if 4 in mouse:      # 滾輪往下，影像往上
                    sub_height = sub_height + scroll_step if sub_height < max_height else sub_height
                    if height_record != sub_height:             # 表示sub_height有所變動，因此按鍵的Rect也要跟著變動
                        for btn in btn_group:
                            btn.rect.center = (btn.rect.center[0], btn.rect.center[1] - scroll_step)
                    height_record = sub_height if height_record != sub_height else height_record    # 假設這個Frame的sub_height有變更，則更新紀錄
                    scroll = True
                elif 5 in mouse:    # 滾輪往上，影像往下
                    sub_height = sub_height - scroll_step if sub_height > scroll_step else sub_height
                    if height_record != sub_height:
                        for btn in btn_group:
                            btn.rect.center = (btn.rect.center[0], btn.rect.center[1] + scroll_step)
                    height_record = sub_height if height_record != sub_height else height_record
                    scroll = True

            self.window.set_bg_by_surface(img.subsurface(pygame.Rect(0, sub_height, self.window.width, self.window.height)), 255)
            if scroll:      # 因應動態背景，每個scroll都需要更新聊天室與console btn text的背景
                chat = self.window.get_chat_win([], [])
                self.chat_room_group.update(chat, None)
                for idx, sprite in enumerate(self.console_text_group.sprites()):
                    sprite.update(self.window.get_text_block(self.console_text[idx], self.pos2[idx]), None)

            self.ptr_group.update(pygame.mouse.get_pos())
            ptr_tip_pos = self.ptr_group.sprites()[0].rect.topleft
            for idx, btn in enumerate(btn_group):
                if btn.update(ptr_tip_pos, mouse_type) and 4 not in mouse and 5 not in mouse:
                    print("Map Moving Stage")
                    self.window.fps_analysis(fps_list)
                    return next_map_list[idx]

            all_group.draw(self.window.screen)
            pygame.display.update()

    def common_group_update(self):
        map_data = Map_Database.map_data[self.current_pos]
        status_win = self.window.get_status_win(self.Char_obj)
        self.status_group.update(status_win, self.window.status_win_template.get_rect().center)
        mini_map_win = self.window.get_map_icon(os.path.join("Map_Image", map_data[1] + ".png"))
        self.mini_map_group.update(mini_map_win, (self.window.width - mini_map_win.get_size()[0] / 2, mini_map_win.get_size()[1] / 2))
        self.health_bar_group.update(self.window.get_health_bar(self.Char_obj), (self.char_pos[0], self.char_pos[1] + 50))
        self.chat_input_group.update(self.window.chat_input_template, self.chat_input_pos)
        name_text = self.window.get_text_block(self.Char_obj.char_name, self.char_name_pos)
        self.name_group = pygame.sprite.Group(Animate_Utility.InfoWindowAnimate(name_text, self.char_name_pos))
        self.ptr_group.update(pygame.mouse.get_pos())
        for idx, sprite in enumerate(self.console_text_group.sprites()):
            sprite.update(self.window.get_text_block(self.console_text[idx], self.pos2[idx]), None)
            # 因為會因為背景不同而需要重新Update
