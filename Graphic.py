import os                                           # Built-in Library
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library

White = (255, 255, 255)
Black = (0, 0, 0)
Font_size = 14


class WindowClass:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load(os.path.join("BG_Image", "Logo.jpg"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Ragnarok Idle")
        self.width = 1024
        self.height = 768
        self.fps = 10
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.Font("TaipeiSansTCBeta-Bold.ttf", Font_size)
        # 1 Chinese Character = 5 Space
        self.clock = pygame.time.Clock()
        self.set_bg_image(os.path.join("BG_Image", "Login_BG.jpg"), 200)
        self.set_message_box(self.background.get_rect(), [ "Press [S] to Start New Game",
                                                           "              [L] to Load Data     ",
                                                           "              [E] to Exit          " ])

    def set_bg_image(self, file_path, alpha):
        self.clear_screen()
        img = pygame.image.load(file_path).convert()
        # Resize the surface to new resolution and output to dest_surface
        pygame.transform.scale(img, self.screen.get_size(), self.background)
        self.background.set_alpha(alpha)
        self.background.convert_alpha()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def set_message_box(self, surface_rect, text):
        # text = ["str1", "str2", "str3" ...]
        size = (350, 140)
        img = pygame.image.load(os.path.join("Info_Image", "Message_Empty.png")).convert()
        dest_surface = pygame.Surface(size).convert()
        pygame.transform.scale(img, size, dest_surface)
        dest_size = dest_surface.get_size()
        self.set_text(dest_surface, text, (0, 0, 0), (dest_size[0] * 0.05, dest_size[1] * 0.20))
        rect = self.screen.blit(dest_surface, (surface_rect.center[0] - (size[0] / 2), (surface_rect.center[1] - (size[1] / 2))))
        pygame.display.update()
        return rect

    def set_text(self, surface, text, color, offset):
        # offset = (width_offset, height_offset)
        # color = (R, G, B)
        max_w, max_h = surface.get_size()
        cur_w, cur_h = offset
        for line in text:
            word_h2 = 0
            for word in line:
                word_surface = self.font.render(word, True, color)
                word_w, word_h = word_surface.get_size()
                word_h2 = word_h
                if cur_w + word_w > max_w:
                    cur_w = offset[0]
                    cur_h += word_h
                surface.blit(word_surface, (cur_w, cur_h))
                cur_w += word_w
            cur_w = offset[0]
            cur_h += word_h2

    def set_block(self, size, color, pos):
        # size = (width, height)
        # color = (R, G, B)
        # pos = (x, y)
        surface = pygame.Surface(size)
        surface.fill(color)
        surface.convert()
        rect = self.screen.blit(surface, pos)
        pygame.display.update()
        return rect

    @staticmethod
    def play_bgm(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops = -1)

    def clear_screen(self):
        black_window = pygame.Surface((self.width, self.height))
        black_window.fill(Black)
        self.screen.blit(black_window, (0, 0))
        pygame.display.update()

    @staticmethod
    def get_key():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.unicode

    def get_cmd(self, input_rec):
        cmd = ""
        input_size = (input_rec.width, input_rec.height)
        while True:
            self.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:     # delete final char
                        cmd = cmd[:-1]
                    elif event.key == pygame.K_RETURN:      # return current cmd
                        self.set_block(input_size, Black, (input_rec.x, input_rec.y))
                        return cmd
                    elif event.key == pygame.K_ESCAPE:      # reset current cmd and clear block
                        cmd = ""
                        self.set_block(input_size, Black, (input_rec.x, input_rec.y))
                        pygame.display.update()
                    else:
                        border_detect = self.font.render(cmd, True, White)
                        if border_detect.get_size()[0] < 0.9 * input_rec.width:
                            cmd += event.unicode
                    self.set_block(input_size, Black, (input_rec.x, input_rec.y))
                    text_surface = pygame.Surface(input_size)
                    self.set_text(text_surface, [cmd], White, (0, 0))
                    self.screen.blit(text_surface, (input_rec.x, input_rec.y))
                    pygame.display.update()
                elif event.type == pygame.QUIT:             # return empty string means keep getting cmd
                    self.set_block(input_size, Black, (input_rec.x, input_rec.y))
                    pygame.display.update()
                    pygame.quit()

    def tick(self, fps):
        self.clock.tick(fps)

    # def cmd_detection(self):
    #     cmd = ""
    #     idx = 0
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_BACKSPACE:
    #                 cmd = cmd[:-1]
    #             elif event.key == pygame.K_RETURN:
    #                 idx = 1
    #             else:
    #                 cmd += event.unicode
    #         elif event.type == pygame.QUIT:
    #             idx = 2
    #     if idx == 0:
    #         self.clear_screen()
    #         self.display_text(cmd)
    #         return cmd
    #     elif idx == 1:
    #         self.clear_screen()
    #         return cmd
    #     elif idx == 2:
    #         self.clear_screen()
    #         return ""
