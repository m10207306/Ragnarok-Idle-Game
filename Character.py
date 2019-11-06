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
    value_list = str(money)
    money_str = ""
    count = 1
    for idx, digit in enumerate(reversed(value_list)):
        if count == 3 and idx + 1 != len(value_list):
            money_str = "," + digit + money_str
            count = 1
        else:
            money_str = digit + money_str
            count += 1
    return money_str


# type = [無，火，水，風，地，毒，聖，闇，念，不死]
monster_data = \
    [   # name,    hp, type,      atk, def, mdef, flee, hit, aspd, base_exp, job_exp
        ['Poring', 60,    3, [13, 17],   2,    5,  178, 203,  160,       27,      20]
    ]


class MonsterClass:
    def __init__(self, moster_number):
        self.mons_number = moster_number
        self.mons_name = monster_data[self.mons_number][0]
        self.hp = monster_data[self.mons_number][1]
        self.type = monster_data[self.mons_number][2]
        self.atk = monster_data[self.mons_number][3]
        self.defence = monster_data[self.mons_number][4]
        self.mdefence = monster_data[self.mons_number][5]
        self.flee = monster_data[self.mons_number][6]
        self.hit = monster_data[self.mons_number][7]
        self.aspd = monster_data[self.mons_number][8]
        self.base_exp = monster_data[self.mons_number][9]
        self.job_exp = monster_data[self.mons_number][10]
        self.standby_img_path = os.path.join("Mons_Image", self.mons_name + "_Standby.png")
        self.attack_img_path = os.path.join("Mons_Image", self.mons_name + "_Attack.png")
        self.att_frq = round(50 / (200 - self.aspd), 1)



