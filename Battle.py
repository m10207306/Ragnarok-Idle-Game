import math, os, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來
import Character

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class BattleControl:
    def __init__(self, graphic_obj, background_path, char):
        self.window = graphic_obj
        self.background_path = background_path
        self.char = char
        self.attack_fps = 30
        self.standby_fps = 10

    def run(self):
        idx = True
        while idx:
            self.window.set_bg_image(self.background_path, 255)
            self.window.play_bgm(os.path.join("BG_Music", "prt_fild08.mp3"))
            self.window.set_status_window(self.char)
            self.window.reset_chat_message()
            self.window.set_chat_window(["按 [A] 開始戰鬥",
                                         "     [Esc] 返回城市"], [Green, Green])
            idx = self.standby()

    def standby(self):
        char_pos = (self.window.width * 0.4, self.window.height * 0.55)

        char_damage = Damage(self.window, char_pos)                     # 無效，只是沿用流程
        char_animate = Animate(self.window, self.char.standby_img_path, self.char.standby_img_path, char_pos, char_damage)
        while True:
            self.window.tick(self.standby_fps)
            content = self.window.get_key()
            if content == "esc":
                return False
            elif content == "a":
                self.attack()
                return True
            char_animate.update()
            self.window.update_screen((0, 0, self.window.width, self.window.height))

    def attack(self):
        self.window.reset_chat_message()
        monster = Character.MonsterClass(0)
        count = 1
        char_center_pos = (self.window.width * 0.4, self.window.height * 0.55)
        enemy_center_pos = (self.window.width * 0.6, self.window.height * 0.55)
        char_damage_center = (enemy_center_pos[0], enemy_center_pos[1] - 110)
        enemy_damage_center = (char_center_pos[0], char_center_pos[1] - 110)

        char_damage = Damage(self.window, char_damage_center)
        enemy_damage = Damage(self.window, enemy_damage_center)

        char_animate = Animate(self.window, self.char.standby_img_path, self.char.attack_img_path, char_center_pos, char_damage)
        enemy_animate = Animate(self.window, monster.standby_img_path, monster.attack_img_path, enemy_center_pos, enemy_damage)

        char_move_frq = math.floor(self.attack_fps / self.char.attribute.att_frq / char_animate.image_count)
        enemy_move_frq = math.floor(self.attack_fps / monster.attribute.att_frq / enemy_animate.image_count)

        char_dead = False
        mons_dead = False
        while True:
            # pygame.dispaly.update 會掉 frame，但暫時無法處理，執行時間大概是0.04秒
            # 測試在 60 fps下只做update就會掉到25fps
            self.window.tick(self.attack_fps)
            content = self.window.get_key()
            print(self.window.clock.get_fps())
            if content == "esc":
                return

            # 處理攻擊動畫、傷害數字、判斷死亡
            if count % char_move_frq == 0:
                mons_dead = char_animate.update_with_sound(self.char, monster)
            if count % enemy_move_frq == 0:
                char_dead = enemy_animate.update_with_sound(monster, self.char)

            # 處理傷害數字的漂浮動畫
            surface = char_damage.generate_surface()
            if surface is not None:
                self.window.screen.blit(surface, (char_damage_center[0]-35, char_damage_center[1]-30-39))
            surface = enemy_damage.generate_surface()
            if surface is not None:
                self.window.screen.blit(surface, (enemy_damage_center[0]-35, enemy_damage_center[1]-30-39))

            # 更新畫面
            self.window.update_screen((0, 0, self.window.width, self.window.height))

            # 死亡後動作
            if mons_dead:
                self.char.get_exp(monster.base_exp, monster.job_exp)
                return
            if char_dead:
                self.char.exp_punish()
                self.char.respawn()
                return

            count += 1


class Animate(pygame.sprite.Sprite):
    def __init__(self, graphic_obj, standby_image_path, attack_image_path, center_pos, damage_obj):
        super().__init__()
        # property 中 image 與 rect 是必須的
        self.window = graphic_obj
        self.default_width = 200
        self.standby_image = self.window.load_image(standby_image_path)
        self.standby_image.set_colorkey(self.standby_image.get_at((0, 0)))
        self.attack_image = self.window.load_image(attack_image_path)
        self.attack_image.set_colorkey(self.attack_image.get_at((0, 0)))
        self.image_count = self.standby_image.get_size()[0] / self.default_width        # 原則上是6
        self.current = 0
        self.standby_image_array = []
        self.attack_image_array = []
        self.center_pos = center_pos
        self.damage = damage_obj
        for i in range(1, int(self.image_count)+1):                             # Parsing 攻擊動畫
            self.standby_image_array.append(self.standby_image.subsurface(self.window.create_rect((i-1) * self.default_width,
                                                                          0,
                                                                          self.default_width,
                                                                          self.default_width)))
            self.attack_image_array.append(self.attack_image.subsurface(self.window.create_rect((i-1) * self.default_width,
                                                                        0,
                                                                        self.default_width,
                                                                        self.default_width)))
        self.rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
        self.rect.center = self.center_pos
        self.image = []
        self.sub_bg = self.window.background.subsurface(self.rect)

    def update(self):
        # for standby
        if self.current == self.image_count:
            self.current = 0
        self.current += 1
        self.blit_screen(self.standby_image_array[self.current - 1])

    def update_with_sound(self, attack_side, defence_side):
        # for attack
        defence_dead = False
        if self.current == self.image_count:
            self.current = 0
            defence_dead = self.damage.add_damage(attack_side, defence_side)
        self.current += 1
        self.blit_screen(self.attack_image_array[self.current - 1])
        return defence_dead

    def blit_screen(self, ani_img):
        rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
        rect.center = self.center_pos
        self.window.screen.blit(self.sub_bg, rect)
        self.window.screen.blit(ani_img, rect)


class Damage:
    def __init__(self, graphic_obj, blit_center_pos):
        self.window = graphic_obj
        self.damage_width = 10
        self.damage_height = 13
        self.cri_width = 70
        self.cri_height = 60
        self.center_pos = blit_center_pos
        self.damage_img = self.window.damage_template
        self.damage_cri_img = self.window.damage_cri_template
        self.miss_img = self.window.miss_template
        self.cri_img = self.window.cri_template
        self.damage_list = []

    def calculate_damage(self, attack_side, defence_side):
        # 先判斷是否命中
        if attack_side.attribute.hit < defence_side.attribute.flee + 100:
            if not self.trigger_or_not(round(attack_side.attribute.hit / (defence_side.attribute.flee + 100), 2)):
                self.window.effect_sound(os.path.join("Effect_Sound", "_attack_sword_miss.wav"))
                return [0, 3]
        defence_ratio = round((4000 + defence_side.attribute.total_defence) / (4000 + defence_side.attribute.total_defence * 10), 2)
        damage_value = random.randint(attack_side.attribute.total_atk[0], attack_side.attribute.total_atk[1])
        damage_value *= defence_ratio
        # 再判斷是否爆擊
        if self.trigger_or_not(round(attack_side.attribute.cri / 100, 2)):
            damage_value *= 1.5
            self.window.effect_sound(os.path.join("Effect_Sound", "ef_hit2_critical.wav"))
            return [math.floor(damage_value), 2]

        self.window.effect_sound(os.path.join("Effect_Sound", "_hit_dagger.wav"))
        # return [damage_value, type]    type1 = 普通  type2 = 爆擊  type3 = miss
        return [math.floor(damage_value), 1]

    def add_damage(self, attack_side, defence_side):
        damage = self.calculate_damage(attack_side, defence_side)
        damage[0] = 9999999 if damage[0] > 9999999 else damage[0]
        defence_side.hp -= damage[0]
        damage_value = [int(d) for d in str(damage[0])]                 # 擷取傷害的每個數字
        self.damage_list.insert(0, [damage_value, damage[1], 0])        # [Token過的傷害, frame idx] 排序方式是越薪的越前面，這樣超過40 frame的傷害就可以從後面開始刪，在iterate時才不會有問題
        if defence_side.hp <= damage[0]:
            return True

    def generate_surface(self):
        if len(self.damage_list) == 0:
            return
        else:
            rect = self.window.create_rect(self.center_pos[0]-(self.cri_width / 2), self.center_pos[1]-(self.cri_height / 2)-39, self.cri_width, 99)
            # 切出傷害漂浮動畫所需要的完整區域，大小是70x99 (60+39)，x是第一個frame center pos - width/2
            # y則是第一個frame center pos - width / 2 - 39(隨著frame往上漂浮的空間)
            bg = self.window.background.copy()
            surface = bg.subsurface(rect)
            for damage, damage_type, frame in self.damage_list:              # 先篩選一遍看是否有壽命到期的傷害
                if frame == 20:
                    self.damage_list.remove([damage, damage_type, frame])
            for damage, damage_type, frame in reversed(self.damage_list):    # 反向iterate，從舊的傷害開始blit
                if damage_type == 1:
                    bg2 = self.window.background.copy()
                    rect2 = self.window.create_rect(0, 0, len(damage) * self.damage_width, self.damage_height)
                    rect2.center = self.window.create_rect(self.center_pos[0]-len(damage)/2, self.center_pos[1]-self.damage_height/2-frame*2, len(damage) * self.damage_width, self.damage_height).center
                    dmg_surface = bg2.subsurface(rect2)             # 切出實際傷害所佔的背景
                    for i in range(len(damage)):                    # 畫上傷害
                        dmg_surface.blit(self.damage_img[damage[i]], (i * self.damage_width, 0))
                    rect3 = self.window.create_rect(0, 38 - frame*2, self.cri_width, self.cri_height)     # 產出在surface上的正確center位置
                    rect2.center = rect3.center                                                           # 轉交這個center位置
                    surface.blit(dmg_surface, rect2)
                elif damage_type == 2:
                    cri_base = self.cri_img.copy()
                    rect3 = self.window.create_rect(0, 0, len(damage) * self.damage_width, self.damage_height)  # 找出預計傷害區域的座標
                    rect3.center = cri_base.get_rect().center               # 把這個區域的中心對準cri_base的中心
                    for i in range(len(damage)):                            # 按照這個座標開始刻數字
                        cri_base.blit(self.damage_cri_img[damage[i]], (rect3.x + i * self.damage_width, rect3.y))
                    rect4 = self.window.create_rect(0, 38 - frame*2, self.cri_width, self.cri_height)
                    surface.blit(cri_base, rect4)
                elif damage_type == 3:
                    rect2 = self.window.miss_template.get_rect()
                    rect3 = self.window.create_rect(0, 38 - frame*2, self.cri_width, self.cri_height)
                    rect2.center = rect3.center
                    surface.blit(self.miss_img, rect2)
                self.damage_list[self.damage_list.index([damage, damage_type, frame])][2] += 1
            return surface

    @staticmethod
    def trigger_or_not(probability):
        return random.randint(1, 100) >= (1 - probability) * 100


#     def standby(self):
#         char_pos = (self.window.width * 0.4, self.window.height * 0.55)
#         char_damage = Damage(self.window, char_pos)                     # 無效，只是沿用流程
#         char_animate = Animate(self.window, self.char.standby_img_path, self.char.standby_img_path, char_pos, char_damage)
#         while True:
#             self.window.tick(self.standby_fps)
#             content = self.window.get_key()
#             if content == "esc":
#                 return False
#             elif content == "a":
#                 self.attack()
#                 return True
#             char_animate.update()
#             self.window.update_screen((0, 0, self.window.width, self.window.height))
#
#     def attack(self):
#         self.window.reset_chat_message()
#         monster = Character.MonsterClass(0)
#         count = 1
#         char_center_pos = (self.window.width * 0.4, self.window.height * 0.55)
#         enemy_center_pos = (self.window.width * 0.6, self.window.height * 0.55)
#         char_damage_center = (enemy_center_pos[0], enemy_center_pos[1] - 110)
#         enemy_damage_center = (char_center_pos[0], char_center_pos[1] - 110)
#
#         char_damage = Damage(self.window, char_damage_center)
#         enemy_damage = Damage(self.window, enemy_damage_center)
#
#         char_animate = Animate(self.window, self.char.standby_img_path, self.char.attack_img_path, char_center_pos, char_damage)
#         enemy_animate = Animate(self.window, monster.standby_img_path, monster.attack_img_path, enemy_center_pos, enemy_damage)
#
#         char_move_frq = math.floor(self.attack_fps / self.char.attribute.att_frq / char_animate.image_count)
#         enemy_move_frq = math.floor(self.attack_fps / monster.attribute.att_frq / enemy_animate.image_count)
#
#         char_dead = False
#         mons_dead = False
#         while True:
#             # pygame.dispaly.update 會掉 frame，但暫時無法處理，執行時間大概是0.04秒
#             # 測試在 60 fps下只做update就會掉到25fps
#             self.window.tick(self.attack_fps)
#             content = self.window.get_key()
#             print(self.window.clock.get_fps())
#             if content == "esc":
#                 return
#
#             # 處理攻擊動畫、傷害數字、判斷死亡
#             if count % char_move_frq == 0:
#                 mons_dead = char_animate.update_with_sound(self.char, monster)
#             if count % enemy_move_frq == 0:
#                 char_dead = enemy_animate.update_with_sound(monster, self.char)
#
#             # 處理傷害數字的漂浮動畫
#             surface = char_damage.generate_surface()
#             if surface is not None:
#                 self.window.screen.blit(surface, (char_damage_center[0]-35, char_damage_center[1]-30-39))
#             surface = enemy_damage.generate_surface()
#             if surface is not None:
#                 self.window.screen.blit(surface, (enemy_damage_center[0]-35, enemy_damage_center[1]-30-39))
#
#             # 更新畫面
#             self.window.update_screen((0, 0, self.window.width, self.window.height))
#
#             # 死亡後動作
#             if mons_dead:
#                 self.char.get_exp(monster.base_exp, monster.job_exp)
#                 return
#             if char_dead:
#                 self.char.exp_punish()
#                 self.char.respawn()
#                 return
#
#             count += 1
#
#
# class Animate:
#     def __init__(self, graphic_obj, standby_image_path, attack_image_path, center_pos, damage_obj):
#         self.window = graphic_obj
#         self.default_width = 200
#         self.standby_image = self.window.load_image(standby_image_path)
#         self.standby_image.set_colorkey(self.standby_image.get_at((0, 0)))
#         self.attack_image = self.window.load_image(attack_image_path)
#         self.attack_image.set_colorkey(self.attack_image.get_at((0, 0)))
#         self.image_count = self.standby_image.get_size()[0] / self.default_width        # 原則上是6
#         self.current = 0
#         self.standby_image_array = []
#         self.attack_image_array = []
#         self.center_pos = center_pos
#         self.damage = damage_obj
#         for i in range(1, int(self.image_count)+1):                             # Parsing 攻擊動畫
#             self.standby_image_array.append(self.standby_image.subsurface(self.window.create_rect((i-1) * self.default_width,
#                                                                           0,
#                                                                           self.default_width,
#                                                                           self.default_width)))
#             self.attack_image_array.append(self.attack_image.subsurface(self.window.create_rect((i-1) * self.default_width,
#                                                                         0,
#                                                                         self.default_width,
#                                                                         self.default_width)))
#         rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
#         rect.center = self.center_pos
#         self.sub_bg = self.window.background.subsurface(rect)
#
#     def update(self):
#         # for standby
#         if self.current == self.image_count:
#             self.current = 0
#         self.current += 1
#         self.blit_screen(self.standby_image_array[self.current - 1])
#
#     def update_with_sound(self, attack_side, defence_side):
#         # for attack
#         defence_dead = False
#         if self.current == self.image_count:
#             self.current = 0
#             defence_dead = self.damage.add_damage(attack_side, defence_side)
#         self.current += 1
#         self.blit_screen(self.attack_image_array[self.current - 1])
#         return defence_dead
#
#     def blit_screen(self, ani_img):
#         rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
#         rect.center = self.center_pos
#         self.window.screen.blit(self.sub_bg, rect)
#         self.window.screen.blit(ani_img, rect)




