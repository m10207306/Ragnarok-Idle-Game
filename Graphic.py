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
        logo = pygame.image.load(os.path.join("BG_Image", "logo.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Ragnarok Idle")
        pygame.mouse.set_visible(False)
        self.width = 1024
        self.height = 768
        self.fps = 60
        self.chat_message = []
        self.chat_color = []
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size())
        self.font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", Font_size)
        self.clock = pygame.time.Clock()
        self.miss_template = pygame.image.load(os.path.join("Info_Image", "miss.png")).convert_alpha()
        self.message_win_template = pygame.image.load(os.path.join("Info_Image", "Win_msgbox.png")).convert_alpha()
        self.chat_input_template = pygame.image.load(os.path.join("Info_Image", "dialog_bg.png")).convert_alpha()
        self.status_win_template = pygame.image.load(os.path.join("Info_Image", "basewin_mini.png")).convert_alpha()
        self.equip_ability_template = pygame.image.load(os.path.join("Info_Image", "equipwin_bg.png")).convert_alpha()
        self.create_char_template = pygame.image.load(os.path.join("Info_Image", "win_make.png")).convert_alpha()
        self.cri_template = pygame.image.load(os.path.join("Info_Image", "critical.png")).convert_alpha()
        self.damage_template = []
        self.damage_cri_template = []
        self.pointer_template = []
        self.txt_win_template = []
        self.btn_ok_template = []
        self.btn_cancel_template = []
        self.btn_ability_template = []
        self.btn_inter_template = []
        self.btn_r_arw_template = []
        self.load_template_image()

    def clear_screen(self):
        self.screen.blit(self.create_color_surface(Black, pygame.Rect(0, 0, self.width, self.height), 255), (0, 0))

    def set_bg_image(self, file_path, alpha):       # 更新背景，並儲存背景
        self.clear_screen()
        img = pygame.image.load(file_path).convert_alpha()
        # Resize the surface to new resolution and output to dest_surface
        # then self.background will save the current background surface, it can be used for reload bg or create bg subsurface
        pygame.transform.scale(img, self.screen.get_size(), self.background)
        self.background.set_alpha(alpha)
        self.screen.blit(self.background, (0, 0))

    def get_map_icon(self, file_path):          # 產生小地圖(半透明)
        img = pygame.image.load(file_path).convert_alpha()
        rect = img.get_rect()
        img2 = pygame.Surface((rect.width//2, rect.height//2)).convert()
        img2.set_alpha(200)
        pygame.transform.scale(img, (rect.width//2, rect.height//2), img2)
        return img2

    def get_resize_surface(self, img1, target_size):
        img2 = pygame.Surface(target_size).convert_alpha()
        pygame.transform.scale(img1, target_size, img2)
        return img2

    def set_text(self, surface, text, color, offset):       # 在輸入的Surface上畫上文字，並且如果文字太長會自動換行
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

    def get_chat_win(self, content, color):      # 創造聊天室
        # content = ["str1", "str2", ...]
        # can store 15 lines content
        size = (600, 221)
        line_limit = 12
        self.chat_message = self.chat_message + content  # concatenate 2 list, keep 15 elements in list
        self.chat_color = self.chat_color + color
        while not len(self.chat_message) < line_limit:
            self.chat_message.pop(0)                           # 刪除最舊的訊息
            self.chat_color.pop(0)
        chat_bg = self.background.subsurface(pygame.Rect(0, self.height - size[1] - self.chat_input_template.get_size()[1], size[0], size[1])).copy()
        chat_ground_surface = self.create_color_surface(Black, pygame.Rect(0, 0, size[0], size[1]), 150)
        chat_bg.blit(chat_ground_surface, (0, 0))
        self.set_text(chat_bg, self.chat_message, self.chat_color, (0, 0))
        return chat_bg

    def get_status_win(self, char_obj): # 創造人物基本資訊視窗
        # char_obj = Character Class Object
        img = self.status_win_template.copy()
        img = self.set_status_text(img, char_obj)
        return img

    def reset_chat_message(self):       # 清空聊天室的聊天內容
        self.chat_message = []
        self.chat_color = []

    def load_template_image(self):      # 載入影像，通常是需要做些處理或是格式安排的部分才放在這
        self.txt_win_template = \
        [
            [pygame.image.load(os.path.join("Info_Image", "titlebar_left.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "titlebar_mid.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "titlebar_right.png")).convert_alpha()],
            [pygame.image.load(os.path.join("Info_Image", "txtbox_lu.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_mu.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_ru.png")).convert_alpha()],
            [pygame.image.load(os.path.join("Info_Image", "txtbox_lm.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_mm.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_rm.png")).convert_alpha()],
            [pygame.image.load(os.path.join("Info_Image", "txtbox_ld.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_md.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "txtbox_rd.png")).convert_alpha()],
            [pygame.image.load(os.path.join("Info_Image", "btnbar_left.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "btnbar_mid.png")).convert_alpha(),
             pygame.image.load(os.path.join("Info_Image", "btnbar_right.png")).convert_alpha()]
        ]
        self.btn_ok_template = [pygame.image.load(os.path.join("Info_Image", "btn_ok.png")).convert_alpha(),
                                pygame.image.load(os.path.join("Info_Image", "btn_ok_a.png")).convert_alpha(),
                                pygame.image.load(os.path.join("Info_Image", "btn_ok_b.png")).convert_alpha()]

        self.btn_cancel_template = [pygame.image.load(os.path.join("Info_Image", "btn_cancel.png")).convert_alpha(),
                                    pygame.image.load(os.path.join("Info_Image", "btn_cancel_a.png")).convert_alpha(),
                                    pygame.image.load(os.path.join("Info_Image", "btn_cancel_b.png")).convert_alpha()]
        self.btn_inter_template = [
                                    [pygame.image.load(os.path.join("Info_Image", "btn_battle_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_battle_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_battle_3.png")).convert_alpha()],
                                    [pygame.image.load(os.path.join("Info_Image", "btn_equip_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_equip_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_equip_3.png")).convert_alpha()],
                                    [pygame.image.load(os.path.join("Info_Image", "btn_info_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_info_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_info_3.png")).convert_alpha()],
                                    [pygame.image.load(os.path.join("Info_Image", "btn_item_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_item_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_item_3.png")).convert_alpha()],
                                    [pygame.image.load(os.path.join("Info_Image", "btn_map_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_map_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_map_3.png")).convert_alpha()],
                                    [pygame.image.load(os.path.join("Info_Image", "btn_skill_1.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_skill_2.png")).convert_alpha(),
                                     pygame.image.load(os.path.join("Info_Image", "btn_skill_3.png")).convert_alpha()]
                                  ]
        self.btn_r_arw_template = [pygame.image.load(os.path.join("Info_Image", "arw_right0.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("Info_Image", "arw_right1.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("Info_Image", "arw_right2.png")).convert_alpha()]
        # 把每個Button送進去resize，然後長寬各乘2倍
        self.btn_inter_template = \
            [[self.get_resize_surface(j, [k*2 for k in j.get_size()]) for j in i] for i in self.btn_inter_template]
        damage_img = pygame.image.load(os.path.join("Info_Image", "damage.png")).convert_alpha()
        damage_cri_img = pygame.image.load(os.path.join("Info_Image", "damage_Critical.png")).convert_alpha()
        pointer_img = pygame.image.load(os.path.join("Info_Image", "pointer.png")).convert_alpha()
        damage_img = self.get_resize_surface(damage_img, (int(damage_img.get_size()[0] * 1.5), int(damage_img.get_size()[1] * 1.5)))
        damage_cri_img = self.get_resize_surface(damage_cri_img, (int(damage_cri_img.get_size()[0] * 1.5), int(damage_cri_img.get_size()[1] * 1.5)))
        damage_width = damage_img.get_size()[0] / 10
        damage_height = damage_img.get_size()[1]
        ptr_width = 22
        ptr_height = 31
        for i in range(1, damage_img.get_size()[0] // int(damage_width) + 1):
            self.damage_template.append(damage_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
            self.damage_cri_template.append(damage_cri_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
        for i in range(1, pointer_img.get_size()[0] // ptr_width + 1):
            self.pointer_template.append(pointer_img.subsurface(pygame.Rect((i-1) * ptr_width, 0, ptr_width, ptr_height)))

    def get_text_block(self, text, center_pos):     # 用於一塊底色(半透明)+文字的Surface
        text_surface = self.font.render(text, True, White)
        rect1 = text_surface.get_rect()
        text_base = self.create_color_surface(Black, pygame.Rect(rect1.x, rect1.y, rect1.width+12, rect1.height+4), 128)
        rect2 = text_base.get_rect()
        rect2.center = center_pos
        bg = self.background.subsurface(rect2).copy()
        rect1.center = bg.get_rect().center
        bg.blit(text_base, (0, 0))
        bg.blit(text_surface, rect1)
        return bg

    def interlude_black_window(self):       # 漸黑屏轉場
        count = 1
        black_sur = self.create_color_surface(Black, pygame.Rect(0, 0, self.width, self.height), 40)
        while True:
            self.clock.tick(self.fps)
            self.input_detect()         # 有點不確定為什麼沒有這行就會有問題
            if count > 25:
                break
            self.screen.blit(black_sur, (0, 0))
            pygame.display.update()
            count += 1

    def create_ability_initial_win(self, ability):      # 創角初始素質的介面
        return_sur = self.create_char_template.copy()
        stand_char = pygame.image.load(os.path.join("Char_Image", "Novice", "Stand.png")).convert_alpha()
        rect = stand_char.get_rect()
        rect.center = (95, 178)
        vertical_bias = [0, 3, 10, 20, 30, 40, 50, 60, 70, 79]
        nonvertical_xbias = [0, 3, 8, 16, 25, 33, 41, 49, 57, 67]
        nonvertical_ybias = [0, 3, 5, 10, 15, 20, 25, 30, 35, 41]
        center_pos = (288, 165)
        str_idx = [center_pos, (center_pos[0], center_pos[1] - vertical_bias[1]),
                   (center_pos[0], center_pos[1] - vertical_bias[2]), (center_pos[0], center_pos[1] - vertical_bias[3]),
                   (center_pos[0], center_pos[1] - vertical_bias[4]), (center_pos[0], center_pos[1] - vertical_bias[5]),
                   (center_pos[0], center_pos[1] - vertical_bias[6]), (center_pos[0], center_pos[1] - vertical_bias[7]),
                   (center_pos[0], center_pos[1] - vertical_bias[8]), (center_pos[0], center_pos[1] - vertical_bias[9])]
        int_idx = [center_pos, (center_pos[0], center_pos[1] + vertical_bias[1]),
                   (center_pos[0], center_pos[1] + vertical_bias[2]), (center_pos[0], center_pos[1] + vertical_bias[3]),
                   (center_pos[0], center_pos[1] + vertical_bias[4]), (center_pos[0], center_pos[1] + vertical_bias[5]),
                   (center_pos[0], center_pos[1] + vertical_bias[6]), (center_pos[0], center_pos[1] + vertical_bias[7]),
                   (center_pos[0], center_pos[1] + vertical_bias[8]), (center_pos[0], center_pos[1] + vertical_bias[9])]
        agi_idx = [center_pos,
                   (center_pos[0] - nonvertical_xbias[1], center_pos[1] - nonvertical_ybias[1]),
                   (center_pos[0] - nonvertical_xbias[2], center_pos[1] - nonvertical_ybias[2]),
                   (center_pos[0] - nonvertical_xbias[3], center_pos[1] - nonvertical_ybias[3]),
                   (center_pos[0] - nonvertical_xbias[4], center_pos[1] - nonvertical_ybias[4]),
                   (center_pos[0] - nonvertical_xbias[5], center_pos[1] - nonvertical_ybias[5]),
                   (center_pos[0] - nonvertical_xbias[6], center_pos[1] - nonvertical_ybias[6]),
                   (center_pos[0] - nonvertical_xbias[7], center_pos[1] - nonvertical_ybias[7]),
                   (center_pos[0] - nonvertical_xbias[8], center_pos[1] - nonvertical_ybias[8]),
                   (center_pos[0] - nonvertical_xbias[9], center_pos[1] - nonvertical_ybias[9])]
        vit_idx = [center_pos,
                   (center_pos[0] + nonvertical_xbias[1], center_pos[1] - nonvertical_ybias[1]),
                   (center_pos[0] + nonvertical_xbias[2], center_pos[1] - nonvertical_ybias[2]),
                   (center_pos[0] + nonvertical_xbias[3], center_pos[1] - nonvertical_ybias[3]),
                   (center_pos[0] + nonvertical_xbias[4], center_pos[1] - nonvertical_ybias[4]),
                   (center_pos[0] + nonvertical_xbias[5], center_pos[1] - nonvertical_ybias[5]),
                   (center_pos[0] + nonvertical_xbias[6], center_pos[1] - nonvertical_ybias[6]),
                   (center_pos[0] + nonvertical_xbias[7], center_pos[1] - nonvertical_ybias[7]),
                   (center_pos[0] + nonvertical_xbias[8], center_pos[1] - nonvertical_ybias[8]),
                   (center_pos[0] + nonvertical_xbias[9], center_pos[1] - nonvertical_ybias[9])]
        dex_idx = [center_pos,
                   (center_pos[0] - nonvertical_xbias[1], center_pos[1] + nonvertical_ybias[1]),
                   (center_pos[0] - nonvertical_xbias[2], center_pos[1] + nonvertical_ybias[2]),
                   (center_pos[0] - nonvertical_xbias[3], center_pos[1] + nonvertical_ybias[3]),
                   (center_pos[0] - nonvertical_xbias[4], center_pos[1] + nonvertical_ybias[4]),
                   (center_pos[0] - nonvertical_xbias[5], center_pos[1] + nonvertical_ybias[5]),
                   (center_pos[0] - nonvertical_xbias[6], center_pos[1] + nonvertical_ybias[6]),
                   (center_pos[0] - nonvertical_xbias[7], center_pos[1] + nonvertical_ybias[7]),
                   (center_pos[0] - nonvertical_xbias[8], center_pos[1] + nonvertical_ybias[8]),
                   (center_pos[0] - nonvertical_xbias[9], center_pos[1] + nonvertical_ybias[9])]
        luk_idx = [center_pos,
                   (center_pos[0] + nonvertical_xbias[1], center_pos[1] + nonvertical_ybias[1]),
                   (center_pos[0] + nonvertical_xbias[2], center_pos[1] + nonvertical_ybias[2]),
                   (center_pos[0] + nonvertical_xbias[3], center_pos[1] + nonvertical_ybias[3]),
                   (center_pos[0] + nonvertical_xbias[4], center_pos[1] + nonvertical_ybias[4]),
                   (center_pos[0] + nonvertical_xbias[5], center_pos[1] + nonvertical_ybias[5]),
                   (center_pos[0] + nonvertical_xbias[6], center_pos[1] + nonvertical_ybias[6]),
                   (center_pos[0] + nonvertical_xbias[7], center_pos[1] + nonvertical_ybias[7]),
                   (center_pos[0] + nonvertical_xbias[8], center_pos[1] + nonvertical_ybias[8]),
                   (center_pos[0] + nonvertical_xbias[9], center_pos[1] + nonvertical_ybias[9])]
        color = (123, 145, 203)
        pygame.draw.polygon(return_sur, color,
                            [str_idx[ability[0]], agi_idx[ability[1]], dex_idx[ability[2]], int_idx[ability[5]], luk_idx[ability[4]],
                             vit_idx[ability[3]]])
        return_sur.blit(self.font.render('請輸入角色名稱(英文)與設定初始素質', True, Black), (8, 25))
        # return_sur.blit(self.font.render('[S]tr, [A]gi, [V]it, [I]nt, [D]ex, [L]uk', True, Black), (8, 40))
        # return_sur.blit(self.font.render('Esc: 重置', True, Black), (8, 55))
        # return_sur.blit(self.font.render('Enter: 送出', True, Black), (8, 70))
        return_sur.blit(self.font.render(str(ability[0]), True, Black), (500, 40))
        return_sur.blit(self.font.render(str(ability[1]), True, Black), (500, 56))
        return_sur.blit(self.font.render(str(ability[3]), True, Black), (500, 72))
        return_sur.blit(self.font.render(str(ability[5]), True, Black), (500, 88))
        return_sur.blit(self.font.render(str(ability[2]), True, Black), (500, 104))
        return_sur.blit(self.font.render(str(ability[4]), True, Black), (500, 120))
        return_sur.blit(stand_char, rect)
        # return_sur.blit(self.font.render(name, True, Black), (65, 245))
        return return_sur

    def create_equip_ability_win(self, char_obj):       # 裝備+素質狀態的介面
        font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", 10)
        attribute = char_obj.attribute
        return_sur = self.equip_ability_template.copy()
        stand_char = char_obj.stand_img
        rect = stand_char.get_rect()
        rect.center = (143, 95)
        return_sur.blit(stand_char, rect)

        right_idx1, right_idx2 = 190, 272
        str_ = char_obj.ability.get_ability('str').value
        agi_ = char_obj.ability.get_ability('agi').value
        vit_ = char_obj.ability.get_ability('vit').value
        int_ = char_obj.ability.get_ability('int').value
        dex_ = char_obj.ability.get_ability('dex').value
        luk_ = char_obj.ability.get_ability('luk').value

        pos1 = 54
        pos2, p2_step = 188, 16
        # 目前基礎素質
        return_sur.blit(font.render(str(str_), True, Black), (pos1, pos2))
        return_sur.blit(font.render(str(agi_), True, Black), (pos1, pos2 + p2_step))
        return_sur.blit(font.render(str(vit_), True, Black), (pos1, pos2 + 2 * p2_step))
        return_sur.blit(font.render(str(int_), True, Black), (pos1, pos2 + 3 * p2_step))
        return_sur.blit(font.render(str(dex_), True, Black), (pos1, pos2 + 4 * p2_step))
        return_sur.blit(font.render(str(luk_), True, Black), (pos1, pos2 + 5 * p2_step))
        ability_step, plus_step = 12, 7
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2))
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2 + p2_step))
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2 + 2 * p2_step))
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2 + 3 * p2_step))
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2 + 4 * p2_step))
        return_sur.blit(font.render("+", True, Black), (pos1 + ability_step, pos2 + 5 * p2_step))
        # 裝備素質 or job加成
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2))
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2 + p2_step))
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2 + 2 * p2_step))
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2 + 3 * p2_step))
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2 + 4 * p2_step))
        return_sur.blit(font.render("0", True, Black), (pos1 + ability_step + plus_step, pos2 + 5 * p2_step))
        # 升級素質所需升級點
        pos1_up = pos1 + 48
        return_sur.blit(font.render(str(char_obj.ability.get_ability("str").upgrade_demand), True, Black), (pos1_up, pos2))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("agi").upgrade_demand), True, Black), (pos1_up, pos2 + p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("vit").upgrade_demand), True, Black), (pos1_up, pos2 + 2 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("int").upgrade_demand), True, Black), (pos1_up, pos2 + 3 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("dex").upgrade_demand), True, Black), (pos1_up, pos2 + 4 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("luk").upgrade_demand), True, Black), (pos1_up, pos2 + 5 * p2_step))

        sur, rect = self.render_and_return_rect(font, str(attribute.total_atk[0]) + " - " + str(attribute.total_atk[1]), Black)
        rect.top, rect.right = 188, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.total_matk[0]) + " - " + str(attribute.total_matk[1]), Black)
        rect.top, rect.right = 204, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.hit), Black)
        rect.top, rect.right = 220, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.cri), Black)
        rect.top, rect.right = 236, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.total_defence), Black)
        rect.top, rect.right = 188, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.total_mdefence), Black)
        rect.top, rect.right = 204, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.flee), Black)
        rect.top, rect.right = 220, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.aspd), Black)
        rect.top, rect.right = 236, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(char_obj.ability.status_point), Black)
        rect.top, rect.right = 252, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, "~ * 仙境情懷 * ~", Black)
        rect.top, rect.right = 268, right_idx2
        return_sur.blit(sur, rect)
        #      裝備欄                                               素質欄
        return return_sur.subsurface(pygame.Rect(0, 0, 280, 166)), return_sur.subsurface(pygame.Rect(0, 167, 280, 120))

    def generate_txt_win(self, width_px, height_px):  # 創造客製化尺寸的系統視窗文字區域，原則上輸入的最小尺寸應胎是60 x 60
        txt_width = 20      # 分割模板的尺寸
        txt_height = 20

        width_count = width_px // txt_width  # 可能沒辦法完全整除時，向下取整數
        height_count = height_px // txt_height
        win = pygame.Surface((width_count * txt_width, height_count * txt_height)).convert_alpha()  # title bar的高度另外算

        height_type = None
        width_type = None
        for i in range(height_count):
            if i == 0:
                height_type = 1
            elif i == height_count - 1:
                height_type = 3
            else:
                height_type = 2
            for j in range(width_count):
                if j == 0:
                    width_type = 0
                elif j == width_count - 1:
                    width_type = 2
                else:
                    width_type = 1
                win.blit(self.txt_win_template[height_type][width_type], (j * txt_width, i * txt_height))
        return win

    def generate_titlebar(self, width_px):          # 創造客製化尺寸的系統視窗的上方Bar與下方Button Bar
        titlebar_width = 20
        titlebar_height = 17
        btnbar_width = 20
        btnbar_height = 28

        width_count = width_px // titlebar_width  # 可能沒辦法完全整除時，向下取整數
        title_bar = pygame.Surface((width_count * titlebar_width, titlebar_height)).convert_alpha()
        btn_bar = pygame.Surface((width_count * btnbar_width, btnbar_height)).convert_alpha()

        for i in range(width_count):
            if i == 0:
                title_bar.blit(self.txt_win_template[0][0], (0, 0))
                btn_bar.blit(self.txt_win_template[4][0], (0, 0))
            elif i == width_count - 1:
                title_bar.blit(self.txt_win_template[0][2], (i * titlebar_width, 0))
                btn_bar.blit(self.txt_win_template[4][2], (i * btnbar_width, 0))
            else:
                title_bar.blit(self.txt_win_template[0][1], (i * titlebar_width, 0))
                btn_bar.blit(self.txt_win_template[4][1], (i * btnbar_width, 0))

        return title_bar, btn_bar

    @staticmethod
    def set_status_text(surface, char_obj):
        temp_font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", 11)
        name_render = temp_font.render(char_obj.char_name, True, Black)
        exp_percentrage = round(char_obj.base_exp / char_obj.target_base_exp * 100, 1)
        # status1 = "Lv.100 / Assassin Cross / Lv.70 / Exp.100.0 %"     # 極限測試
        # status2 = "HP 99999/99999 | SP 9999/9999 | 10000000Z"
        status1 = "Lv." + str(char_obj.base_level) + " / " + char_obj.job_name + " / Lv." + str(char_obj.job_level) + " / Exp. " + str(exp_percentrage) + " %"
        status2 = "HP " + str(char_obj.hp) + " / " + str(char_obj.attribute.max_hp) + "| SP " + str(char_obj.sp) + " / " + str(char_obj.attribute.max_sp) + " | " + str(Character.tool_money_format(char_obj.zeny)) + " Z"
        surface.blit(name_render, (19, 0))
        status1_render = temp_font.render(status1, True, Black)
        surface.blit(status1_render, (6, 17))
        status2_render = temp_font.render(status2, True, Black)
        surface.blit(status2_render, (6, 33))
        return surface

    @staticmethod
    def fps_analysis(fps_list):
        if len(fps_list) > 30:
            del fps_list[0:29]
        print("FPS: ", str(min(fps_list)), " - ", str(max(fps_list)))

    @staticmethod
    def combine_sprite(*input_group):
        all_group = pygame.sprite.Group()
        for group in input_group:
            for sprite in group:
                all_group.add(sprite)
        return all_group

    @staticmethod
    def render_and_return_rect(font, text, color):
        sur = font.render(text, True, color)
        return sur, sur.get_rect()

    @staticmethod
    def get_health_bar(char_obj):               # 創造HP/SP Bar
        hp_ratio = math.floor(char_obj.hp / char_obj.attribute.max_hp * 100 / 2)  # 0 - 100 整數
        sp_ratio = math.floor(char_obj.sp / char_obj.attribute.max_sp * 100 / 2)
        hp_color = (13, 242, 39)
        sp_color = (9, 90, 219)
        empty_color = (61, 69, 70)
        border_color = (32, 28, 103)
        width, height = 50, 8
        bar_surface = pygame.Surface((width, height)).convert()
        bar_surface.fill(empty_color)

        if hp_ratio > 0:
            hp_bar = pygame.Surface((hp_ratio, height / 2)).convert()
            hp_bar.fill(hp_color)
            bar_surface.blit(hp_bar, (0, 0))
        if sp_ratio > 0:
            sp_bar = pygame.Surface((sp_ratio, height / 2)).convert()
            sp_bar.fill(sp_color)
            bar_surface.blit(sp_bar, (0, height / 2))

        pygame.draw.rect(bar_surface, border_color, (0, 0, width, height), 1)
        return bar_surface

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
    def play_bgm(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops = -1)

    @staticmethod
    def input_detect():
        key = []
        key_id = []
        mouse = []
        mouse_type = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    key.append("escape")
                elif event.key == pygame.K_RETURN:
                    key.append("return")
                elif event.key == pygame.K_BACKSPACE:
                    key.append("backspace")
                elif event.key == pygame.K_UP:
                    key.append("up")
                elif event.key == pygame.K_DOWN:
                    key.append("down")
                elif event.key == pygame.K_LEFT:
                    key.append("left")
                elif event.key == pygame.K_RIGHT:
                    key.append("right")
                else:
                    key.append(event.unicode)
                key_id.append(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.append(event.button)
                mouse_type.append("down")
            elif event.type == pygame.MOUSEBUTTONUP:
                if len(mouse) > 0 and event.button == mouse[-1] and mouse_type[-1] == "down":  # 假設同一個frame同時有down與up，還同一個鍵，應該定義為click
                    mouse_type[-1] = "click"
                else:
                    mouse.append(event.button)
                    mouse_type.append("up")

        if len(mouse) == 0:
            button_list = pygame.mouse.get_pressed()
            if button_list[0]:
                mouse.append(1)
            elif button_list[1]:
                mouse.append(2)
            elif button_list[2]:
                mouse.append(3)
            if sum(button_list) != 0:
                mouse_type.append("down")

        return key, key_id, mouse, mouse_type

    @staticmethod
    def effect_sound(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.2)
        sound.play()
