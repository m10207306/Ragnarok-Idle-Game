
class CharacterClass:

    def __init__(self, name):
        self.char_name = name
        self.job_name = "Novice"
        self.hp = 100
        self.max_hp = 100
        self.sp = 100
        self.max_sp = 100
        self.base_level = 1
        self.job_level = 1
        self.attribute = AttributeClusterClass()
        self.zeny = 0
        self.base_exp = 0
        self.target_base_exp = 100
        self.job_exp = 0
        self.target_job_exp = 100
        self.item = []

    def __str__(self):
        base_exp_per = round(self.base_exp / self.target_base_exp * 100, 1)
        job_exp_per = round(self.job_exp / self.target_job_exp * 100, 1)
        return "   Name: " + self.char_name + " / Job: " + self.job_name + "\n"\
               "   HP: " + str(self.hp) + " / " + str(self.max_hp) + "\n"\
               "   SP: " + str(self.sp) + " / " + str(self.max_sp) + "\n"\
               "   Base Experience: " + str(base_exp_per) + " %\n"\
               "   Job Experience: " + str(job_exp_per) + " %\n"\
               "   Zeny: " + tool_money_format(self.zeny)


class AttributeClusterClass:
    def __init__(self):
        self.attribute = [ AttributeClass("str", 1),
                           AttributeClass("agi", 1),
                           AttributeClass("vit", 1),
                           AttributeClass("int", 1),
                           AttributeClass("dex", 1),
                           AttributeClass("luk", 1) ]


class AttributeClass:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


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

