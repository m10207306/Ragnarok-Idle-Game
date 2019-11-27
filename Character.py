import os, math
import Attribute, Monster_Database


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


base_exp_list = [0, 0, 550, 900, 1500, 2200, 3200, 3800, 4200, 4550, 5000, 5500, 6000, 6100, 6350, 6700, 7350, 8000, 8400, 8800, 9200, 9700, 10300, 11000, 11800, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23200, 24000, 26000, 27500, 29000, 30000, 31500, 33000, 34000, 36000, 37500, 38000, 40000, 42000, 44500, 47000, 49000, 51000, 55000, 59000, 61500, 61500, 63000, 65000, 67000, 69000, 69000, 70000, 73000, 77000, 80000, 84000, 88000, 91000, 95000, 110000, 128000, 140000, 155000, 163000, 170000, 180000, 188000, 195000, 200000, 230000, 260000, 300000, 350000, 400000, 480000, 550000, 600000, 680000, 750000, 900000, 1000000, 1200000, 1500000, 1800000, 2100000, 2400000, 2800000, 3300000, 4000000]

class MonsterClass:
    def __init__(self, moster_number):
        self.mons_number = moster_number
        self.mons_en_name = Monster_Database.monster_data[self.mons_number][0]
        self.mons_zh_name = Monster_Database.monster_data[self.mons_number][1]
        self.base_level = Monster_Database.monster_data[self.mons_number][2]
        self.hp = Monster_Database.monster_data[self.mons_number][3]
        self.base_exp = Monster_Database.monster_data[self.mons_number][11]
        self.job_exp = Monster_Database.monster_data[self.mons_number][12]
        self.attribute = Attribute.MonsterAttribute(Monster_Database.monster_data[self.mons_number])
        self.standby_img_path = os.path.join("Mons_Image", self.mons_en_name + "_Standby.png")
        self.attack_img_path = os.path.join("Mons_Image", self.mons_en_name + "_Attack.png")
        self.dead_img_path = os.path.join("Mons_Image", self.mons_en_name + "_Dead.png")


