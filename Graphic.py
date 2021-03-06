import os, math                                     # Built-in Library
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library
import Character, Animate_Utility

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Font_size = 12


class WindowClass:
    obj = None

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
        self.item_detail_template = pygame.image.load(os.path.join("Info_Image", "collection_bg.png")).convert_alpha()
        self.txt_win_template = []       # 文字區域板塊（九宮格模板，可自訂大小）
        self.btn_ok_template = []        # 確認按鈕
        self.btn_cancel_template = []    # 取消按鈕
        self.btn_inter_template = []     # 主界面的功能按鈕，且會放大
        self.btn_r_arw_template = []     # 素質加點向右箭頭
        self.btn_use_template = []       # 物品使用按鈕
        self.btn_auto_use_template = []  # 補品自動使用開啟按鈕
        self.btn_unload_template = []    # 卸下裝備按鈕
        self.item_tab_template = []      # 物品欄左方分類標籤
        self.item_base_template = []     # 物品欄格子模板
        self.damage_template = []        # 普通攻擊數值
        self.damage_cri_template = []    # 爆擊傷害數值
        self.health_hp_template = []     # 補血數字
        self.health_sp_template = []     # 補魔數字
        self.pointer_template = []       # 滑鼠動畫
        self.load_template_image()
        self.char_pos = (self.width * 0.4, self.height * 0.55)  # center pos
        self.mons_pos = (self.width * 0.6, self.height * 0.55)
        self.char_name_pos = (self.char_pos[0], self.char_pos[1] - 70)
        self.mons_name_pos = (self.mons_pos[0], self.mons_pos[1] - 70)
        self.char_damage_pos = (self.mons_pos[0], self.mons_pos[1] - 110)
        self.mons_damage_pos = (self.char_pos[0], self.char_pos[1] - 110)
        WindowClass.obj = self

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

    def set_bg_by_surface(self, surface, alpha):
        self.clear_screen()
        pygame.transform.scale(surface, self.screen.get_size(), self.background)
        self.background.set_alpha(alpha)
        self.screen.blit(self.background, (0, 0))

    def set_text(self, surface, text, color, str_offset, end_offset = None):       # 在輸入的Surface上畫上文字，並且如果文字太長會自動換行
        # It seems that surface needs always be converted
        # offset = (width_offset, height_offset)
        # color = (R, G, B)
        max_w, max_h = surface.get_size()
        cur_w, cur_h = str_offset
        end_w, end_h = (end_offset[0], end_offset[1]) if end_offset is not None else (0, 0)
        color_idx = 0
        for line in text:
            word_h2 = 0
            for word in line:
                word_surface = self.font.render(word, True, color[color_idx])
                word_w, word_h = word_surface.get_size()
                word_h += 3                                 # increase the space between lines
                word_h2 = word_h
                if max_w - (cur_w + word_w) < end_w:
                    cur_w = str_offset[0]
                    cur_h += word_h
                surface.blit(word_surface, (cur_w, cur_h))
                cur_w += word_w
            cur_w = str_offset[0]
            cur_h += word_h2
            color_idx += 1

    def get_chat_win(self, content, color, only_input_chat_content = False):      # 創造聊天室
        # content = ["str1", "str2", ...]
        # can store 15 lines content
        size = (600, 221)
        line_limit = 12
        if content is not None:
            self.chat_message = self.chat_message + content  # concatenate 2 list, keep 15 elements in list
            self.chat_color = self.chat_color + color
        while not len(self.chat_message) < line_limit:
            self.chat_message.pop(0)                           # 刪除最舊的訊息
            self.chat_color.pop(0)
        if not only_input_chat_content:
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
        self.txt_win_template = [
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
        self.btn_use_template = [pygame.image.load(os.path.join("Info_Image", "btn_use.png")).convert_alpha(),
                                 pygame.image.load(os.path.join("Info_Image", "btn_use_a.png")).convert_alpha(),
                                 pygame.image.load(os.path.join("Info_Image", "btn_use_b.png")).convert_alpha()]
        self.btn_auto_use_template = [pygame.image.load(os.path.join("Info_Image", "btn_auto_use.png")).convert_alpha(),
                                      pygame.image.load(os.path.join("Info_Image", "btn_auto_use_a.png")).convert_alpha(),
                                      pygame.image.load(os.path.join("Info_Image", "btn_auto_use_b.png")).convert_alpha()]
        self.btn_unload_template = [pygame.image.load(os.path.join("Info_Image", "btn_unload.png")).convert_alpha(),
                                    pygame.image.load(os.path.join("Info_Image", "btn_unload_a.png")).convert_alpha(),
                                    pygame.image.load(os.path.join("Info_Image", "btn_unload_b.png")).convert_alpha()]
        self.item_tab_template = [pygame.image.load(os.path.join("Info_Image", "tab_itm_01.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("Info_Image", "tab_itm_02.png")).convert_alpha(),
                                  pygame.image.load(os.path.join("Info_Image", "tab_itm_03.png")).convert_alpha()]
        self.item_base_template = [pygame.image.load(os.path.join("Info_Image", "itemwin_left.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("Info_Image", "itemwin_mid.png")).convert_alpha(),
                                   pygame.image.load(os.path.join("Info_Image", "itemwin_right.png")).convert_alpha()]
        # 把每個Button送進去resize，然後長寬各乘2倍
        self.btn_inter_template = \
            [[self.get_resize_surface(j, [k*2 for k in j.get_size()]) for j in i] for i in self.btn_inter_template]
        damage_img = pygame.image.load(os.path.join("Info_Image", "damage.png")).convert_alpha()
        damage_img = self.get_resize_surface(damage_img, (int(damage_img.get_size()[0] * 1.5), int(damage_img.get_size()[1] * 1.5)))
        damage_cri_img = pygame.image.load(os.path.join("Info_Image", "damage_Critical.png")).convert_alpha()
        damage_cri_img = self.get_resize_surface(damage_cri_img, (int(damage_cri_img.get_size()[0] * 1.5), int(damage_cri_img.get_size()[1] * 1.5)))
        health_hp_img = pygame.image.load(os.path.join("Info_Image", "HealthHP.png")).convert_alpha()
        health_hp_img = self.get_resize_surface(health_hp_img, (int(health_hp_img.get_size()[0] * 1.5), int(health_hp_img.get_size()[1] * 1.5)))
        health_sp_img = pygame.image.load(os.path.join("Info_Image", "HealthSP.png")).convert_alpha()
        health_sp_img = self.get_resize_surface(health_sp_img, (int(health_sp_img.get_size()[0] * 1.5), int(health_sp_img.get_size()[1] * 1.5)))
        pointer_img = pygame.image.load(os.path.join("Info_Image", "pointer.png")).convert_alpha()
        damage_width = damage_img.get_size()[0] / 10
        damage_height = damage_img.get_size()[1]
        ptr_width = 22
        ptr_height = 31
        for i in range(1, damage_img.get_size()[0] // int(damage_width) + 1):
            self.damage_template.append(damage_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
            self.damage_cri_template.append(damage_cri_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
            self.health_hp_template.append(health_hp_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
            self.health_sp_template.append(health_sp_img.subsurface(pygame.Rect((i-1) * damage_width, 0, damage_width, damage_height)))
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
        return_sur.blit(self.font.render(str(ability[0]), True, Black), (500, 40))
        return_sur.blit(self.font.render(str(ability[1]), True, Black), (500, 56))
        return_sur.blit(self.font.render(str(ability[3]), True, Black), (500, 72))
        return_sur.blit(self.font.render(str(ability[5]), True, Black), (500, 88))
        return_sur.blit(self.font.render(str(ability[2]), True, Black), (500, 104))
        return_sur.blit(self.font.render(str(ability[4]), True, Black), (500, 120))
        return_sur.blit(stand_char, rect)
        return return_sur

    def create_equip_ability_win(self, char_obj, group):       # 裝備+素質狀態的介面
        font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", 10)
        attribute = char_obj.attribute
        return_sur = self.equip_ability_template.copy()
        stand_char = char_obj.stand_img
        rect = stand_char.get_rect()
        rect.center = (143, 95)
        return_sur.blit(stand_char, rect)
        equip_win_size = (280, 166)
        status_win_size = (280, 120)

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
        return_sur.blit(font.render(str(char_obj.attribute.equip_str), True, Black), (pos1 + ability_step + plus_step, pos2))
        return_sur.blit(font.render(str(char_obj.attribute.equip_agi), True, Black), (pos1 + ability_step + plus_step, pos2 + p2_step))
        return_sur.blit(font.render(str(char_obj.attribute.equip_vit), True, Black), (pos1 + ability_step + plus_step, pos2 + 2 * p2_step))
        return_sur.blit(font.render(str(char_obj.attribute.equip_int), True, Black), (pos1 + ability_step + plus_step, pos2 + 3 * p2_step))
        return_sur.blit(font.render(str(char_obj.attribute.equip_dex), True, Black), (pos1 + ability_step + plus_step, pos2 + 4 * p2_step))
        return_sur.blit(font.render(str(char_obj.attribute.equip_luk), True, Black), (pos1 + ability_step + plus_step, pos2 + 5 * p2_step))
        # 升級素質所需升級點
        pos1_up = pos1 + 48
        return_sur.blit(font.render(str(char_obj.ability.get_ability("str").upgrade_demand), True, Black), (pos1_up, pos2))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("agi").upgrade_demand), True, Black), (pos1_up, pos2 + p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("vit").upgrade_demand), True, Black), (pos1_up, pos2 + 2 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("int").upgrade_demand), True, Black), (pos1_up, pos2 + 3 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("dex").upgrade_demand), True, Black), (pos1_up, pos2 + 4 * p2_step))
        return_sur.blit(font.render(str(char_obj.ability.get_ability("luk").upgrade_demand), True, Black), (pos1_up, pos2 + 5 * p2_step))
        # 右方詳細數值
        sur, rect = self.render_and_return_rect(font, str(attribute.char_atk) + " + " + str(attribute.equip_atk), Black)
        rect.top, rect.right = 188, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.char_matk) + " + " + str(attribute.equip_matk), Black)
        rect.top, rect.right = 204, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.hit), Black)
        rect.top, rect.right = 220, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.cri), Black)
        rect.top, rect.right = 236, right_idx1
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.char_def) + " + " + str(attribute.equip_def), Black)
        rect.top, rect.right = 188, right_idx2
        return_sur.blit(sur, rect)
        sur, rect = self.render_and_return_rect(font, str(attribute.char_mdef) + " + " + str(attribute.equip_mdef), Black)
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
        # 裝備
        left_ini_pos, right_ini_pos, step = (17, 30), (262, 30), 26
        pos_list = (left_ini_pos, right_ini_pos,
                    (left_ini_pos[0], left_ini_pos[1] + step),
                    (right_ini_pos[0], right_ini_pos[1] + step),
                    (left_ini_pos[0], left_ini_pos[1] + 2 * step),
                    (right_ini_pos[0], right_ini_pos[1] + 2 * step),
                    (left_ini_pos[0], left_ini_pos[1] + 3 * step),
                    (right_ini_pos[0], right_ini_pos[1] + 3 * step),
                    (left_ini_pos[0], left_ini_pos[1] + 4 * step),
                    (right_ini_pos[0], right_ini_pos[1] + 4 * step))
        group.empty()
        topleft = pygame.Rect(0, 0, equip_win_size[0], equip_win_size[1])
        topleft.center = (self.width * 0.15, self.height * 0.55)
        transparent_list = [self.create_transparent_surface(step, step)] * 3
        for idx, equip in enumerate(char_obj.equipment.equip_list):
            if equip is not None:
                rect = equip.icon_image.get_rect()
                rect.center = pos_list[idx]
                return_sur.blit(equip.icon_image, rect)
                group.add(Animate_Utility.SlideItemButtonAnimate(transparent_list, (topleft.topleft[0] + rect.centerx, topleft.topleft[1] + rect.centery), [0, self.height, 0, self.width], 1, equip.item_type, equip.item_idx, idx))
                name = self.font.render(equip.item_name, True, Black)
                rect = name.get_rect()
                if idx % 2 == 0:
                    rect.left, rect.centery = pos_list[idx][0] + 20, pos_list[idx][1]
                else:
                    rect.right, rect.centery = pos_list[idx][0] - 20, pos_list[idx][1]
                return_sur.blit(name, rect)
        #      裝備欄                                                                            素質欄                                                                                                裝備按鈕
        return return_sur.subsurface(pygame.Rect(0, 0, equip_win_size[0], equip_win_size[1])), return_sur.subsurface(pygame.Rect(0, equip_win_size[1] + 1, status_win_size[0], status_win_size[1])), group

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

    def get_item_base_win(self, item_type):
        width, height = 260, 173
        win = pygame.Surface((width, height)).convert_alpha()

        title_bar, btn_bar = self.generate_titlebar(width)
        win.blit(title_bar, (0, 0))
        win.blit(self.item_tab_template[item_type], (0, 17))
        win.blit(btn_bar, (0, 145))

        return win

    def get_item_detail_win(self, item_obj):
        win = self.item_detail_template.copy()
        win.blit(item_obj.image, (10, 11))
        win.blit(self.font.render(item_obj.item_name, True, Black), (95, 9))
        self.set_text(win, item_obj.descrip, item_obj.descrip_color, (95, 30), (10, 10))
        return win

    def get_item_list_win(self, item_list, border_list, btn_group):
        # border_list = [border_up, border_down, border_left, border_right]
        item_num = len(item_list)
        item_in_row = 7
        edge_width, block_width, height = 40, 32, 32
        row_num = int(math.ceil(item_num / item_in_row))
        row_num = 4 if row_num < 4 else row_num
        win_width = (item_in_row - 2) * block_width + 2 * edge_width
        win_height = row_num * height

        win = pygame.Surface((win_width, win_height)).convert_alpha()
        cur_width, cur_height = 0, 0
        for r in range(row_num):            # 先畫出物品欄的底圖
            win.blit(self.item_base_template[0], (cur_width, cur_height))
            cur_width += edge_width
            for i in range(5):
                win.blit(self.item_base_template[1], (cur_width, cur_height))
                cur_width += block_width
            win.blit(self.item_base_template[2], (cur_width, cur_height))
            cur_width = 0
            cur_height += height

        count = 1
        cur_width, cur_height = 24, 14
        width_space, height_space = 32, 32
        amount_bias = 10
        btn_list = [self.create_transparent_surface(width_space, height_space)] * 3
        font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", 10)
        btn_group.empty()
        for idx, item in enumerate(item_list):              # 按照順序將物品icon畫上並標註數量
            rect = item.icon_image.get_rect()
            rect.center = (cur_width, cur_height)
            win.blit(item.icon_image, rect)
            btn_group.add(Animate_Utility.SlideItemButtonAnimate(btn_list, (border_list[2] + cur_width, border_list[0] + cur_height + 2), border_list, 2, item.item_type, item.item_idx, idx))
            amount = font.render(str(item.amount), True, Black)
            rect = amount.get_rect()
            rect.center = (cur_width + amount_bias, cur_height + amount_bias)
            win.blit(amount, rect)
            cur_width += width_space
            if count == 7:
                count = 1
                cur_width = 24
                cur_height += height_space
            else:
                count += 1
        return win, btn_group

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
    def get_map_icon(file_path):  # 產生小地圖(半透明)
        img = pygame.image.load(file_path).convert_alpha()
        rect = img.get_rect()
        img2 = pygame.Surface((rect.width // 2, rect.height // 2)).convert()
        img2.set_alpha(200)
        pygame.transform.scale(img, (rect.width // 2, rect.height // 2), img2)
        return img2

    @staticmethod
    def get_resize_surface(img1, target_size):
        img2 = pygame.Surface(target_size).convert_alpha()
        pygame.transform.scale(img1, target_size, img2)
        return img2

    @staticmethod
    def set_status_text(surface, char_obj):
        temp_font = pygame.font.Font("GenJyuuGothic-Monospace-Bold.ttf", 11)
        name_render = temp_font.render(char_obj.char_name, True, Black)
        exp_percentrage = round(char_obj.base_exp / char_obj.target_base_exp * 100, 1)
        # status1 = "Lv.100 / Assassin Cross / Lv.70 / Exp.100.0 %"     # 極限測試
        # status2 = "HP 99999/99999 | SP 9999/9999 | 10000000Z"
        status1 = "Lv." + str(char_obj.base_level) + " / " + char_obj.job_name + " / Lv." + str(
            char_obj.job_level) + " / Exp. " + str(exp_percentrage) + " %"
        status2 = "HP " + str(char_obj.hp) + " / " + str(char_obj.attribute.max_hp) + "| SP " + str(
            char_obj.sp) + " / " + str(char_obj.attribute.max_sp) + " | " + str(
            Character.tool_money_format(char_obj.zeny)) + " Z"
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
        print("FPS: ", str(round(min(fps_list), 2)), " - ", str(round(max(fps_list), 2)))

    @staticmethod
    def render_and_return_rect(font, text, color):
        sur = font.render(text, True, color)
        return sur, sur.get_rect()

    @staticmethod
    def get_health_bar(char_obj):  # 創造HP/SP Bar
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
        surface.fill((5, 5, 5))
        surface.set_colorkey((5, 5, 5))
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
        pygame.mixer.music.play(loops=-1)

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
