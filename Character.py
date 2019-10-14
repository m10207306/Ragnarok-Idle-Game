import time

import Attribute

class CharacterClass:
    def __init__(self, name):
        self.char_name = name
        self.job_name = "Novice"

        self.base_level = 1
        self.job_level = 1

        self.zeny = 0
        self.base_exp = 0
        self.target_base_exp = 100
        self.base_exp_per = round(self.base_exp / self.target_base_exp * 100, 1)
        self.job_exp = 0
        self.target_job_exp = 100
        self.job_exp_per = round(self.job_exp / self.target_job_exp * 100, 1)

        self.equipment = []
        self.ability = Attribute.AbilityClusterClass()
        self.attribute = Attribute.AttributeClusterClass(self)
        self.item = []

        self.hp = self.attribute.max_hp
        self.sp = self.attribute.max_sp

    def __str__(self):
        return "   Name: " + self.char_name + " / Job: " + self.job_name + "\n"\
               "   HP: " + str(self.hp) + " / " + str(self.attribute.max_hp) + "\n"\
               "   SP: " + str(self.sp) + " / " + str(self.attribute.max_sp) + "\n"\
               "   Base Experience: " + str(self.base_exp_per) + " %\n"\
               "   Job Experience: " + str(self.job_exp_per) + " %\n"\
               "   Zeny: " + tool_money_format(self.zeny)

    # def attribute_console(self):
    #     print(self.attribute_list())
    #     while True:
    #         command = input(">> Enter Command: ")
    #         if command == "exit":
    #             return
    #
    # def attribute_list(self):
    #     att_list = "\n=====================================================\n"
    #     att_list += "  Max HP: " + str(self.attribute.max_hp) + "\n" + \
    #                           "  Max SP: " + str(self.attribute.max_sp) + "\n"
    #     for i in range(len(self.ability.ability)):
    #         ability = self.ability.ability[i]
    #         att_list += "  " + ability.tag.capitalize() + ": "
    #         if ability.value < 10:
    #             att_list += "0" + str(ability.value) + "\n"
    #         else:
    #             att_list += str(att_list.value) + "\n"
    #     att_list += str(self.attribute)
    #     return att_list


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

