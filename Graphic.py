import os                                           # Built-in Library
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
        self.fps = 30
        self.chat_message = []
        self.chat_color = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        # 1 Chinese Character = 4 Space
        self.font = pygame.font.Font("TaipeiSansTCBeta-Bold.ttf", Font_size)
        self.clock = pygame.time.Clock()

    def clear_screen(self):
        self.screen.blit(self.create_color_surface(Black, pygame.Rect(0, 0, self.width, self.height), 255), (0, 0))
        pygame.display.update()

    def set_bg_image(self, file_path, alpha):
        self.clear_screen()
        img = pygame.image.load(file_path).convert()
        # Resize the surface to new resolution and output to dest_surface
        # then self.background will save the current background surface, it can be used for reload bg or create bg subsurface
        pygame.transform.scale(img, self.screen.get_size(), self.background)
        self.background.set_alpha(alpha)
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def set_message_box(self, surface_rect, text):
        # text = ["str1", "str2", "str3" ...]
        # return rect if message_box
        img = pygame.image.load(os.path.join("Info_Image", "win_msgbox.png"))
        img.set_colorkey(img.get_at((0, 0)))
        img = img.convert()
        dest_rect = img.get_rect()
        color = []
        for i in range(len(text)):
            color.append(Black)
        self.set_text(img, text, color, (dest_rect.width * 0.05, dest_rect.height * 0.20))
        dest_rect.center = surface_rect.center
        rect = self.screen.blit(img, dest_rect)
        pygame.display.update()
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
        pygame.display.update()
        return rect

    def get_cmd(self, input_rec):
        # return cmd when enter pressed, or return "" when esc pressed
        cmd = ""
        input_size = (input_rec.width, input_rec.height)
        while True:
            self.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:     # delete final char
                        cmd = cmd[:-1]
                    elif event.key == pygame.K_RETURN:      # return current cmd
                        self.set_block(Black, input_rec)
                        return cmd
                    elif event.key == pygame.K_ESCAPE:      # reset current cmd and clear block
                        cmd = ""
                        self.set_block(Black, input_rec)
                        pygame.display.update()
                    else:
                        border_detect = self.font.render(cmd, True, White)
                        if border_detect.get_size()[0] < 0.9 * input_rec.width:
                            cmd += event.unicode
                    self.set_block(Black, input_rec)
                    text_surface = pygame.Surface(input_size)
                    self.set_text(text_surface, [cmd], [White], (0, 0))
                    self.screen.blit(text_surface, input_rec)
                    pygame.display.update()
                elif event.type == pygame.QUIT:             # return empty string means keep getting cmd
                    self.set_block(Black, input_rec)
                    pygame.display.update()
                    pygame.quit()

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
        pygame.display.update()

    def set_status_window(self, char_obj):
        # char_obj = Character Class Object
        img = pygame.image.load(os.path.join("Info_Image", "basewin_mini.png")).convert()
        img.set_colorkey(img.get_at((0, 0)))        # Turn the default purple to transparent (need convert() first)
        img = self.set_status_text(img, char_obj)
        self.screen.blit(img, (0, 0))
        pygame.display.update()

    def reset_chat_message(self):
        self.chat_message = []
        self.chat_color = []

    def set_sit_char(self, sit_image_path):
        img = pygame.image.load(sit_image_path).convert()
        img.set_colorkey(img.get_at((0, 0)))
        width, height = img.get_size()
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (self.width * 0.4, self.height * 0.55)
        # self.screen.blit(img, (self.width * 0.4 - width / 2, self.height * 0.55 - height / 2))
        self.screen.blit(img, rect)
        pygame.display.update()

    @staticmethod
    def create_color_surface(color, rect, alpha):
        # color = (R, G, B)
        # rect = pygame.Rect(x, y, width, height)
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(color)
        surface.set_alpha(alpha)
        return surface.convert()

    @staticmethod
    def set_status_text(surface, char_obj):
        temp_font = pygame.font.Font("TaipeiSansTCBeta-Bold.ttf", 11)
        name_render = temp_font.render(char_obj.char_name, True, Black)
        status1 = "Lv. " + str(char_obj.base_level) + " / " + char_obj.job_name + " / Lv. " + str(char_obj.job_level) + " / Exp. " + str(char_obj.base_exp_per) + "%"
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
    def create_rect(x, y, width, height):
        # for other script to use without import pygame
        return pygame.Rect(x, y, width, height)

    def tick(self, fps):
        # for other script to use without import pygame
        return self.clock.tick(fps)

    @staticmethod
    def load_image(image_path):
        return pygame.image.load(image_path).convert()

    @staticmethod
    def update_screen(pos):
        pygame.display.update(pygame.Rect(pos))

    @staticmethod
    def effect_sound(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.2)
        sound.play()
