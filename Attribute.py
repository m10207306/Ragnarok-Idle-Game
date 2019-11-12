import math


class AbilityClusterClass:
    def __init__(self):
        self.ability = [ AbilityClass("str", 1),
                         AbilityClass("agi", 1),
                         AbilityClass("vit", 1),
                         AbilityClass("int", 1),
                         AbilityClass("dex", 1),
                         AbilityClass("luk", 1) ]

    def get_ability(self, ability_tag):
        ability = ["str", "agi", "vit", "int", "dex", "luk"]
        try:
            idx = ability.index(ability_tag)
            return self.ability[idx]
        except Exception as error_message:
            print(">> ", error_message)
            return


class AbilityClass:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


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
        self.type = content[2]
        self.total_atk = [math.floor(content[3]*0.9), math.ceil(content[3]*1.1)]
        self.total_defence = content[4]
        self.total_mdefence = content[5]
        self.flee = content[6]
        self.hit = content[7]
        self.cri = content[11]
        self.aspd = content[8]
        self.att_frq = round(50 / (200 - self.aspd), 1)






