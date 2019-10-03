
class CharacterClass:

    def __init__(self, name):
        self.char_name = name
        self.job_name = "Novice"

        self.base_level = 1
        self.job_level = 1

        self.zeny = 0
        self.base_exp = 0
        self.target_base_exp = 100
        self.job_exp = 0
        self.target_job_exp = 100

        self.equipment = []
        self.ability = AbilityClusterClass()
        self.attribute = AttributeClusterClass(self)
        self.item = []

        self.hp = self.attribute.max_hp
        self.sp = self.attribute.max_sp

    def __str__(self):
        base_exp_per = round(self.base_exp / self.target_base_exp * 100, 1)
        job_exp_per = round(self.job_exp / self.target_job_exp * 100, 1)
        return "   Name: " + self.char_name + " / Job: " + self.job_name + "\n"\
               "   HP: " + str(self.hp) + " / " + str(self.attribute.max_hp) + "\n"\
               "   SP: " + str(self.sp) + " / " + str(self.attribute.max_sp) + "\n"\
               "   Base Experience: " + str(base_exp_per) + " %\n"\
               "   Job Experience: " + str(job_exp_per) + " %\n"\
               "   Zeny: " + tool_money_format(self.zeny)

    def attribute_list(self):
        att_list = "=====================================================\n"
        for i in range(len(self.ability.ability)):
            ability = self.ability.ability[i]
            att_list = att_list + ability.tag + ": "
            if ability.value < 10:
                att_list = att_list + "0" + str(ability.value)
            else:
                att_list = att_list + str(att_list.value) + "\n"
        att_list = att_list + ""


class AbilityClusterClass:
    def __init__(self):
        self.ability = [ AbilityClass("str", 1),
                         AbilityClass("agi", 1),
                         AbilityClass("vit", 1),
                         AbilityClass("int", 1),
                         AbilityClass("dex", 1),
                         AbilityClass("luk", 1) ]


class AbilityClass:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


class AttributeClusterClass:
    def __init__(self, char_obj):
        self.char_atk =
        self.weapon_atk =
        self.max_hp = 35 + char_obj.base_level
        self.max_sp =


def tool_money_format(money):
    str_money = str(money)
    str_money = str_money[::-1]  # inverse string
    digit = len(str_money)
    comma_num = digit // 3
    result = ""
    if comma_num > 1:
        for i in range(1, comma_num+1):
            if i == comma_num:
                tmp = str_money[(i-1)*3 : i*3]
                tmp2 = str_money[i*3 : len(str_money)+1]
                result = (tmp2[::-1] + "," + tmp[::-1]) + result
            else:
                tmp = str_money[(i-1)*3 : i*3]
                result = ("," + tmp[::-1]) + result
        return result
    else:
        return str(money)

