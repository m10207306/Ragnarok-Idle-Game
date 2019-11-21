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
        char_group = pygame.sprite.Group()
        char_group.add(Animate(self.window, self.char.standby_img_path, self.char.standby_img_path, char_pos))
        while True:
            self.window.tick(self.standby_fps)
            content = self.window.get_key()
            if content == "esc":
                return False
            elif content == "a":
                self.attack()
                return True
            char_group.clear(self.window.screen, self.window.background)
            char_group.update(1)
            char_group.draw(self.window.screen)
            pygame.display.update()

    def attack(self):
        self.window.reset_chat_message()
        monster = Character.MonsterClass(0)
        count = 1
        char_pos = (self.window.width * 0.4, self.window.height * 0.55)
        mons_pos = (self.window.width * 0.6, self.window.height * 0.55)
        char_animate_group = pygame.sprite.Group()
        mons_animate_group = pygame.sprite.Group()
        damage_group = pygame.sprite.Group()
        Damage.AllGroup = damage_group

        char_animate = Animate(self.window, self.char.standby_img_path, self.char.attack_img_path, char_pos, self.char, monster, (mons_pos[0], mons_pos[1] - 110))
        char_animate_group.add(char_animate)
        char_move_frq = math.floor(self.attack_fps / self.char.attribute.att_frq / char_animate.image_count)

        mons_animate = Animate(self.window, monster.standby_img_path, monster.attack_img_path, mons_pos, monster, self.char, (char_pos[0], char_pos[1] - 110))
        mons_animate_group.add(mons_animate)
        mons_move_frq = math.floor(self.attack_fps / monster.attribute.att_frq / mons_animate.image_count)

        mons_dead = False
        char_dead = False
        while True:
            self.window.tick(self.attack_fps)
            content = self.window.get_key()
            print(self.window.clock.get_fps())
            if content == "esc":
                return

            # 角色攻擊動畫
            if count % char_move_frq == 0:
                if count <= char_move_frq:
                    rect = pygame.Rect(0, 0, 200, 200)
                    rect.center = char_pos
                    self.window.screen.blit(self.window.background.subsurface(pygame.Rect(rect)), rect)
                else:   # 當第一次呼叫clear時不會有動作，因為他是根據上一次draw的內容做clear，所以才需要有上面的情境
                    char_animate_group.clear(self.window.screen, self.window.background)
                    char_animate_group.update(2)
                    char_animate_group.draw(self.window.screen)
            # 怪物攻擊動畫
            if count % mons_move_frq == 0:
                if count <= mons_move_frq:
                    rect = pygame.Rect(0, 0, 200, 200)
                    rect.center = mons_pos
                    self.window.screen.blit(self.window.background.subsurface(pygame.Rect(rect)), rect)
                else:
                    mons_animate_group.clear(self.window.screen, self.window.background)
                    mons_animate_group.update(2)
                    mons_animate_group.draw(self.window.screen)

            # 傷害動畫
            damage_group.clear(self.window.screen, self.window.background)
            damage_group.update()
            damage_group.draw(self.window.screen)
            pygame.display.update()

            # 判斷生死
            if monster.hp <= 0:
                self.char.get_exp(monster.base_exp, monster.job_exp)
                return
            if self.char.hp <= 0:
                self.char.exp_punish()
                self.char.respawn()
                return

            count += 1


class Animate(pygame.sprite.Sprite):
    def __init__(self, graphic_obj, standby_image_path, attack_image_path, center_pos, attacker = None, defencer = None, damage_pos = None):
        super().__init__()
        # 想以sprite.group的方式來控制動畫 property 中 image 與 rect 是必須的
        self.window = graphic_obj
        self.default_width = 200
        self.standby_image = self.window.load_image(standby_image_path)
        self.standby_image.set_colorkey(self.standby_image.get_at((0, 0)))
        self.attack_image = self.window.load_image(attack_image_path)
        self.attack_image.set_colorkey(self.attack_image.get_at((0, 0)))
        self.image_count = self.standby_image.get_size()[0] / self.default_width        # 原則上是6
        self.current = 0
        self.current_type = 0
        self.standby_image_array = []
        self.attack_image_array = []
        self.center_pos = center_pos
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
        self.attacker = attacker
        self.defencer = defencer
        self.damage_pos = damage_pos

    def update(self, type_flag):
        # Sprite.Group()當中override掉的function
        # type_flag: 1 = standby, 2 = attack, 3 = dead
        # 如果輸入進來的type_flag跟目前的self.current_type不同，則self.current歸0(代表動畫重置)
        if type_flag != self.current_type:
            self.current = 0
            self.current_type = type_flag
        if self.current == self.image_count:
            self.current = 0
        self.current += 1
        if type_flag == 1:
            self.update_standby()
        elif type_flag == 2:
            self.update_attack()
            if self.current == self.image_count:
                Damage.AllGroup.add(Damage(self.window, self.attacker, self.defencer, self.damage_pos))
        elif type_flag == 3:
            self.update_dead()
        else:
            print("Error Animation Update: parameter - type_flag = ", type_flag)
            return

    def update_standby(self):
        self.image = self.standby_image_array[self.current - 1]

    def update_attack(self):
        self.image = self.attack_image_array[self.current - 1]

    def update_dead(self):
        print("Handle Dead Animation")


class Damage(pygame.sprite.Sprite):
    AllGroup = None

    def __init__(self, graphic_obj, attacker, defencer, pos):
        super().__init__()
        self.window = graphic_obj
        self.image = self.window.create_transparent_surface(70, 60)     # transparent surface
        self.rect = self.image.get_rect()
        self.rect.center = pos                                          # set to target position
        damage, flag = self.calculate_damage(attacker, defencer)
        defencer.hp -= damage
        rect1 = pygame.Rect(0, 0, 70, 60)
        if flag == 3:
            rect2 = self.window.miss_template.get_rect()
            rect2.center = rect1.center
            self.image.blit(self.window.miss_template, rect2)
        elif flag == 1 or flag == 2:
            if flag == 2:
                self.image.blit(self.window.cri_template, (0, 0))
            damage_sur = self.generate_surface(damage, flag)
            rect2 = damage_sur.get_rect()
            rect2.center = rect1.center
            self.image.blit(damage_sur, rect2)
        self.life = 0

    def generate_surface(self, damage, flag):
        damage = 9999999 if damage > 9999999 else damage
        damage_value = [int(d) for d in str(damage)]
        damage_surface = self.window.create_transparent_surface(10*len(damage_value), 13)
        for i in range(len(damage_value)):
            if flag == 1:
                damage_surface.blit(self.window.damage_template[damage_value[i]], (i*10, 0))
            elif flag == 2:
                damage_surface.blit(self.window.damage_cri_template[damage_value[i]], (i*10, 0))
        return damage_surface

    def calculate_damage(self, attacker, defencer):
        # 先判斷是否命中
        if attacker.attribute.hit < defencer.attribute.flee + 100:
            if self.trigger_or_not(round(attacker.attribute.hit / (defencer.attribute.flee + 100), 2)):
                self.window.effect_sound(os.path.join("Effect_Sound", "_attack_sword_miss.wav"))
                return 0, 3
        defence_ratio = round((4000 + defencer.attribute.total_defence) / (4000 + defencer.attribute.total_defence * 10), 2)
        damage_value = random.randint(attacker.attribute.total_atk[0], attacker.attribute.total_atk[1])
        damage_value *= defence_ratio
        # 再判斷是否爆擊
        if self.trigger_or_not(round(attacker.attribute.cri / 100, 2)):
            damage_value *= 1.5
            self.window.effect_sound(os.path.join("Effect_Sound", "ef_hit2_critical.wav"))
            return math.floor(damage_value), 2

        self.window.effect_sound(os.path.join("Effect_Sound", "_hit_dagger.wav"))
        # return [damage_value, type]    type1 = 普通  type2 = 爆擊  type3 = miss
        return math.floor(damage_value), 1

    def update(self):
        if self.life >= 40:
            Damage.AllGroup.remove(self)
        self.rect.y -= 2
        self.life += 1

    @staticmethod
    def trigger_or_not(probability):
        return random.randint(1, 100) >= (1 - probability) * 100
