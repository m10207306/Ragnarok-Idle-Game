import math, os, random

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class BattleControl:
    def __init__(self, graphic_obj, background_path, char, enemy):
        self.window = graphic_obj
        self.background_path = background_path
        self.char = char
        self.enemy = enemy
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
        char_animate = Animate(self.window, self.char.standby_img_path, char_pos, char_damage)
        while True:
            self.window.tick(self.standby_fps)
            content = self.window.get_key()
            if content == "esc":
                return False
            elif content == "a":
                self.attack()
                return True
            char_animate.update()

    def attack(self):
        self.window.reset_chat_message()
        count = 1
        char_center_pos = (self.window.width * 0.4, self.window.height * 0.55)
        enemy_center_pos = (self.window.width * 0.6, self.window.height * 0.55)
        char_damage = Damage(self.window, (enemy_center_pos[0], enemy_center_pos[1] - 110))
        enemy_damage = Damage(self.window, (char_center_pos[0], char_center_pos[1] - 110))
        char_animate = Animate(self.window, self.char.attack_img_path, char_center_pos, char_damage)
        enemy_animate = Animate(self.window, self.enemy.attack_img_path, enemy_center_pos, enemy_damage)
        char_move_frq = math.floor(self.attack_fps / self.char.attribute.att_frq / char_animate.image_count)
        enemy_move_frq = math.floor(self.attack_fps / self.enemy.attribute.att_frq / enemy_animate.image_count)

        while True:
            # pygame.dispaly.update 會掉 frame，但暫時無法處理
            # 測試在 30 or 60 fps下只做update就會掉到25fps
            self.window.tick(self.attack_fps)
            content = self.window.get_key()
            # print(self.window.clock.get_fps())
            if content == "esc":
                return

            if count % char_move_frq == 0:
                damage = random.randint(1000, 1000000)
                char_animate.update_with_sound(damage)
            if count % enemy_move_frq == 0:
                damage = random.randint(5, 15)
                enemy_animate.update_with_sound(damage)

            surface = char_damage.generate_surface()
            if surface is not None:
                self.window.screen.blit(surface, (enemy_center_pos[0]-35, enemy_center_pos[1]-110-6-39))
            surface = enemy_damage.generate_surface()
            if surface is not None:
                self.window.screen.blit(surface, (char_center_pos[0]-35, char_center_pos[1]-110-6-39))

            count += 1


class Animate:
    def __init__(self, graphic_obj, standby_image_path, center_pos, damage_obj):
        self.window = graphic_obj
        self.default_width = 200
        self.image = self.window.load_image(standby_image_path)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_count = self.image.get_size()[0] / self.default_width        # 原則上是6
        self.current = 0
        self.image_array = []
        self.center_pos = center_pos
        self.damage = damage_obj
        for i in range(1, int(self.image_count)+1):                             # Parsing 攻擊動畫
            self.image_array.append(self.image.subsurface(self.window.create_rect((i-1) * self.default_width,
                                                          0,
                                                          self.default_width,
                                                          self.default_width)))
        rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
        rect.center = self.center_pos
        self.sub_bg = self.window.background.subsurface(rect)

    def update(self):
        # for standby
        if self.current == self.image_count:
            self.current = 0
        self.current += 1
        self.blit_screen()

    def update_with_sound(self, damage):
        # for battle
        if self.current == self.image_count:
            self.current = 0
            self.window.effect_sound(os.path.join("Effect_Sound", "_hit_dagger.wav"))
            self.damage.add_damage(damage)
        self.current += 1
        self.blit_screen()

    def blit_screen(self):
        ani_img = self.image_array[self.current-1]
        rect = self.window.create_rect(0, 0, self.default_width, self.default_width)
        rect.center = self.center_pos
        self.window.screen.blit(self.sub_bg, rect)
        self.window.screen.blit(ani_img, rect)
        self.window.update_screen(rect)


class Damage:
    def __init__(self, graphic_obj, blit_center_pos):
        self.window = graphic_obj
        self.width = 10
        self.height = 13
        self.center_pos = blit_center_pos
        self.damage_img = []
        self.miss_img = self.window.load_image(os.path.join("Info_Image", "Damage.png"))
        damage_img = self.window.load_image(os.path.join("Info_Image", "Damage.png"))
        damage_img.set_colorkey(damage_img.get_at((0, 0)))
        for i in range(1, 11):                                              # Parsing 傷害數字
            self.damage_img.append(damage_img.subsurface(self.window.create_rect((i-1) * self.width, 0, self.width, self.height)))
        self.damage_list = []

    def check_container(self):
        if len(self.damage_list) == 0:
            return False
        else:
            return True

    def add_damage(self, damage):
        damage = 9999999 if damage > 9999999 else damage
        damage_value = [int(d) for d in str(damage)]                        # 擷取傷害的每個數字
        self.damage_list.insert(0, [damage_value, 0])                       # [Token過的傷害, frame idx] 排序方式是越薪的越前面，這樣超過40 frame的傷害就可以從後面開始刪，在iterate時才不會有問題

    def generate_surface(self):
        if len(self.damage_list) == 0:
            return
        else:
            rect = self.window.create_rect(self.center_pos[0]-0-35, self.center_pos[1]-6-39, 7 * self.width, 52)
            bg = self.window.background.copy()
            surface = bg.subsurface(rect)
            for damage, frame in self.damage_list:
                if frame == 40:
                    self.damage_list.remove([damage, frame])
            for damage, frame in reversed(self.damage_list):
                bg2 = self.window.background.copy()
                rect2 = self.window.create_rect(0, 0, len(damage) * self.width, self.height)
                rect2.center = self.window.create_rect(self.center_pos[0]-len(damage)/2, self.center_pos[1]-self.height/2-frame, len(damage) * self.width, self.height).center
                dmg_surface = bg2.subsurface(rect2)
                for i in range(len(damage)):
                    dmg_surface.blit(self.damage_img[damage[i]], (i * self.width, 0))
                rect3 = self.window.create_rect(0, 38 - frame, 7 * self.width, self.height)
                rect2.center = rect3.center
                surface.blit(dmg_surface, rect2)
                self.damage_list[self.damage_list.index([damage, frame])][1] += 1
            return surface


    # def generate_damage(self, damage):
    #     damage = 9999999 if damage > 9999999 else damage
    #     damage_value = [int(d) for d in str(damage)]                        # 擷取傷害的每個數字
    #     bg = self.window.background.copy()
    #     rect = self.window.create_rect(0, 0, 7 * self.width, self.height)   # 預先撈出傷害所需要的最大畫面空間 (9999999) 為了避免顯示大的數字後顯示小數字會沒有把前一個數字蓋乾淨
    #     rect.center = self.center_pos                                       # pos是指這個畫面的中心位置
    #     surface = bg.subsurface(rect)                                       # surface 是最大傷害畫面區域的背景
    #
    #     bg2 = self.window.background.copy()
    #     rect2 = self.window.create_rect(0, 0, len(damage_value) * self.width, self.height)
    #     rect2.center = self.center_pos
    #     dmg_surface = bg2.subsurface(rect2)                                 # dmg_surface 是實際傷害的圖像，接著要把這兩個併起來
    #     for i in range(len(damage_value)):
    #         dmg_surface.blit(self.damage_img[damage_value[i]], (i * self.width, 0))
    #
    #     rect.topleft = (0, 0)                                               # 在blit時，總是以該圖自己內部的座標來指定，左上角總是0, 0
    #     rect2.center = rect.center                                          # 把surface與dmg_surface的中心點對齊後畫上去
    #     surface.blit(dmg_surface, rect2)
    #     return surface


