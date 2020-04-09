import os

folder = "Item_Image"
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 222, 0)
Orange = (255, 170, 0)
Battle_Meg_Color = (0, 196, 255)

sword_series = [1, 7, 13, 19, 25]       # 劍士全系列職業編碼
magic_series = [2, 8, 14, 20, 26]
thief_series = [3, 9, 15, 21, 27]
acoly_series = [4, 10, 16, 22, 28]
arche_series = [5, 11, 17, 23, 29]
mechi_series = [6, 12, 18, 24, 30]

usable_list = (
  # 編號  名稱             補的HP    補的SP        售價    縮圖路徑                              大圖路徑                                        詳細說明                                                                                                                    說明字體顏色
    (0,  "蘋果",           (16,   22),  None,         7,   os.path.join(folder, "usable_0.png"), os.path.join(folder, "usable_detail_0.png"),    ("清爽香甜的水果，可恢復少量的HP。",),                                                                                      (Black,)),
    (1,  "紅蘿蔔",         (18,   20),  None,         7,   os.path.join(folder, "usable_1.png"), os.path.join(folder, "usable_detail_1.png"),    ("紅色的蔬菜。味道香甜,常被拿來作菜食用 可恢復少量的HP。",),                                                                (Black,)),
    (2,  "香蕉",           (17,   21),  None,         7,   os.path.join(folder, "usable_2.png"), os.path.join(folder, "usable_detail_2.png"),    ("香甜好吃的水果，可恢復少量的HP。",),                                                                                      (Black,)),
    (3,  "蕃薯",           (15,   23),  None,         7,   os.path.join(folder, "usable_3.png"), os.path.join(folder, "usable_detail_3.png"),    ("含有豐富的澱粉，味道香甜，常被拿來食用 可恢復少量的HP。",),                                                               (Black,)),
    (4,  "牛奶",           (27,   37),  None,        12,   os.path.join(folder, "usable_4.png"), os.path.join(folder, "usable_detail_4.png"),    ("牛奶加工而成的液體，被視為小孩子成長期時最具營養的食品。",),                                                              (Black,)),
    (5,  "肉",             (70,  100),  None,        25,   os.path.join(folder, "usable_5.png"), os.path.join(folder, "usable_detail_5.png"),    ("味道很棒。可恢復少量的HP。",),                                                                                            (Black,)),
    (6,  "好吃的魚",       (100, 150),  None,       125,   os.path.join(folder, "usable_6.png"), os.path.join(folder, "usable_detail_6.png"),    ("随着不同的料理方式，能烹調出多樣吃法的魚，可以區分成白色肉和藍色背的兩種魚，可以恢復少量的HP。",),                        (Black,)),
    (7,  "魔物飼料",       (72,  108),  None,        30,   os.path.join(folder, "usable_7.png"), os.path.join(folder, "usable_detail_7.png"),    ("魔物們最喜愛的加工食品，可恢復少量的HP。",),                                                                              (Black,)),
    (8,  "紅色藥草",       (18,   28),  None,         9,   os.path.join(folder, "usable_8.png"), os.path.join(folder, "usable_detail_8.png"),    ("在治療傷處上有一定功效的珍貴藥草，可恢復少量的HP。",),                                                                    (Black,)),
    (9,  "紅色藥水",       (45,   65),  None,        25,   os.path.join(folder, "usable_9.png"), os.path.join(folder, "usable_detail_9.png"),    ("將紅色藥草搗碎製成的體力恢復劑，HP恢復45。",),                                                                            (Black,)),
    (10,  "黃色藥草",      (38,   58),  None,        20,   os.path.join(folder, "usable_10.png"), os.path.join(folder, "usable_detail_10.png"),  ("在治療傷處上有相當功效的珍貴藥草，可恢復少量的HP。",),                                                                    (Black,)),
    (11,  "黃色藥水",      (175, 235),  None,       275,   os.path.join(folder, "usable_11.png"), os.path.join(folder, "usable_detail_11.png"),  ("將黃色藥草搗碎製成的體力恢復劑，HP恢復175。",),                                                                           (Black,)),
    (12,  "赤色藥水",      (105, 145),  None,       100,   os.path.join(folder, "usable_12.png"), os.path.join(folder, "usable_detail_12.png"),  ("將紅色藥草與黃色藥草搗碎製成的體力恢復劑，HP恢復105。",),                                                                 (Black,)),
    (13,  "白色藥草",      (75,  115),  None,        60,   os.path.join(folder, "usable_13.png"), os.path.join(folder, "usable_detail_13.png"),  ("在治療傷處上功效相當顯著的珍貴藥草，可恢復少量的HP。",),                                                                  (Black,)),
    (14,  "白色藥水",      (325, 405),  None,       600,   os.path.join(folder, "usable_14.png"), os.path.join(folder, "usable_detail_14.png"),  ("將白色的藥草搗碎製成的體力恢復劑，約可恢復325點HP。",),                                                                   (Black,)),
    (15,  "蜂蜜",           (70, 100), (20,  40),   250,   os.path.join(folder, "usable_15.png"), os.path.join(folder, "usable_detail_15.png"),  ("味道香甜的液體，營養相當高，常被拿來治療用，可恢復少量HP與SP。",),                                                        (Black,)),
    (16,  "蜂膠",          (325, 405), (40,  60),  3500,   os.path.join(folder, "usable_16.png"), os.path.join(folder, "usable_detail_16.png"),  ("從蜂蜜收集來的物品，此物品蜂后專門食用的食品，對身體健康有相當幫助，可恢復所有狀態且增加HP和SP。",),                      (Black,)),
    (17,  "瑪絲黛拉果實",  (400, 600),  None,      4250,   os.path.join(folder, "usable_17.png"), os.path.join(folder, "usable_detail_17.png"),  ("瑪絲黛拉樹上采下的紫色果實，可恢復大量的HP。",),                                                                          (Black,)),
    (18,  "年糕",             (0.1, ),  None,        10,   os.path.join(folder, "usable_18.png"), os.path.join(folder, "usable_detail_18.png"),  ("把揉好的粳米粉捏成恰當的大小，塞滿餡之後做成半圓形狀再用松針覆蓋的糕。是熱門韓國傳統節日食物的一種。恢復最大HP的10％",),  (Black,)),
    (19,  "天地樹芽",         (0.5, ),  (0.5, ),   2500,   os.path.join(folder, "usable_19.png"), os.path.join(folder, "usable_detail_19.png"),  ("形成這個世界根源的天地樹果實之芽，透露著微微香氣且甘甜美味，可恢復一半的HP與SP。",),                                      (Black,)),
    (20,  "天地樹果實",       (1.0, ),  (1.0, ),   2500,   os.path.join(folder, "usable_20.png"), os.path.join(folder, "usable_detail_20.png"),  ("天地樹的果實，據說食用後精神會為之一振，感覺活力滿滿。可將使用者的HP和SP全數恢復。",),                                    (Black,)),
    (21,  "綠色藥草",            None,  None,         5,   os.path.join(folder, "usable_21.png"), os.path.join(folder, "usable_detail_21.png"),  ("可中和所有毒性的珍貴藥草,具有治療的功效解毒。",),                                                                         (Black,))
)

head = (
  # 編號  名稱             atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                            大圖路徑                                    詳細說明                                                                                                                           說明字體顏色
    (0,  "初學者蛋殼帽",   0,      3,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0],                                                                              0,        1,            10,     os.path.join(folder, "head_0.png"), os.path.join(folder, "head_detail_0.png"),  ("為了初學冒險者,秘密決死組織在夢羅克的大肚魚同學會裡,所做成100%假的蛋殼帽,說假的令大家還不敢相信,因為手藝非常高明", "不可精鍊"),  (Black, Black)),
    (1,  "漁夫帽",         0,      2,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        0,        1,           500,     os.path.join(folder, "head_1.png"), os.path.join(folder, "head_detail_1.png"),  ("可以遮蔽陽光的寬鬆帽子。",),                                                                                                     (Black,)),
    (2,  "無邊帽",         0,      7,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   sword_series + arche_series + mechi_series + thief_series,                        0,        1,          6000,     os.path.join(folder, "head_2.png"), os.path.join(folder, "head_detail_2.png"),  ("簡單的設計,有著活動性和使用性的帽子。",),                                                                                        (Black,)),
    (3,  "太陽眼鏡",       0,      0,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        1,        1,          2500,     os.path.join(folder, "head_3.png"), os.path.join(folder, "head_detail_3.png"),  ("黑色的眼鏡,可用來阻擋太陽用或當做時髦的裝飾品用。", "對黑暗的攻擊,可減少5% 的傷害度。(未實裝)"),                                 (Black, Battle_Meg_Color)),
    (4,  "眼鏡",           0,      0,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        1,        1,          2000,     os.path.join(folder, "head_4.png"), os.path.join(folder, "head_detail_4.png"),  ("用玻璃壓縮做成的眼鏡,配帶這眼鏡的人,都是視力不太好的人。",),                                                                     (Black,)),
    (5,  "口罩",           0,      0,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        2,        1,           150,     os.path.join(folder, "head_5.png"), os.path.join(folder, "head_detail_5.png"),  ("當感冒或保暖時,所戴的口罩。", "對沉默的攻擊,可減少10% 的傷害度。（未實裝）", "對「中國武漢肺炎」有絕佳抵抗力，出門請戴口罩"),    (Black, Battle_Meg_Color, Orange)),
    (6,  "香菸",           0,      0,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(1, 31),                                                                     2,        1,            10,     os.path.join(folder, "head_6.png"), os.path.join(folder, "head_detail_6.png"),  ("吸煙有害人體健康,未成年的人絕對禁止吸煙。", "受到昆蟲系敵人的攻擊時,可減少3%的傷害度。（未實裝）"),                              (Black, Battle_Meg_Color)),
    (7,  "小丑鼻子",       0,      0,     0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        2,        1,            10,     os.path.join(folder, "head_7.png"), os.path.join(folder, "head_detail_7.png"),  ("小丑戴在鼻子上的飾品。",),                                                                                                       (Black,))
)

armor = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                             大圖路徑                                      詳細說明                                             說明字體顏色
    (0,  "棉襯衫",    0,     10,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        3,        1,               5,   os.path.join(folder, "armor_0.png"), os.path.join(folder, "armor_detail_0.png"),   ("純棉製成的衣服，穿著時非常舒服的衣物。",),         (Black,)),
    (1,  "皮製外套",  0,     15,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        3,        1,             100,   os.path.join(folder, "armor_1.png"), os.path.join(folder, "armor_detail_1.png"),   ("價格低廉的皮製外套,穿久了會有特別的皮革風采。",),  (Black,)),
    (2,  "冒險衣",    0,     20,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        3,        1,             500,   os.path.join(folder, "armor_2.png"), os.path.join(folder, "armor_detail_2.png"),   ("專為冒險者製作的衣服。,"),                         (Black,)),
)

weapon = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                              大圖路徑                                       詳細說明                                             說明字體顏色
    (0,  "短劍",     17,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + magic_series + arche_series + mechi_series + thief_series,   4,        1,              25,   os.path.join(folder, "weapon_0.png"), os.path.join(folder, "weapon_detail_0.png"),   ("為了方便任何人使用所製作出來的短劍。",),           (Black,)),
    (1,  "卡特短劍", 30,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + magic_series + arche_series + mechi_series + thief_series,   4,        1,             625,   os.path.join(folder, "weapon_1.png"), os.path.join(folder, "weapon_detail_1.png"),   ("專門為了割東西所製造出來的短劍。",),               (Black,)),
    (2,  "笨拙短劍", 43,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + magic_series + arche_series + mechi_series + thief_series,   4,        1,            1200,   os.path.join(folder, "weapon_2.png"), os.path.join(folder, "weapon_detail_2.png"),   ("以多功能使用為訴求,所製造出來的短劍。",),          (Black,)),
    (3,  "長劍",     25,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + thief_series + mechi_series,                                 4,        2,              50,   os.path.join(folder, "weapon_3.png"), os.path.join(folder, "weapon_detail_3.png"),   ("看起來任何人都可使用的劍，但服事不能使用。",),     (Black,)),
    (4,  "圓月刀",   39,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + thief_series + mechi_series,                                 4,        2,             750,   os.path.join(folder, "weapon_4.png"), os.path.join(folder, "weapon_detail_4.png"),   ("有著圓刃的刀。",),                                 (Black,)),
    (5,  "厚刃劍",   53,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + thief_series + mechi_series,                                 4,        2,            1450,   os.path.join(folder, "weapon_5.png"), os.path.join(folder, "weapon_detail_5.png"),   ("有著厚刃的劍,用處很廣泛。",),                      (Black,)),
    (6,  "木錘",     23,      0,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + acoly_series + mechi_series,                                 4,        2,              60,   os.path.join(folder, "weapon_6.png"), os.path.join(folder, "weapon_detail_6.png"),   ("木製的鈍器,任何人都方便使用。",),                  (Black,))
)

shield = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                              大圖路徑                                       詳細說明                                             說明字體顏色
    (0,   "鐵盾",     0,     20,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        5,        1,             250,   os.path.join(folder, "shield_0.png"), os.path.join(folder, "shield_detail_0.png"),   ("可以抵擋敵人攻擊的盾牌。"),                        (Black,)),
    (1,   "圓盾",     0,     40,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   sword_series + acoly_series + mechi_series + thief_series,                        5,        1,            7000,   os.path.join(folder, "shield_1.png"), os.path.join(folder, "shield_detail_1.png"),   ("製作簡單且方便使用,所以普遍使用的圓形盾牌。",),    (Black,)),

)

robe = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                            大圖路徑                                    詳細說明                                                     說明字體顏色
    (0,  "連帽披肩",  0,      4,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        6,        1,             500,   os.path.join(folder, "robe_0.png"), os.path.join(folder, "robe_detail_0.png"),  ("保護肩膀和頭部的連帽披肩。",),                             (Black,)),
    (1,  "披肩",      0,      8,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        6,        1,            2500,   os.path.join(folder, "robe_1.png"), os.path.join(folder, "robe_detail_1.png"),  ("圍巾式的斗篷。",),                                         (Black,)),
    (2,  "斗篷",      0,     13,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   [0] + sword_series + mechi_series + thief_series,                                 6,        1,           16000,   os.path.join(folder, "robe_2.png"), os.path.join(folder, "robe_detail_2.png"),  ("用堅硬的布料做成,遮住脖子、肩膀和背部,有防禦力的斗篷。",), (Black,))
)

shoes = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                             大圖路徑                                     詳細說明                                              說明字體顏色
    (0,  "輕便鞋",    0,      5,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(31),                                                                        7,        1,             200,   os.path.join(folder, "shoes_0.png"), os.path.join(folder, "shoes_detail_0.png"),  ("很方便著裝的鞋子,不過沒有什麼防禦力。",),           (Black,)),
    (1,  "長靴",      0,     10,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   range(1, 31),                                                                     7,        1,            1750,   os.path.join(folder, "shoes_1.png"), os.path.join(folder, "shoes_detail_1.png"),  ("保護到腳腕的長靴。",),                              (Black,)),
    (2,  "戰士長靴",  0,     16,    0,    0,    0,     0,      0,  0,  0,  0,  0,  0,   sword_series + arche_series + mechi_series + thief_series,                        7,        1,            9000,   os.path.join(folder, "shoes_2.png"), os.path.join(folder, "shoes_detail_2.png"),  ("用堅硬的布料做成的長靴。",),                        (Black,))
)

accessory = (
  # 編號  名稱       atk     def    matk  mdef  增加hp 增加sp  str agi vit int dex luk  可使用職業                                                                        裝備位置  裝備需要等級  售出    縮圖路徑                                 大圖路徑                                         詳細說明                                                                   說明字體顏色
    (0,  "力量戒指",  0,      0,    0,    0,    0,     0,      2,  0,  0,  0,  0,  0,   range(1, 31),                                                                     8,        20,          15000,   os.path.join(folder, "accessory_0.png"), os.path.join(folder, "accessory_detail_0.png"),  ("讓使用者的力量增強,有神秘魔力的戒指。", "Str + 2"),                      (Black, Orange)),
    (1,  "智力耳環",  0,      0,    0,    0,    0,     0,      0,  0,  0,  2,  0,  0,   range(1, 31),                                                                     8,        20,          15000,   os.path.join(folder, "accessory_1.png"), os.path.join(folder, "accessory_detail_1.png"),  ("掛在耳朵時,會感覺到神秘的力量,是種讓精神抖擻的神奇耳環。", "Int + 2"),   (Black, Orange)),
    (2,  "體力項鏈",  0,      0,    0,    0,    0,     0,      0,  0,  2,  0,  0,  0,   range(1, 31),                                                                     8,        20,          15000,   os.path.join(folder, "accessory_2.png"), os.path.join(folder, "accessory_detail_2.png"),  ("掛在脖子上時,會感覺到全身活力十足的神奇項鏈。", "Vit + 2"),              (Black, Orange)),
    (3,  "防禦手套",  0,      0,    0,    0,    0,     0,      0,  0,  0,  0,  2,  0,   range(1, 31),                                                                     8,        20,          15000,   os.path.join(folder, "accessory_3.png"), os.path.join(folder, "accessory_detail_3.png"),  ("穿戴在手上,可做細活的手套。", "Dex + 2"),                                (Black, Orange)),
    (4,  "敏捷別針",  0,      0,    0,    0,    0,     0,      0,  2,  0,  0,  0,  0,   range(1, 31),                                                                     8,        20,          15000,   os.path.join(folder, "accessory_4.png"), os.path.join(folder, "accessory_detail_4.png"),  ("可以裝飾在衣服和布料上的裝飾品。", "Agi + 2"),                           (Black, Orange))
)


equip_list = (
    head, armor, weapon, shield, robe, shoes, accessory
)

collection_list = (
  # 編號  名稱         售價  縮圖路徑,                               大圖路徑                                       詳細說明                                                      說明字體顏色
    (0,  "傑勒比結晶",     3, os.path.join(folder, "collect_0.png"),  os.path.join(folder, "collect_detail_0.png"),   ("從一部份怪物身上得來的結晶,可向收集商購買。",),                                                                             (Black,)),
    (1,  "空瓶",           3, os.path.join(folder, "collect_1.png"),  os.path.join(folder, "collect_detail_1.png"),   ("什麼也沒裝的瓶子。似乎可以在瓶中裝進東西帶走的樣子。",),                                                                    (Black,)),
    (2,  "黏稠液體",      35, os.path.join(folder, "collect_2.png"),  os.path.join(folder, "collect_detail_2.png"),   ("不知名的黏稠液體,可向收集商購買。",),                                                                                       (Black,)),
    (3,  "青蘋果",       500, os.path.join(folder, "collect_3.png"),  os.path.join(folder, "collect_detail_3.png"),   ("尚未熟透就掉落的蘋果。是魔物波利最喜愛的食物。",),                                                                          (Black,)),
    (4,  "波利卡片",   10000, os.path.join(folder, "collect_4.png"),  os.path.join(folder, "collect_detail_4.png"),   ("Luk + 2", "完全迴避 + 1", "（未實裝）"),                                                                                    (Orange, Orange, Battle_Meg_Color)),
    (5,  "毛",            10, os.path.join(folder, "collect_5.png"),  os.path.join(folder, "collect_detail_5.png"),   ("小型魔物身上的毛,可以用來做衣服的原料,可向收集商購買。",),                                                                  (Black,)),
    (6,  "三葉幸運草",     5, os.path.join(folder, "collect_6.png"),  os.path.join(folder, "collect_detail_6.png"),   ("有著三片心型葉子的植物,6至7月間會開著白色的花,有時候還可以找到有四片葉子的,這類的植物名為幸運草,傳說它會為人帶來好運。",),  (Black,)),
    (7,  "柔毛",           4, os.path.join(folder, "collect_7.png"),  os.path.join(folder, "collect_detail_7.png"),   ("相當柔軟的毛,可用來製作高級衣物。可向收集商購買。",),                                                                       (Black,)),
    (8,  "綠寶石",      3000, os.path.join(folder, "collect_8.png"),  os.path.join(folder, "collect_detail_8.png"),   ("呈現出綠色光芒的寶石。",),                                                                                                  (Black,)),
    (9,  "綠棉蟲卡片", 10000, os.path.join(folder, "collect_4.png"),  os.path.join(folder, "collect_detail_4.png"),   ("Vit + 1", "MHP + 100", "（未實裝）"),                                                                                       (Orange, Orange, Battle_Meg_Color)),
    (10, "彩色紅蘿蔔",  1250, os.path.join(folder, "collect_10.png"), os.path.join(folder, "collect_detail_10.png"),  ("有五種彩虹光芒顏色的紅蘿蔔,隱隱約約的香氣實在誘人,是魔物瘋兔最喜愛的食物。",),                                              (Black,)),
    (11, "瘋兔卡片",   10000, os.path.join(folder, "collect_4.png"),  os.path.join(folder, "collect_detail_4.png"),   ("Luk + 1", "必殺攻擊 + 1", "完全迴避 + 1", "（未實裝）"),                                                                    (Orange, Orange, Orange, Battle_Meg_Color))
)

item_list = (usable_list, equip_list, collection_list)


