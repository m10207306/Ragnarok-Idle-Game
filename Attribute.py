
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
        except ValueError as error_message:
            print(">> " + error_message)
            return


class AbilityClass:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


class AttributeClusterClass:
    def __init__(self, char_obj):
        ability = char_obj.ability
        atk_addition = ability.get_ability("luk").value / 3 + ability.get_ability("dex").value / 5 + char_obj.base_level / 4
        self.max_hp = 35 + char_obj.base_level * 60
        self.max_sp = round((char_obj.base_level * 3) * (100 + ability.get_ability("int").value) / 100)
        self.char_atk = round(ability.get_ability("str").value + atk_addition)
        self.weapon_atk = 0
        self.char_matk = round(ability.get_ability("int").value * 1.5 + atk_addition)
        self.weapon_matk = 0
        self.defence = round((char_obj.base_level + ability.get_ability("vit").value) / 2 + ability.get_ability("agi").value / 5)
        self.m_defence = round(char_obj.base_level / 4 +
                               ability.get_ability("int").value +
                               ability.get_ability("vit").value / 5 +
                               ability.get_ability("dex").value / 5)
        self.hit = round(175 + ability.get_ability("dex").value + char_obj.base_level + ability.get_ability("luk").value / 3)
        self.flee = char_obj.base_level + ability.get_ability("agi").value
        self.cri = round(ability.get_ability("luk").value / 3 + 1)
        self.aspd = round(150 + (200 - 150) * (ability.get_ability("agi").value + ability.get_ability("dex").value / 4) / 250)
        self.att_freq = round(50 / (200 - self.aspd), 1)

    def __str__(self):
        return "  Atk:\t" + str(self.char_atk) + "\t\tDef:\t" + str(self.defence) + "\n" \
               "  Matk:\t" + str(self.char_matk) + "\t\tMdef:\t" + str(self.m_defence) + "\n" \
               "  Hit:\t" + str(self.hit) + "\t\tFlee:\t" + str(self.flee) + "\n" \
               "  Cri:\t" + str(self.cri) + "\t\tAspd:\t" + str(self.aspd) + "\n"
