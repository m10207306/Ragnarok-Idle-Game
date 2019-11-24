import os, math
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
        self.job_exp = 0
        self.target_job_exp = 100

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
        self.dead_img_path = os.path.join("Char_Image", self.job_name, "Dead.png")

    def get_exp(self, base_exp, job_exp):
        self.base_exp += base_exp
        self.job_exp += job_exp
        self.check_level_up()

    def check_level_up(self):
        print("Empty")

    def exp_punish(self):
        self.base_exp = self.base_exp - math.floor(0.02 * self.target_base_exp) if \
                        self.base_exp > math.floor(0.02 * self.target_base_exp) else 0
        self.job_exp = self.job_exp - math.floor(0.02 * self.target_job_exp) if \
                       self.job_exp > math.floor(0.02 * self.target_job_exp) else 0

    def respawn(self):
        self.hp = math.floor(0.1 * self.attribute.max_hp)
        self.sp = math.floor(0.1 * self.attribute.max_sp)


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
    [   # name,      hp, type, atk, def, mdef, flee, hit, aspd, base_exp, job_exp, cri
        ["Poring",   60,    3,   7,   2,    5,  178, 203,  150,       27,      20,   5],
        ["Fabre",    72,    4,  15,  25,    7,  159, 207,  150,       54,      41,   5],
        ["Lunatic",  55,    0,  14,  21,    1,  156, 206,  150,       36,      27,   5]
    ]


class MonsterClass:
    def __init__(self, moster_number):
        self.mons_number = moster_number
        self.mons_name = monster_data[self.mons_number][0]
        self.hp = monster_data[self.mons_number][1]
        self.base_exp = monster_data[self.mons_number][9]
        self.job_exp = monster_data[self.mons_number][10]
        self.attribute = Attribute.MonsterAttribute(monster_data[self.mons_number])
        self.standby_img_path = os.path.join("Mons_Image", self.mons_name + "_Standby.png")
        self.attack_img_path = os.path.join("Mons_Image", self.mons_name + "_Attack.png")
        self.dead_img_path = os.path.join("Mons_Image", self.mons_name + "_Dead.png")


