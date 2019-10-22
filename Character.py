import os
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

        self.equipment = [[], [], [], ["棉襯衫", 10], ["短劍", 17], [], [], [], [], []]
        # Temp Version
        # head_up, head_mid, head_down, body, R-hand, L-hand, robe, shoes, accessory1, accessory2
        self.item = []

        self.ability = Attribute.AbilityClusterClass()          # control str, agi, vit ...etc
        self.attribute = Attribute.AttributeClusterClass(self)  # generate atk, def, flee ...etc

        self.hp = self.attribute.max_hp
        self.sp = self.attribute.max_sp

        self.sit_img_path = os.path.join("Char_Image", self.job_name, "Sit.png")
        self.standby_img_path = os.path.join("Char_Image", self.job_name, "Standby_Dagger.png")
        self.attack_img_path = os.path.join("Char_Image", self.job_name, "Attack_Dagger.png")


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

