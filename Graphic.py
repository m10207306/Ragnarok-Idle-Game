import os, math                                     # Built-in Library
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library
import Character

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Font_size = 12


class WindowClass:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load(os.path.join("BG_Image", "Logo.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Ragnarok Idle")
        self.width = 1024
        self.height = 768
        self.fps = 60
        self.chat_message = []
        self.chat_color = []
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size())
        # 1 Chinese Character = 4 Space
        self.font = pygame.font.Font("TaipeiSansTCBeta-Bold.ttf", Font_size)
        self.clock = pygame.time.Clock()
        self.damage_template = []
        self.damage_cri_template = []
        self.miss_template = []
        self.cri_template = []
        self.token_damage_image()

    def clear_screen(self):
        self.screen.blit(self.create_color_surface(Black, pygame.Rect(0, 0, self.width, self.height), 255), (0, 0))

    def set_bg_image(self, file_path, alpha):
        self.clear_screen()
        img = pygame.image.load(file_path).convert_alpha()
        # Resize the surface to new resolution and output to dest_surface
        # then self.background will save the current background surface, it can be used for reload bg or create bg subsurface
        pygame.transform.scale(img, self.screen.get_size(), self.background)
        self.background.set_alpha(alpha)
        self.screen.blit(self.background, (0, 0))

    def set_message_box(self, center_pos, text):
        # text = ["str1", "str2", "str3" ...]
        # return rect if message_box
        img = pygame.image.load(os.path.join("Info_Image", "win_msgbox.png")).convert_alpha()
        # img.set_colorkey(img.get_at((0, 0)))
        dest_rect = img.get_rect()
        color = []
        for i in range(len(text)):
            color.append(Black)
        self.set_text(img, text, color, (dest_rect.width * 0.05, dest_rect.height * 0.20))
        dest_rect.center = center_pos
        rect = self.screen.blit(img, dest_rect)
        return rect

    def set_text(self, surface, text, color, offset):
        # It seems that surface needs always be converted
        # offset = (width_offset, height_offset)
        # color = (R, G, B)
        max_w, max_h = surface.get_size()
        cur_w, cur_h = offset
        color_idx = 0
        for line in text:
            word_h2 = 0
            for word in line:
                word_surface = self.font.render(word, True, color[color_idx])
                word_w, word_h = word_surface.get_size()
                word_h += 3                                 # increase the space between lines
                word_h2 = word_h
                if cur_w + word_w > max_w:
                    cur_w = offset[0]
                    cur_h += word_h
                surface.blit(word_surface, (cur_w, cur_h))
                cur_w += word_w
            cur_w = offset[0]
            cur_h += word_h2
            color_idx += 1

    def set_block(self, color, rect):
        # color = (R, G, B)
        # rect = pygame.Rect(x, y, width, height)
        surface = self.create_color_surface(color, rect, 255)
        rect = self.screen.blit(surface, rect)
        return rect

    def get_cmd(self, background_color, rect):
        # return cmd when enter pressed, or return "" when esc pressed
        self.set_block(background_color, rect)
        pygame.display.update()
        cmd = ""
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:     # delete final char
                        cmd = cmd[:-1]
                    elif event.key == pygame.K_RETURN:      # return current cmd
                        self.set_block(Black, rect)
                        return cmd
                    elif event.key == pygame.K_ESCAPE:      # reset current cmd and clear block
                        cmd = ""
                        self.set_block(Black, rect)
                    else:
                        if len(cmd) < 12:                   # 考慮到status window，限制只能輸入12個字
                            cmd += event.unicode
                    self.set_block(Black, rect)
                    text_surface = pygame.Surface(rect.size)
                    self.set_text(text_surface, [cmd], [White], (0, 0))
                    self.screen.blit(text_surface, rect)
                    pygame.display.update()

    def set_chat_window(self, content, color):
        # content = ["str1", "str2", ...]
        # can store 15 lines content
        size = (680, 235)
        line_limit = 15
        if not len(self.chat_message) < line_limit:
            self.chat_message.pop(-1)                            # remove first element
        self.chat_message = content + self.chat_message         # concatenate 2 list, keep 17 elements in list
        self.chat_color = color + self.chat_color
        chat_surface = self.create_color_surface(Black, pygame.Rect(0, 0, size[0], size[1]), 150)

        text_surface = pygame.Surface(size)
        self.set_text(text_surface, self.chat_message, self.chat_color, (0, 0))
        text_surface.set_colorkey(Black)
        text_surface.convert()

        sub_bg = self.background.subsurface(pygame.Rect(0, self.height - size[1], size[0], size[1]))
        self.screen.blit(sub_bg, (0, self.height - size[1]))
        self.screen.blit(chat_surface, (0, self.height - size[1]))
        self.screen.blit(text_surface, (0, self.height - size[1]))

    def set_status_window(self, char_obj):
        # char_obj = Character Class Object
        img = pygame.image.load(os.path.join("Info_Image", "basewin_mini.png")).convert_alpha()
        # img.set_colorkey(img.get_at((0, 0)))        # Turn the default purple to transparent (need convert() first)
        img = self.set_status_text(img, char_obj)
        self.screen.blit(img, (0, 0))

    def reset_chat_message(self):
        self.chat_message = []
        self.chat_color = []

    def set_sit_char(self, sit_image_path, pos):
        img = pygame.image.load(sit_image_path).convert_alpha()
        width, height = img.get_size()
        rect = pygame.Rect(0, 0, width, height)
        rect.center = pos
        self.screen.blit(img, rect)

    def token_damage_image(self):
        damage_img = pygame.image.load(os.path.join("Info_Image", "Damage.png")).convert_alpha()
        damage_cri_img = pygame.image.load(os.path.join("Info_Image", "Damage_Critical.png")).convert_alpha()
        self.miss_template = pygame.image.load(os.path.join("Info_Image", "Miss.png")).convert_alpha()
        self.cri_template = pygame.image.load(os.path.join("Info_Image", "Critical.png")).convert_alpha()
        digit_width = 10
        digit_height = 13
        for i in range(1, 11):
            self.damage_template.append(damage_img.subsurface(pygame.Rect((i-1) * digit_width, 0, digit_width, digit_height)))
            self.damage_cri_template.append(damage_cri_img.subsurface(pygame.Rect((i-1) * digit_width, 0, digit_width, digit_height)))

    def set_text_block(self, surface, text, center_pos):
        text_surface = self.font.render(text, True, White)
        rect1 = text_surface.get_rect()
        rect1.center = center_pos
        text_base = self.create_color_surface(Black, pygame.Rect(rect1.x, rect1.y, rect1.width+12, rect1.height+4), 128)
        rect2 = text_base.get_rect()
        rect2.center = center_pos
        surface.blit(text_base, rect2)
        surface.blit(text_surface, rect1)

    def interlude_black_window(self):
        count = 1
        black_sur = self.create_color_surface(Black, pygame.Rect(0, 0, self.width, self.height), 40)
        while True:
            self.clock.tick(self.fps)
            self.get_key()
            print(self.clock.get_fps())
            if count > 30:
                break
            self.screen.blit(black_sur, (0, 0))
            pygame.display.update()
            count += 1

    @staticmethod
    def create_health_bar(surface, char_obj, center_pos):
        hp_ratio = math.floor(char_obj.hp / char_obj.attribute.max_hp * 100 / 2)    # 0 - 100 整數
        sp_ratio = math.floor(char_obj.sp / char_obj.attribute.max_sp * 100 / 2)
        hp_color = (13, 242, 39)
        sp_color = (9, 90, 219)
        empty_color = (61, 69, 70)
        border_color = (32, 28, 103)
        width, height = 50, 8
        bar_surface = pygame.Surface((width, height)).convert()
        bar_surface.fill(empty_color)

        if hp_ratio > 0:
            hp_bar = pygame.Surface((hp_ratio, height/2)).convert()
            hp_bar.fill(hp_color)
            bar_surface.blit(hp_bar, (0, 0))
        if sp_ratio > 0:
            sp_bar = pygame.Surface((sp_ratio, height/2)).convert()
            sp_bar.fill(sp_color)
            bar_surface.blit(sp_bar, (0, height/2))

        pygame.draw.rect(bar_surface, border_color, (0, 0, width, height), 1)
        rect = bar_surface.get_rect()
        rect.center = center_pos
        surface.blit(bar_surface, rect)

    @staticmethod
    def create_transparent_surface(width, height):
        surface = pygame.Surface((width, height)).convert()
        surface.set_colorkey((0, 0, 0))
        return surface

    @staticmethod
    def create_color_surface(color, rect, alpha):
        # color = (R, G, B)
        # rect = pygame.Rect(x, y, width, height)
        # 這個會強制把整個Surface化為透明，就算之後再對他畫任何內容也看不到，因此如果是要一個透明的底來畫東西要用create_transparent_surface()
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(color)
        surface.set_alpha(alpha)
        return surface.convert()

    @staticmethod
    def set_status_text(surface, char_obj):
        temp_font = pygame.font.Font("TaipeiSansTCBeta-Bold.ttf", 11)
        name_render = temp_font.render(char_obj.char_name, True, Black)
        exp_percentrage = round(char_obj.base_exp / char_obj.target_base_exp * 100, 2)
        status1 = "Lv. " + str(char_obj.base_level) + " / " + char_obj.job_name + " / Lv. " + str(char_obj.job_level) + " / Exp. " + str(exp_percentrage) + "%"
        status2 = "HP " + str(char_obj.hp) + " / " + str(char_obj.attribute.max_hp) + " | SP " + str(char_obj.sp) + " / " + str(char_obj.attribute.max_sp) + " | " + str(Character.tool_money_format(char_obj.zeny)) + " Z"
        max_width, max_height = surface.get_size()
        surface.blit(name_render, (0.02 * max_width, 0.08 * max_height))
        status1_render = temp_font.render(status1, True, Black)
        width, height = status1_render.get_size()
        surface.blit(status1_render, (0.95 * max_width - width, 0.1 * max_height))
        status2_render = temp_font.render(status2, True, Black)
        width, height = status2_render.get_size()
        surface.blit(status2_render, (0.95 * max_width - width, 0.6 * max_height))
        return surface

    @staticmethod
    def play_bgm(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops = -1)

    @staticmethod
    def get_key():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "esc"
                elif event.key == pygame.K_RETURN:
                    return "enter"
                elif event.key == pygame.K_BACKSPACE:
                    return "backspace"
                else:
                    return event.unicode

    @staticmethod
    def effect_sound(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.2)
        sound.play()
