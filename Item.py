import os, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library
import Item_Database, Animate_Utility, Graphic, World

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 222, 0)
Orange = (255, 170, 0)
Battle_Meg_Color = (0, 196, 255)
Purple = (200, 95, 200)


class ItemList:
    def __init__(self, equip_obj):
        self.usable_item_list = []
        self.usable_idx = []
        self.equipment_list = []
        self.equip_idx = []
        self.collection_list = []
        self.collect_idx = []
        self.equip_obj = equip_obj

        self.all_list = [self.usable_item_list, self.equipment_list, self.collection_list]
        self.all_idx_list = [self.usable_idx, self.equip_idx, self.collect_idx]

    def add_item(self, item_obj):
        container, idx_container = self.all_list[item_obj.item_type], self.all_idx_list[item_obj.item_type]
        if item_obj.item_idx in idx_container and item_obj.item_type != 1:      # 已存在的物品增加數量(除了裝備不能疊放)
            container[idx_container.index(item_obj.item_idx)].amount += item_obj.amount
        else:
            container.append(item_obj)              # 未存在的物品新增進List
            idx_container.append(item_obj.item_idx)

    def get_item(self, item_type, order):
        return self.all_list[item_type][order]

    def use_item(self, item_type, order):
        obj = self.all_list[item_type][order]
        response = obj.use_action(self.equip_obj)
        if response is not False and obj.item_type == 1:    # 代表不是裝備失敗，如果沒有限定item_type = 1，補品用一次就會消失
            self.all_list[item_type].remove(obj)            # 裝備成功先將該裝備移出物品欄
            if isinstance(response, ItemObj):               # 代表原先位置有裝備，被return回來
                self.add_item(response)                     # 加入裝備欄
            return 0                                        # 裝備的amount不會-1，因為只是跑過去裝備欄，但是這邊要return 0才會從物品欄消除
        if obj.amount <= 0 and obj.item_type == 0:
            self.all_list[item_type].remove(obj)
            return 0
        else:
            return obj.amount


class EquipmentList:
    def __init__(self):
        self.equip_list = [None, None, None, None, None, None, None, None, None, None]
        # 頭上, 頭中, 頭下, 鎧甲, 左邊手的格子(右手), 右邊手的格子(左手), 披風, 鞋子, 左飾品, 右飾品 (飾品的位置編號為8，但是8跟9都可以安裝)
        self.equip_atk, self.equip_def, self.equip_matk, self.equip_mdef, self.equip_hp, self.equip_sp = 0, 0, 0, 0, 0, 0
        self.equip_str, self.equip_agi, self.equip_vit, self.equip_int, self.equip_dex, self.equip_luk = 0, 0, 0, 0, 0, 0
        self.equip_idx = []

    def get_idx(self):
        idx = []
        for equip in self.equip_list:
            if equip is None:
                idx.append(equip)
            else:
                idx.append(equip.item_idx)
        return idx

    def equip(self, item_obj):
        if self.check_equip_limit(item_obj):                    # 檢查是否符合裝備限定的職業與等級
            print(item_obj.equip_pos)
            pos = item_obj.equip_pos
            if pos == 8:                                        # 代表是飾品 (左飾品為空，直接裝，這邊無動作)
                if self.equip_list[pos] is not None and self.equip_list[pos + 1] is None:   # 左裝飾品有東西，右裝飾品沒有，就改安裝到9號位，其他都是裝到8號位
                    pos = pos + 1
            current_equip = self.equip_list[pos]
            self.equip_list[pos] = item_obj                     # 根據位置裝上裝備
            self.calculate_bonus()                              # 重新統整裝備給予的加成
            return current_equip                                # return None or Obj
        else:
            return False                                        # return False

    def unload(self, pos):
        if self.equip_list[pos] is not None:
            current_equip = self.equip_list[pos]
            self.equip_list[pos] = None
            self.calculate_bonus()
            return current_equip
        else:
            return None

    def reset_equip(self):
        self.equip_list = [None, None, None, None, None, None, None, None, None, None]

    def reset_equip_bonus(self):
        self.equip_atk, self.equip_def, self.equip_matk, self.equip_mdef, self.equip_hp, self.equip_sp = 0, 0, 0, 0, 0, 0
        self.equip_str, self.equip_agi, self.equip_vit, self.equip_int, self.equip_dex, self.equip_luk = 0, 0, 0, 0, 0, 0
        self.equip_idx = []

    def calculate_bonus(self):
        self.reset_equip_bonus()
        for idx, obj in enumerate(self.equip_list):
            if obj is not None:
                self.equip_atk = self.equip_atk + obj.attack
                self.equip_def = self.equip_def + obj.defence
                self.equip_matk = self.equip_matk + obj.mattack
                self.equip_mdef = self.equip_mdef + obj.mdefence
                self.equip_hp = self.equip_hp + obj.hp
                self.equip_sp = self.equip_sp + obj.sp
                self.equip_str = self.equip_str + obj.str
                self.equip_agi = self.equip_agi + obj.agi
                self.equip_vit = self.equip_vit + obj.vit
                self.equip_int = self.equip_int + obj.int
                self.equip_dex = self.equip_dex + obj.dex
                self.equip_luk = self.equip_luk + obj.luk
                self.equip_idx.append(idx)

    @staticmethod
    def check_equip_limit(item_obj):
        if item_obj.char.job_idx in item_obj.equip_target:
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
        self.item_data = Item_Database.item_list[item_type][item_idx] if item_type != 1 else Item_Database.item_list[item_type][item_idx[0]][item_idx[1]]
        self.item_name = None
        self.health_hp, self.health_sp = None, None
        self.attack, self.defence, self.mattack, self.mdefence, self.hp, self.sp = None, None, None, None, None, None
        self.str, self.agi, self.vit, self.int, self.dex, self.luk = None, None, None, None, None, None
        self.equip_target, self.equip_pos, self.equip_min_level = None, None, None
        self.price = None
        self.icon_image = None
        self.image = None
        self.descrip = None
        self.descrip_color = None
        self.amount = amount
        self.use_action = None
        self.data_setting()

    def usable_use(self, equip_obj):
        health_hp = random.randint(self.health_hp[0], self.health_hp[1]) if self.health_hp is not None else None
        if health_hp is not None:
            Animate_Utility.HealthAnimate.health_hp_group.add(
                Animate_Utility.HealthAnimate(
                    True, health_hp, Graphic.WindowClass.obj.mons_damage_pos, Animate_Utility.HealthAnimate.health_hp_group))
            self.char.hp = self.char.hp + health_hp
            self.char.hp = self.char.attribute.max_hp if self.char.hp >= self.char.attribute.max_hp else self.char.hp
        health_sp = random.randint(self.health_sp[0], self.health_sp[1]) if self.health_sp is not None else None
        if health_sp is not None:
            Animate_Utility.HealthAnimate.health_sp_group.add(
                Animate_Utility.HealthAnimate(
                    False, health_sp, Graphic.WindowClass.obj.mons_damage_pos, Animate_Utility.HealthAnimate.health_sp_group))
            self.char.sp = self.char.sp + health_sp
            self.char.sp = self.char.attribute.max_sp if self.char.sp >= self.char.attribute.max_sp else self.char.sp
        self.amount -= 1
        message = "[物品使用] 使用 " + self.item_name
        if health_hp is not None or health_sp is not None:
            message += " 恢復 HP " + str(health_hp) if health_hp is not None else ""
            message += " 恢復 SP " + str(health_sp) if health_sp is not None else ""
            win = Graphic.WindowClass.obj.get_chat_win([message], [Purple])
            World.WorldClass.chat_group.update(win, None)
        return True

    def equip_use(self, equip_obj):
        response = equip_obj.equip(self)                                        # 可能return True, Equipment_Obj, False
        message = "[物品使用] 裝備 " + self.item_name
        if response is not False:                                               # 代表確實裝備上去
            message += " 成功！"
            win = Graphic.WindowClass.obj.get_chat_win([message], [Purple])
            World.WorldClass.chat_group.update(win, None)
            self.char.attribute.transform(self.char)                            # 裝備上去之後需要更新attribute
            if isinstance(response, ItemObj):
                return response                                                 # 回傳卸下的裝備，準備裝入物品欄
            else:
                return True
        else:
            message += " 失敗！"
            win = Graphic.WindowClass.obj.get_chat_win([message], [Red])
            World.WorldClass.chat_group.update(win, None)
            return response                                                     # 回傳False，裝備失敗

    def data_setting(self):
        self.item_name = self.item_data[1]
        if self.item_type == 0:
            self.health_hp = self.item_data[2]
            if self.health_hp is not None:
                if len(self.health_hp) < 2:                  # 如果只有一個數字代表他是percentage，不然通常是兩個數字
                    self.health_hp = (int(self.health_hp[0] * self.char.attribute.max_hp), int(self.health_hp[0] * self.char.attribute.max_hp) + 1)
            self.health_sp = self.item_data[3]
            if self.health_sp is not None:
                if len(self.health_sp) < 2:
                    self.health_sp = (int(self.health_sp[0] * self.char.attribute.max_sp), int(self.health_sp[0] * self.char.attribute.max_sp) + 1)
            self.price = self.item_data[4]
            self.icon_image = pygame.image.load(self.item_data[5]).convert_alpha()
            self.image = pygame.image.load(self.item_data[6]).convert_alpha()
            self.descrip = self.item_data[7]
            self.descrip_color = self.item_data[8]
            self.use_action = self.usable_use
        elif self.item_type == 1:
            self.attack = self.item_data[2]
            self.defence = self.item_data[3]
            self.mattack = self.item_data[4]
            self.mdefence = self.item_data[5]
            self.hp = self.item_data[6]
            self.sp = self.item_data[7]
            self.str = self.item_data[8]
            self.agi = self.item_data[9]
            self.vit = self.item_data[10]
            self.int = self.item_data[11]
            self.dex = self.item_data[12]
            self.luk = self.item_data[13]
            self.equip_target = self.item_data[14]
            self.equip_pos = self.item_data[15]
            self.equip_min_level = self.item_data[16]
            self.price = self.item_data[17]
            self.icon_image = pygame.image.load(self.item_data[18]).convert_alpha()
            self.image = pygame.image.load(self.item_data[19]).convert_alpha()
            self.descrip = self.item_data[20]
            self.descrip_color = self.item_data[21]
            self.use_action = self.equip_use
        elif self.item_type == 2:
            self.price = self.item_data[2]
            self.icon_image = pygame.image.load(self.item_data[3])
            self.image = pygame.image.load(self.item_data[4])
            self.descrip = self.item_data[5]
            self.descrip_color = self.item_data[6]




