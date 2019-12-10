import math, os, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # Python重複import也不會像C++一樣有影響，sys.module中如果已存在就只是reference過來

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class Animate(pygame.sprite.Sprite):
    def __init__(self, graphic_obj, standby_image_path, attack_image_path, dead_image_path, center_pos, attacker=None,
                 defencer=None, damage_pos=None):
        super().__init__()
        # 想以sprite.group的方式來控制動畫 property 中 image 與 rect 是必須的
        self.window = graphic_obj
        self.default_width = 200
        self.standby_image = pygame.image.load(standby_image_path).convert_alpha()
        # self.standby_image.set_colorkey(self.standby_image.get_at((0, 0)))
        self.attack_image = pygame.image.load(attack_image_path).convert_alpha()
        # self.attack_image.set_colorkey(self.attack_image.get_at((0, 0)))
        self.dead_image = pygame.image.load(dead_image_path).convert_alpha()
        self.image_count = self.standby_image.get_size()[0] / self.default_width  # 原則上是6
        self.current = 0
        self.current_type = 0
        self.standby_image_array = []
        self.attack_image_array = []
        self.dead_image_array = []
        self.center_pos = center_pos
        for i in range(1, int(self.image_count) + 1):  # Parsing 攻擊動畫
            self.standby_image_array.append(self.standby_image.subsurface(pygame.Rect((i - 1) * self.default_width,
                                                                                      0,
                                                                                      self.default_width,
                                                                                      self.default_width)))
            self.attack_image_array.append(self.attack_image.subsurface(pygame.Rect((i - 1) * self.default_width,
                                                                                    0,
                                                                                    self.default_width,
                                                                                    self.default_width)))
            self.dead_image_array.append(self.dead_image.subsurface(pygame.Rect((i - 1) * self.default_width,
                                                                                0,
                                                                                self.default_width,
                                                                                self.default_width)))
        self.rect = pygame.Rect(0, 0, self.default_width, self.default_width)
        self.rect.center = self.center_pos
        self.image = []
        self.attacker = attacker
        self.defencer = defencer
        self.damage_pos = damage_pos

    def update(self, type_flag, alpha):
        # Sprite.Group()當中override掉的function
        # type_flag: 1 = standby, 2 = attack, 3 = dead
        # 如果輸入進來的type_flag跟目前的self.current_type不同，則self.current歸0(代表動畫重置)
        if type_flag != self.current_type:
            self.current = 0
            self.current_type = type_flag
        if self.current == self.image_count:  # 動畫播完reset重播
            self.current = 0
        self.current += 1
        if type_flag == 1:  # 待機動畫
            self.update_standby(alpha)
        elif type_flag == 2:  # 攻擊動畫
            self.update_attack(alpha)
            if self.current == self.image_count:
                Damage.AllGroup.add(Damage(self.window, self.attacker, self.defencer, self.damage_pos))
        elif type_flag == 3:  # 死亡動畫
            self.update_dead(alpha)
        else:
            print("Error Animation Update: parameter - type_flag = ", type_flag)
            return

    def update_standby(self, alpha):
        copy = self.standby_image_array[self.current - 1].copy()
        # self.image.set_alpha(alpha)       # 因為使用convert_alpha()處理影像，所以沒辦法直接用surface alpha
        if alpha < 255:
            alpha_surface = pygame.Surface(copy.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, alpha))
            copy.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = copy

    def update_attack(self, alpha):
        copy = self.attack_image_array[self.current - 1]
        # self.image.set_alpha(alpha)
        if alpha < 255:
            alpha_surface = pygame.Surface(copy.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, alpha))
            copy.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = copy

    def update_dead(self, alpha):
        copy = self.dead_image_array[self.current - 1]
        if alpha < 255:
            alpha_surface = pygame.Surface(copy.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, alpha))
            copy.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = copy


class Damage(pygame.sprite.Sprite):
    AllGroup = None

    def __init__(self, graphic_obj, attacker, defencer, pos):
        super().__init__()
        self.window = graphic_obj
        self.image = self.window.create_transparent_surface(70, 60)  # transparent surface
        self.rect = self.image.get_rect()
        self.rect.center = pos  # set to target position
        damage, flag = self.calculate_damage(attacker, defencer)  # 傷害計算(普通、爆擊、迴避，含音效)
        defencer.hp -= damage  # 傷害傳遞
        rect1 = pygame.Rect(0, 0, 70, 60)
        if flag == 3:  # 迴避
            rect2 = self.window.miss_template.get_rect()
            rect2.center = rect1.center
            self.image.blit(self.window.miss_template, rect2)
        elif flag == 1 or flag == 2:  # 普通or爆擊，差別在是否有爆擊動畫與數字顏色
            if flag == 2:
                self.image.blit(self.window.cri_template, (0, 0))
            damage_sur = self.generate_surface(damage, flag)
            rect2 = damage_sur.get_rect()
            rect2.center = rect1.center
            self.image.blit(damage_sur, rect2)
        self.life = 0  # 傷害數字動畫壽命(40個frame)

    def generate_surface(self, damage, flag):
        damage = 9999999 if damage > 9999999 else damage
        damage_value = [int(d) for d in str(damage)]
        damage_surface = self.window.create_transparent_surface(10 * len(damage_value), 13)
        for i in range(len(damage_value)):
            if flag == 1:
                damage_surface.blit(self.window.damage_template[damage_value[i]], (i * 10, 0))
            elif flag == 2:
                damage_surface.blit(self.window.damage_cri_template[damage_value[i]], (i * 10, 0))
        return damage_surface

    def calculate_damage(self, attacker, defencer):
        # 先判斷是否命中
        if attacker.attribute.hit < defencer.attribute.flee + 100:
            if not self.trigger_or_not(round(attacker.attribute.hit / (defencer.attribute.flee + 100), 2)):     # 代表miss
                self.window.effect_sound(os.path.join("Effect_Sound", "_attack_sword_miss.wav"))
                return 0, 3
        defence_ratio = round(
            (4000 + defencer.attribute.total_defence) / (4000 + defencer.attribute.total_defence * 10), 2)
        damage_value = random.randint(attacker.attribute.total_atk[0], attacker.attribute.total_atk[1])
        damage_value *= defence_ratio
        # 再判斷是否爆擊
        if self.trigger_or_not(round(attacker.attribute.cri / 100, 2)):
            damage_value *= 1.5
            self.window.effect_sound(os.path.join("Effect_Sound", "ef_hit2_critical.wav"))
            return round(damage_value), 2

        self.window.effect_sound(os.path.join("Effect_Sound", "_hit_dagger.wav"))
        # return damage_value, type    type1 = 普通  type2 = 爆擊  type3 = miss
        return round(damage_value), 1

    def update(self):
        if self.life >= 40:
            Damage.AllGroup.remove(self)
        self.rect.y -= 2
        self.life += 1

    @staticmethod
    def trigger_or_not(probability):
        return random.randint(1, 100) <= int(probability * 100)
