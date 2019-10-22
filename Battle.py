import math


Green = (0, 255, 0)


class BattleControl:
    def __init__(self, graphic_obj, background_path, char, enemy):
        self.window = graphic_obj
        self.background_path = background_path
        self.char = char
        self.enemy = enemy
        self.char_animate = []
        self.enemy_animate = []

    def run(self):
        idx = True
        while idx:
            self.window.set_bg_image(self.background_path, 255)
            self.window.set_status_window(self.char)
            self.window.chat_message = []
            self.window.set_chat_window(["按 [A] 開始戰鬥"], Green)
            idx = self.standby()

    def standby(self):
        self.char_animate = Animate(self.window, self.char.standby_img_path)
        while True:
            self.window.tick(10)
            content = self.window.get_key()
            if content == "esc":
                return False
            elif content == "a":
                self.attack()
                return True
            self.char_animate.update((self.window.width * 0.4 - self.char_animate.default_width / 2, self.window.height * 0.55 - self.char_animate.default_width / 2))

    def attack(self):
        fps = 60
        count = 1
        self.char_animate = Animate(self.window, self.char.attack_img_path)
        self.enemy_animate = Animate(self.window, self.enemy.attack_img_path)
        char_move_frq = math.floor(fps / self.char.attribute.att_frq / self.char_animate.image_count)
        enemy_move_frq = math.floor(fps / self.char.attribute.att_frq / self.enemy_animate.image_count)
        while True:
            self.window.tick(fps)
            content = self.window.get_key()
            if content == "esc":
                return

            if count % char_move_frq == 0:
                pos = (self.window.width * 0.4 - self.char_animate.default_width / 2, self.window.height * 0.55 - self.char_animate.default_width / 2)
                self.char_animate.update(pos)

            if count % enemy_move_frq == 0:
                pos = (self.window.width * 0.6 - self.enemy_animate.default_width / 2, self.window.height * 0.55 - self.enemy_animate.default_width / 2)
                self.enemy_animate.update(pos)
            count += 1



class Animate:
    def __init__(self, graphic_obj, standby_image_path):
        self.window = graphic_obj
        self.default_width = 200
        self.image = self.window.load_image(standby_image_path)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_count = self.image.get_size()[0] / self.default_width
        self.current = 0

    def update(self, pos):
        if self.current == self.image_count:
            self.current = 0
        self.current += 1
        ani_img = self.image.subsurface(self.window.create_rect((self.current-1) * self.default_width, 0, self.default_width, self.default_width))

        sub_bg = self.window.background.subsurface(self.window.create_rect(pos[0], pos[1], self.default_width, self.default_width))

        self.window.screen.blit(sub_bg, pos)
        self.window.screen.blit(ani_img, pos)
        self.window.update_screen()




