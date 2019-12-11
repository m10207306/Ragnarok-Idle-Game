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
        try:
            idx = ability.index(ability_tag)
            return self.ability[idx]
        except Exception as error_message:
            print(">> ", error_message)
            return

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
        self.max_hp = []
        self.max_sp = []
        self.char_atk = []          # atk from ability
        self.weapon_atk = []        # atk from weapon
        self.char_matk = []         # matk from ability
        self.weapon_matk = []       # matk from weapon
        self.defence = []           # def
        self.armor_defence = []
        self.mdefence = []          # mdef
        self.armor_mdefence = []
        self.hit = []               # 100% hit needs = (100 + enemy flee)
        self.flee = []
        self.cri = []
        self.aspd = []
        self.att_frq = []           # attack number in one sec
        self.total_atk = []
        self.total_matk = []
        self.total_defence = []
        self.total_mdefence = []
        self.transform(char_obj, char_obj.equipment)

    def transform(self, char_obj, equipment):
        ability = char_obj.ability
        atk_addition = ability.get_ability("luk").value / 3 + ability.get_ability("dex").value / 5 + char_obj.base_level / 4
        self.max_hp = 35 + char_obj.base_level * 60
        self.max_sp = round((char_obj.base_level * 3) * (100 + ability.get_ability("int").value) / 100)
        self.char_atk = round(ability.get_ability("str").value + atk_addition)
        self.weapon_atk = equipment[4][1]
        self.char_matk = round(ability.get_ability("int").value * 1.5 + atk_addition)
        self.weapon_matk = 0
        self.defence = round((char_obj.base_level + ability.get_ability("vit").value) / 2 + ability.get_ability("agi").value / 5)
        self.armor_defence = equipment[3][1]
        self.mdefence = round(char_obj.base_level / 4 +
                               ability.get_ability("int").value +
                               ability.get_ability("vit").value / 5 +
                               ability.get_ability("dex").value / 5)
        self.armor_mdefence = 0
        self.hit = round(175 + ability.get_ability("dex").value + char_obj.base_level + ability.get_ability("luk").value / 3)
        self.flee = round(100 + char_obj.base_level + ability.get_ability("agi").value + ability.get_ability("luk").value / 5)
        self.cri = round(ability.get_ability("luk").value / 3 + 1)
        self.aspd = round(160 + (200 - 150) * (ability.get_ability("agi").value + ability.get_ability("dex").value / 4) / 250)
        self.aspd = 190 if self.aspd > 190 else self.aspd
        self.aspd = 150 if self.aspd < 150 else self.aspd
        self.att_frq = round(50 / (200 - self.aspd), 1)
        self.total_atk = [math.floor((self.char_atk + self.weapon_atk) * 0.9), math.ceil((self.char_atk + self.weapon_atk) * 1.1)]
        self.total_matk = [math.floor((self.char_matk + self.weapon_matk) * 0.9), math.ceil((self.char_matk + self.weapon_matk) * 1.1)]
        self.total_defence = self.defence + self.armor_defence
        self.total_mdefence = self.mdefence + self.armor_mdefence


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
        self.att_frq = round(50 / (200 - self.aspd), 1)






