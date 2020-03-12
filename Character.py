import os, math
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame                                       # 3rd party Library
import Attribute, Monster_Database


class CharacterClass:
    def __init__(self, name, ini_ability):
        self.char_name = name
        self.job_name = "Novice"
        self.job_type = 1

        self.base_level = 1
        self.job_level = 1

        self.zeny = 0
        self.base_exp = 0
        self.target_base_exp = 0
        self.define_base_exp_type()
        self.job_exp = 0
        self.target_job_exp = 0
        self.define_job_exp_type()

        self.equipment = [[], [], [], ["棉襯衫", 10], ["短劍", 17], [], [], [], [], []]
        # Temp Version
        # head_up, head_mid, head_down, body, R-hand, L-hand, robe, shoes, accessory1, accessory2
        self.item = []

        self.ability = Attribute.AbilityClusterClass(ini_ability)          # control str, agi, vit ...etc
        self.attribute = Attribute.AttributeClusterClass(self)  # generate atk, def, flee ...etc

        self.hp = self.attribute.max_hp
        self.sp = self.attribute.max_sp

        self.sit_img_path = os.path.join("Char_Image", self.job_name, "Sit.png")
        self.stand_img_path = os.path.join("Char_Image", self.job_name, "Stand.png")
        self.standby_img_path = os.path.join("Char_Image", self.job_name, "Standby_Dagger.png")
        self.attack_img_path = os.path.join("Char_Image", self.job_name, "Attack_Dagger.png")
        self.dead_img_path = os.path.join("Char_Image", self.job_name, "Dead.png")

        self.sit_img = pygame.image.load(self.sit_img_path).convert_alpha()
        self.stand_img = pygame.image.load(self.stand_img_path).convert_alpha()
        self.dead_img = []
        self.standby_img = []
        self.attack_img = []
        img1 = pygame.image.load(self.standby_img_path).convert_alpha()
        img2 = pygame.image.load(self.attack_img_path).convert_alpha()
        img3 = pygame.image.load(self.dead_img_path).convert_alpha()
        width, height = 200, 200
        for i in range(1, img1.get_size()[0] // width + 1):
            self.standby_img.append(img1.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))
            self.attack_img.append(img2.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))
            self.dead_img.append(img3.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))

    def get_exp(self, base_exp, job_exp):
        if self.base_level < 99:        # 確認是否階段性滿等
            self.base_exp += base_exp
        if self.job_level < job_max_level[self.job_type]:
            self.job_exp += job_exp
        self.check_level_up()

    def check_level_up(self):
        if self.base_level < 99 and self.base_exp > self.target_base_exp:
            self.base_level += 1
            self.base_exp -= self.target_base_exp
            self.define_base_exp_type()                 # 定義下一級目標經驗值
            self.ability.level_up()                     # 加素質點
        if self.job_level < job_max_level[self.job_type] and self.job_exp > self.target_job_exp:
            self.job_level += 1
            self.job_exp -= self.target_job_exp
            self.define_job_exp_type()

    def define_base_exp_type(self):
        if self.job_type == 1 or self.job_type == 2 or self.job_type == 3:  # 未轉生
            self.target_base_exp = int(base_exp_list1[self.base_level+1] / 10)
        elif self.job_type == 4 or self.job_type == 5:    # 轉生
            self.target_base_exp = base_exp_list2[self.base_level+1]

    def define_job_exp_type(self):
        if self.job_type == 1:  # 初心者
            self.target_job_exp = novice_job_exp_list[self.job_level+1]
        elif self.job_type == 2:    # 未轉生一轉職業
            self.target_job_exp = job1_exp_list1[self.job_level+1]
        elif self.job_type == 3:    # 未轉生二轉職業
            self.target_job_exp = job2_exp_list1[self.job_level+1]
        elif self.job_type == 4:    # 轉生一轉職業
            self.target_job_exp = job1_exp_list2[self.job_level+1]
        elif self.job_type == 5:    # 轉生二轉職業
            self.target_job_exp = job2_exp_list2[self.job_level+1]

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


# Base Level 經驗表(轉生前)
base_exp_list1 = [0, 0, 550, 900, 1500, 2200, 3200, 3800, 4200, 4550, 5000, 5500, 6000, 6100, 6350, 6700, 7350, 8000, 8400, 8800, 9200, 9700, 10300, 11000, 11800, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23200, 24000, 26000, 27500, 29000, 30000, 31500, 33000, 34000, 36000, 37500, 38000, 40000, 42000, 44500, 47000, 49000, 51000, 53000, 55000, 57000, 59000, 61500, 63000, 65000, 67000, 69000, 70000, 73000, 77000, 80000, 84000, 88000, 91000, 95000, 110000, 128000, 140000, 155000, 163000, 170000, 180000, 188000, 195000, 200000, 230000, 260000, 300000, 350000, 400000, 480000, 550000, 600000, 680000, 750000, 900000, 1000000, 1200000, 1500000, 1800000, 2100000, 2400000, 2800000, 3300000, 4000000]
# Base Level 經驗表(轉生後)
base_exp_list2 = [0, 0, 660, 1080, 1800, 2640, 3840, 4560, 5040, 5460, 6000, 6600, 7200, 7320, 7620, 8040, 8820, 9600, 10080, 10560, 11040, 12610, 13390, 14300, 15340, 16900, 18460, 19500, 20800, 22100, 23400, 24700, 26000, 27300, 28600, 30160, 31200, 33800, 35750, 37700, 39000, 44100, 46200, 47600, 50400, 52500, 53200, 56000, 58800, 62300, 65800, 68600, 71400, 74200, 77000, 79800, 82600, 86100, 88200, 91000, 96800, 103500, 105000, 109500, 115500, 120000, 126000, 132000, 136500, 142500, 165000, 192000, 210000, 232500, 244500, 255000, 270000, 282000, 292500, 300000, 345000, 416000, 480000, 560000, 640000, 768000, 880000, 960000, 1088000, 1200000, 1440000, 1700000, 2040000, 2550000, 3060000, 3570000, 4080000, 4760000, 5610000, 6800000]
# 初心者 Job 經驗表
novice_job_exp_list = [0, 0, 10, 18, 28, 40, 91, 151, 205, 268, 340]
# 一轉經驗表(轉生前)
job1_exp_list1 = [0, 0, 60, 130, 260, 360, 780, 1060, 1300, 1560, 1910, 2290, 2680, 2990, 3340, 3740, 4360, 4970, 5330, 6120, 6700, 8090, 8920, 9970, 11080, 12690, 14440, 15850, 17400, 19220, 21060, 22870, 24910, 26840, 29080, 31320, 33300, 37110, 40500, 43570, 46180, 53510, 57200, 60310, 65690, 70090, 72130, 77540, 83320, 90120, 97180]
# 一轉經驗表(轉生後)
job1_exp_list2 = [0, 0, 340, 550, 760, 990, 1250, 1600, 1980, 2340, 2740, 3140, 3950, 4510, 5210, 5950, 7000, 8150, 9130, 10220, 11480, 12780, 14090, 15560, 16980, 18620, 20280, 21780, 24510, 27000, 29000, 31000, 36000, 39000, 41000, 45000, 49000, 51900, 55000, 59450, 64630, 70030, 74940, 79800, 84630, 89610, 95170, 100420, 107250, 112070, 118120]
# 二轉經驗表(轉生前)
job2_exp_list1 = [0, 0, 2500, 4200, 7000, 10300, 15900, 18900, 20900, 22600, 24900, 28800, 31500, 32300, 33300, 35100, 40500, 44100, 46300, 48500, 50700, 56000, 59400, 63500, 68100, 75000, 85700, 90500, 96600, 102600, 108600, 119700, 126000, 132300, 138600, 146100, 157500, 170600, 180400, 190300, 196800, 214900, 225200, 232000, 245700, 255900, 279300, 294000, 308700, 327000, 345400]
# 二轉經驗表(轉生後)
job2_exp_list2 = [0, 0, 3800, 6200, 10400, 15200, 22900, 27100, 30000, 32500, 35700, 41300, 45000, 45800, 47600, 50300, 58700, 63900, 67100, 70300, 73500, 90600, 96200, 102700, 110200, 121400, 144700, 152900, 163100, 173300, 183500, 213500, 224700, 236000, 247200, 260700, 299800, 324800, 343600, 362300, 374800, 474400, 497000, 512100, 542200, 564800, 644300, 678200, 712100, 764500, 796900, 949300, 988100, 1026800, 1065600, 1104300, 1334800, 1371400, 1425300, 1470600, 1515800, 2003800, 2032800, 2119900, 2236100, 2323200, 3025300, 3433300, 3776600, 4436900, 6758400]
# Job 等級上限（根據job_type）
job_max_level = [0, 10, 50, 50, 50, 70]


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
        self.standby_img = []
        self.attack_img = []
        self.dead_img = []
        img1 = pygame.image.load(self.standby_img_path).convert_alpha()
        img2 = pygame.image.load(self.attack_img_path).convert_alpha()
        img3 = pygame.image.load(self.dead_img_path).convert_alpha()
        width, height = 200, 200
        for i in range(1, img1.get_size()[0] // width + 1):
            self.standby_img.append(img1.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))
            self.attack_img.append(img2.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))
            self.dead_img.append(img3.subsurface(pygame.Rect((i - 1) * width, 0, width, height)))


