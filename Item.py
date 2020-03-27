import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library
import Item_Database


class ItemList:
    def __init__(self):
        self.usable_item_list = []
        self.usable_idx = []
        self.equipment_list = []
        self.equip_idx = []
        self.collection_list = []
        self.collect_idx = []

        self.all_list = [self.usable_item_list, self.equipment_list, self.collection_list]
        self.all_idx_list = [self.usable_idx, self.equip_idx, self.collect_idx]

    def add_item(self, item_obj):
        container, idx_container = self.all_list[item_obj.item_type], self.all_idx_list[item_obj.item_type]
        if item_obj.item_idx in idx_container and item_obj.item_type != 1:      # 已存在的物品增加數量(除了裝備不能疊放)
            container[idx_container.index(item_obj.item_idx)].amount += item_obj.amount
        else:
            container.append(item_obj)              # 未存在的物品新增進List
            idx_container.append(item_obj.item_idx)

    def get_item(self, item_type, item_idx):
        return self.all_list[item_type][self.all_idx_list[item_type].index(item_idx)]

    # def double_click(self, item_type, item_idx):        # 當數量為0時需要從表單中刪除
    #     obj = self.all_list[item_type][self.all_idx_list[item_type].index(item_idx)]
    #     if item_type == 0:
    #         obj.usable_double_click()
    #     return


class EquipmentList:
    def __init__(self):
        self.equip_list = [None, None, None, None, None, None, None, None, None, None]
        # 頭上, 頭中, 頭下, 鎧甲, 左邊手的格子(右手), 右邊手的格子(左手), 披風, 鞋子, 左飾品, 右飾品
        self.equip_atk, self.equip_def, self.equip_hp, self.equip_sp = 0, 0, 0, 0
        self.equip_str, self.equip_agi, self.equip_vit, self.equip_int, self.equip_dex, self.equip_luk = 0, 0, 0, 0, 0, 0

    def equip(self, item_obj, item_list):
        if self.check_equip_limit(item_obj):  # 檢查是否符合裝備限定的職業與等級
            current = self.equip_list[item_obj.equip_pos]
            self.equip_list[item_obj.equip_pos] = item_obj     # 根據位置裝上裝備
            if current is not None:
                item_list.add_item(current)     # 假如原本該位置有裝備，放入物品欄
            self.calculate_bonus()              # 重新統整裝備給予的加成

    def calculate_bonus(self):
        for obj in self.equip_list:
            self.equip_atk = self.equip_atk + obj.attack if obj is not None else self.equip_atk
            self.equip_def = self.equip_def + obj.defence if obj is not None else self.equip_def
            self.equip_hp = self.equip_hp + obj.hp if obj is not None else self.equip_hp
            self.equip_sp = self.equip_sp + obj.sp if obj is not None else self.equip_sp
            self.equip_str = self.equip_str + obj.str if obj is not None else self.equip_str
            self.equip_agi = self.equip_agi + obj.agi if obj is not None else self.equip_agi
            self.equip_vit = self.equip_vit + obj.vit if obj is not None else self.equip_vit
            self.equip_int = self.equip_int + obj.int if obj is not None else self.equip_int
            self.equip_dex = self.equip_dex + obj.dex if obj is not None else self.equip_dex
            self.equip_luk = self.equip_luk + obj.luk if obj is not None else self.equip_luk

    @staticmethod
    def check_equip_limit(item_obj):
        if item_obj.char.job_idx in item_obj.item_data[12]:
            if item_obj.char.base_level >= item_obj.equip_min_level:
                return True
            else:
                return False
        else:
            return False


class ItemObj:
    def __init__(self, item_type, item_idx, char, amount):
        self.item_type = item_type        # type 0 = usable item, type 1 = equipment, type 2 = collection
        self.char = char
        self.item_idx = item_idx
        self.item_data = Item_Database.item_list[item_type][item_idx]
        self.item_name = None
        self.health_hp, self.health_sp = None, None
        self.attack, self.defence, self.hp, self.sp = None, None, None, None
        self.str, self.agi, self.vit, self.int, self.dex, self.luk = None, None, None, None, None, None
        self.equip_target, self.equip_pos, self.equip_min_level = None, None, None
        self.price = None
        self.icon_image = None
        self.image = None
        self.descrip = None
        self.descrip_color = None
        self.amount = amount
        self.double_click_act = None
        self.data_setting()

    # def usable_double_click(self):
    #     self.char.hp = self.char.hp + self.health_hp if self.health_hp is not None else self.char.hp
    #     self.char.hp = self.char.attribute.max_hp if self.char.hp >= self.char.attribute.max_hp else self.char.hp
    #     self.char.sp = self.char.sp + self.health_sp if self.health_sp is not None else self.char.sp
    #     self.char.sp = self.char.attribute.max_sp if self.char.sp >= self.char.attribute.max_sp else self.char.sp
    #     self.amount -= 1
    #
    # def equip_double_click(self):
    #     return

    def data_setting(self):
        self.item_name = self.item_data[1]
        if self.item_type == 0:
            self.health_hp = self.item_data[2]
            self.health_sp = self.item_data[3]
            self.price = self.item_data[4]
            self.icon_image = pygame.image.load(self.item_data[5]).convert_alpha()
            self.image = pygame.image.load(self.item_data[6]).convert_alpha()
            self.descrip = self.item_data[7]
            self.descrip_color = self.item_data[8]
            # self.double_click_act = self.usable_double_click
        elif self.item_type == 1:
            self.attack = self.item_data[2]
            self.defence = self.item_data[3]
            self.hp = self.item_data[4]
            self.sp = self.item_data[5]
            self.str = self.item_data[6]
            self.agi = self.item_data[7]
            self.vit = self.item_data[8]
            self.int = self.item_data[9]
            self.dex = self.item_data[10]
            self.luk = self.item_data[11]
            self.equip_target = self.item_data[12]
            self.equip_pos = self.item_data[13]
            self.equip_min_level = self.item_data[14]
            self.price = self.item_data[15]
            self.icon_image = pygame.image.load(self.item_data[16]).convert_alpha()
            self.image = pygame.image.load(self.item_data[17]).convert_alpha()
            self.descrip = self.item_data[18]
            self.descrip_color = self.item_data[19]
            # self.double_click_act = self.equip_double_click
        elif self.item_type == 2:
            self.price = self.item_data[2]
            self.icon_image = pygame.image.load(self.item_data[3])
            self.image = pygame.image.load(self.item_data[4])
            self.descrip = self.item_data[5]
            self.descrip_color = self.item_data[6]




