import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library

White = (255, 255, 255)
Black = (0, 0, 0)
Font_size = 16


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
        self.font = pygame.font.Font("Cascadia.ttf", Font_size)
        self.clock = pygame.time.Clock()
        self.set_bg_image(os.path.join("BG_Image", "Login_BG3.jpg"), self.background, 200)
        self.set_message_box(self.background.get_rect(), (350, 140), ["Press [S] to Start New Game",
                                                                      "      [L] to Load Data     ",
                                                                      "      [E] to Exit"])

        while True:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def set_bg_image(self, file_path, dest_surface, alpha):
        self.clear_screen()
        img = pygame.image.load(file_path).convert()
        # Resize the surface to new resolution and output to dest_surface
        pygame.transform.scale(img, self.screen.get_size(), dest_surface)
        dest_surface.set_alpha(alpha)
        dest_surface.convert_alpha()
        self.screen.blit(dest_surface, (0, 0))
        pygame.display.update()

    def set_message_box(self, surface_rect, size, text):
        # text = ["str1", "str2", "str3" ...]
        # size = (width, height)
        img = pygame.image.load(os.path.join("Info_Image", "Message_Empty.png")).convert()
        dest_surface = pygame.Surface(size).convert()
        pygame.transform.scale(img, size, dest_surface)
        dest_size = dest_surface.get_size()
        self.set_text(dest_surface, text, (0, 0, 0), (dest_size[0] * 0.10, dest_size[1] * 0.20))
        self.screen.blit(dest_surface, (surface_rect.center[0] - (size[0] / 2), (surface_rect.center[1] - (size[1] / 2))))
        pygame.display.update()

    def set_text(self, surface, text, color, offset):
        # offset = (width_offset, height_offset)
        # color = (R, G, B)
        max_w, max_h = surface.get_size()
        cur_w, cur_h = offset
        for line in text:
            for word in line:
                word_surface = self.font.render(word, True, color)
                word_w, word_h = word_surface.get_size()
                if cur_w + word_w > max_w:
                    cur_w = offset[0]
                    cur_h += word_h
                surface.blit(word_surface, (cur_w, cur_h))
                cur_w += word_w
            cur_w = offset[0]
            cur_h += word_h

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

    # @staticmethod
    # def key_detection():
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             return event.unicode

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

    # def clear_screen(self):
    #     self.screen.fill(Black)
    #     pygame.display.update()
    #
    # def display_text(self, text):
    #     rendered_text = self.font.render(text, True, (255, 255, 255))
    #     rect = rendered_text.get_rect()
    #     self.screen.blit(rendered_text, rect)
    #     pygame.display.flip()
