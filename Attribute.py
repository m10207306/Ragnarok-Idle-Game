import math


class AbilityClusterClass:
    def __init__(self, ini_ability):
        self.ability = [ AbilityClass("str", ini_ability[0]),
                         AbilityClass("agi", ini_ability[1]),
                         AbilityClass("vit", ini_ability[2]),
                         AbilityClass("int", ini_ability[3]),
                         AbilityClass("dex", ini_ability[4]),
                         AbilityClass("luk", ini_ability[5]) ]
        self.status_point = 0
        self.level = 1

    def get_ability(self, ability_tag):
        ability = ["str", "agi", "vit", "int", "dex", "luk"]
        return self.ability[ability.index(ability_tag)]

    def level_up(self):
        self.status_point += levelup_ability_point[self.level + 1]
        self.level += 1


# 升級時所給予的素質升級點
levelup_ability_point = [0, 0] \
                        + [3 for _ in range(4)] + [4 for _ in range(5)] + [5 for _ in range(5)] \
                        + [6 for _ in range(5)] + [7 for _ in range(5)] + [8 for _ in range(5)] \
                        + [9 for _ in range(5)] + [10 for _ in range(5)] + [11 for _ in range(5)] \
                        + [12 for _ in range(5)] + [13 for _ in range(5)] + [14 for _ in range(5)] \
                        + [15 for _ in range(5)] + [16 for _ in range(5)] + [17 for _ in range(5)] \
                        + [18 for _ in range(5)] + [19 for _ in range(5)] + [20 for _ in range(5)] \
                        + [21 for _ in range(5)] + [22 for _ in range(5)]

# 素質提升所需要的升級點
ability_upgrade_point = [0, 0] \
                        + [2 for _ in range(10)] + [3 for _ in range(10)] + [4 for _ in range(10)] \
                        + [5 for _ in range(10)] + [6 for _ in range(10)] + [7 for _ in range(10)] \
                        + [8 for _ in range(10)] + [9 for _ in range(10)] + [10 for _ in range(10)] \
                        + [11 for _ in range(9)]


class AbilityClass:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
        self.upgrade_demand = ability_upgrade_point[self.value + 1]

    def add_ability(self):
        self.value += 1
        self.upgrade_demand = ability_upgrade_point[self.value + 1]


class AttributeClusterClass:
    def __init__(self, char_obj):
        self.equip_hp = []
        self.equip_sp = []
        self.max_hp = []
        self.max_sp = []
        self.char_atk = []          # atk from ability
        self.equip_atk = []         # atk from equipment
        self.char_matk = []         # matk from ability
        self.equip_matk = []        # matk from equipment
        self.char_def = []          # def
        self.equip_def = []
        self.char_mdef = []         # mdef
        self.equip_mdef = []
        self.equip_str = []
        self.equip_agi = []
        self.equip_vit = []
        self.equip_int = []
        self.equip_dex = []
        self.equip_luk = []
        self.hit = []               # 100% hit needs = (100 + enemy flee)
        self.flee = []
        self.cri = []
        self.aspd = []
        self.att_frame = []         # frame number in an attack
        self.total_atk = []
        self.total_matk = []
        self.total_def = []
        self.total_mdef = []
        self.transform(char_obj)

    def transform(self, char_obj):
        ability = char_obj.ability
        self.equip_str = char_obj.equipment.equip_str
        self.equip_agi = char_obj.equipment.equip_agi
        self.equip_vit = char_obj.equipment.equip_vit
        self.equip_int = char_obj.equipment.equip_int
        self.equip_dex = char_obj.equipment.equip_dex
        self.equip_luk = char_obj.equipment.equip_luk
        atk_addition = (ability.get_ability("luk").value + self.equip_luk) / 3 + \
                       (ability.get_ability("dex").value + self.equip_dex) / 5 + \
                       char_obj.base_level / 4
        self.equip_hp = char_obj.equipment.equip_hp
        self.equip_sp = char_obj.equipment.equip_sp
        self.max_hp = round(35 +
                            char_obj.base_level * 60 * (100 + (ability.get_ability("vit").value + self.equip_vit)) / 100) + \
                            self.equip_hp
        self.max_sp = round((char_obj.base_level * 3) * (100 + (ability.get_ability("int").value + self.equip_int)) / 100) + \
                             self.equip_sp
        self.char_atk = round((ability.get_ability("str").value + self.equip_str) + atk_addition)
        self.equip_atk = char_obj.equipment.equip_atk
        self.char_matk = round((ability.get_ability("int").value + self.equip_int) * 1.5 + atk_addition)
        self.equip_matk = char_obj.equipment.equip_matk
        self.char_def = round((char_obj.base_level + (ability.get_ability("vit").value + self.equip_vit)) / 2 +
                              (ability.get_ability("agi").value + self.equip_agi) / 5)
        self.equip_def = char_obj.equipment.equip_def
        self.char_mdef = round(char_obj.base_level / 4 +
                               (ability.get_ability("int").value + self.equip_int) +
                               (ability.get_ability("vit").value + self.equip_vit) / 5 +
                               (ability.get_ability("dex").value + self.equip_dex) / 5)
        self.equip_mdef = char_obj.equipment.equip_mdef
        self.hit = round(175 + (ability.get_ability("dex").value + self.equip_dex) +
                         char_obj.base_level +
                         (ability.get_ability("luk").value + self.equip_luk) / 3)
        self.flee = round(100 + char_obj.base_level +
                          (ability.get_ability("agi").value + self.equip_agi) +
                          (ability.get_ability("luk").value + self.equip_luk) / 5)
        self.cri = round((ability.get_ability("luk").value + self.equip_luk) / 3 + 1)
        self.aspd = round(160 +
                          (200 - 150) *
                          ((ability.get_ability("agi").value + self.equip_agi) + (ability.get_ability("dex").value + self.equip_dex) / 4) / 250)
        self.aspd = 190 if self.aspd > 190 else self.aspd
        self.aspd = 150 if self.aspd < 150 else self.aspd
        self.att_frame = round(60 / round(50 / (200 - self.aspd)))
        self.total_atk = [math.floor((self.char_atk + self.equip_atk) * 0.9), math.ceil((self.char_atk + self.equip_atk) * 1.1)]
        self.total_matk = [math.floor((self.char_matk + self.equip_matk) * 0.9), math.ceil((self.char_matk + self.equip_matk) * 1.1)]
        self.total_def = self.char_def + self.equip_def
        self.total_mdef = self.char_mdef + self.equip_mdef


class MonsterAttribute:
    def __init__(self, content):
        self.type = content[4]
        self.total_atk = [math.floor(content[5]*0.9), math.ceil(content[5]*1.1)]
        self.total_defence = content[6]
        self.total_mdefence = content[7]
        self.flee = content[8]
        self.hit = content[9]
        self.cri = content[13]
        self.aspd = content[10]
        self.att_frame = round(50 / (200 - self.aspd) * 60)






