import os

folder = "Item_Image"
Black = (0, 0, 0)

usable_list = (
  # 編號  名稱             補的HP    補的SP       售價          縮圖路徑                            大圖路徑                                  詳細說明
    (0,  "蘋果",          (16,   22),  None,      7,      os.path.join(folder, "usable_0.png"), os.path.join(folder, "usable_detail_0.png"),    ("清爽香甜的水果，可恢復少量的HP。",),                                                                          (Black,)),
    (1,  "紅蘿蔔",        (18,   20),  None,      7,      os.path.join(folder, "usable_1.png"), os.path.join(folder, "usable_detail_1.png"),    ("紅色的蔬菜。味道香甜,常被拿來作菜食用 可恢復少量的HP。",),                                                       (Black,)),
    (2,  "香蕉",          (17,   21),  None,      7,      os.path.join(folder, "usable_2.png"), os.path.join(folder, "usable_detail_2.png"),    ("香甜好吃的水果，可恢復少量的HP。",),                                                                          (Black,)),
    (3,  "蕃薯",          (15,   23),  None,      7,      os.path.join(folder, "usable_3.png"), os.path.join(folder, "usable_detail_3.png"),    ("含有豐富的澱粉，味道香甜，常被拿來食用 可恢復少量的HP。",),                                                      (Black,)),
    (4,  "牛奶",          (27,   37),  None,      12,     os.path.join(folder, "usable_4.png"), os.path.join(folder, "usable_detail_4.png"),    ("牛奶加工而成的液體，被視為小孩子成長期時最具營養的食品。",),                                                      (Black,)),
    (5,  "肉",            (70,  100),  None,      25,     os.path.join(folder, "usable_5.png"), os.path.join(folder, "usable_detail_5.png"),    ("味道很棒。可恢復少量的HP。",),                                                                              (Black,)),
    (6,  "好吃的魚",       (100, 150),  None,      125,    os.path.join(folder, "usable_6.png"), os.path.join(folder, "usable_detail_6.png"),    ("随着不同的料理方式，能烹調出多樣吃法的魚，可以區分成白色肉和藍色背的兩種魚，可以恢復少量的HP。",),                    (Black,)),
    (7,  "魔物飼料",       (72,  108),  None,      30,     os.path.join(folder, "usable_7.png"), os.path.join(folder, "usable_detail_7.png"),    ("魔物們最喜愛的加工食品，可恢復少量的HP。",),                                                                  (Black,)),
    (8,  "紅色藥草",       (18,   28),  None,      9,      os.path.join(folder, "usable_8.png"), os.path.join(folder, "usable_detail_8.png"),    ("在治療傷處上有一定功效的珍貴藥草，可恢復少量的HP。",),                                                          (Black,)),
    (9,  "紅色藥水",       (45,   65),  None,      25,     os.path.join(folder, "usable_9.png"), os.path.join(folder, "usable_detail_9.png"),    ("將紅色藥草搗碎製成的體力恢復劑，HP恢復45。",),                                                                (Black,)),
    (10,  "黃色藥草",      (38,   58),  None,      20,     os.path.join(folder, "usable_10.png"), os.path.join(folder, "usable_detail_10.png"),  ("在治療傷處上有相當功效的珍貴藥草，可恢復少量的HP。",),                                                          (Black,)),
    (11,  "黃色藥水",      (175, 235),  None,      275,    os.path.join(folder, "usable_11.png"), os.path.join(folder, "usable_detail_11.png"),  ("將黃色藥草搗碎製成的體力恢復劑，HP恢復175。",),                                                               (Black,)),
    (12,  "赤色藥水",      (105, 145),  None,      100,    os.path.join(folder, "usable_12.png"), os.path.join(folder, "usable_detail_12.png"),  ("將紅色藥草與黃色藥草搗碎製成的體力恢復劑，HP恢復105。",),                                                       (Black,)),
    (13,  "白色藥草",      (75,  115),  None,      60,     os.path.join(folder, "usable_13.png"), os.path.join(folder, "usable_detail_13.png"),  ("在治療傷處上功效相當顯著的珍貴藥草，可恢復少量的HP。",),                                                        (Black,)),
    (14,  "白色藥水",      (325, 405),  None,      600,    os.path.join(folder, "usable_14.png"), os.path.join(folder, "usable_detail_14.png"),  ("將白色的藥草搗碎製成的體力恢復劑，約可恢復325點HP。",),                                                         (Black,)),
    (15,  "蜂蜜",          (70, 100),  (20,  40),  250,   os.path.join(folder, "usable_15.png"), os.path.join(folder, "usable_detail_15.png"),  ("味道香甜的液體，營養相當高，常被拿來治療用，可恢復少量HP與SP。",),                                                (Black,)),
    (16,  "蜂膠",          (325, 405), (40,  60),  3500,  os.path.join(folder, "usable_16.png"), os.path.join(folder, "usable_detail_16.png"),  ("從蜂蜜收集來的物品，此物品蜂后專門食用的食品，對身體健康有相當幫助，可恢復所有狀態且增加HP和SP。",),                   (Black,)),
    (17,  "瑪絲黛拉果實",   (400, 600),  None,      4250,  os.path.join(folder, "usable_17.png"), os.path.join(folder, "usable_detail_17.png"),  ("瑪絲黛拉樹上采下的紫色果實，可恢復大量的HP。",),                                                                (Black,)),
    (18,  "年糕",          (0.1, ),     None,      10,    os.path.join(folder, "usable_18.png"), os.path.join(folder, "usable_detail_18.png"),  ("把揉好的粳米粉捏成恰當的大小，塞滿餡之後做成半圓形狀再用松針覆蓋的糕。是熱門韓國傳統節日食物的一種。恢復最大HP的10％",),  (Black,)),
    (19,  "天地樹芽",       (0.5, ),    (0.5, ),    2500,  os.path.join(folder, "usable_19.png"), os.path.join(folder, "usable_detail_19.png"),  ("形成這個世界根源的天地樹果實之芽，透露著微微香氣且甘甜美味，可恢復一半的HP與SP。",),                                 (Black,)),
    (20,  "天地樹果實",     (1.0, ),    (1.0, ),    2500,  os.path.join(folder, "usable_20.png"), os.path.join(folder, "usable_detail_20.png"),  ("天地樹的果實，據說食用後精神會為之一振，感覺活力滿滿。可將使用者的HP和SP全數恢復。",),                               (Black,)),
)

equip_list = (
  # 編號  名稱       atk    def   matk   mdef 增加hp  增加sp  str agi vit int dex luk  可使用職業    裝備位置  裝備需要等級  售價   縮圖路徑                              大圖路徑                                      詳細說明
    (0,  "棉襯衫",   0,     10,    0,    0,   0,     0,      0,  0,  0,  0,  0,  0,   range(30),  3,       1,          5,    os.path.join(folder, "equip_0.png"), os.path.join(folder, "equip_detail_0.png"),   ("純棉製成的衣服,穿著時非常舒服的衣物。",),           (Black,)),
    (1,  "短劍",     17,     0,    0,    0,   0,     0,      0,  0,  0,  0,  0,  0,   range(30),  4,       1,          25,   os.path.join(folder, "equip_1.png"), os.path.join(folder, "equip_detail_1.png"),   ("為了方便任何人使用所製作出來的短劍。",),            (Black,)),
    (2, "鐵盾", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 5, 1, 25, os.path.join(folder, "equip_2.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (3, "短劍", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 4, 1, 25, os.path.join(folder, "equip_3.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (4, "蛋殼帽", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 0, 1, 25, os.path.join(folder, "equip_4.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (5, "眼鏡", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 1, 1, 25, os.path.join(folder, "equip_5.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (6, "草葉", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 2, 1, 25, os.path.join(folder, "equip_6.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (7, "披肩", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 6, 1, 25, os.path.join(folder, "equip_7.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (8, "海灘鞋", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 7, 1, 25, os.path.join(folder, "equip_8.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (9, "力量手環", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 8, 1, 25, os.path.join(folder, "equip_9.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),
    (10, "敏捷別針", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, range(30), 8, 1, 25, os.path.join(folder, "equip_10.png"), os.path.join(folder, "equip_detail_1.png"), ("為了方便任何人使用所製作出來的短劍。",), (Black,)),

)

collection_list = (
  # 編號  名稱         售價  縮圖路徑,                               大圖路徑  詳細說明
    (0,  "傑勒比結晶", 3,    os.path.join(folder, "collect_0.png"), os.path.join(folder, "collect_detail_0.png"),   ("從一部份怪物身上得來的結晶,可向收集商購買。",),            (Black,)),
    (1,  "黏稠液體",   35,   os.path.join(folder, "collect_1.png"), os.path.join(folder, "collect_detail_1.png"),   ("不知名的黏稠液體,可向收集商購買。",),                    (Black,)),
    (2,  "柔毛",      4,    os.path.join(folder, "collect_2.png"), os.path.join(folder, "collect_detail_2.png"),   ("相當柔軟的毛,可用來製作高級衣物。可向收集商購買。 ",),      (Black,)),
    (3,  "毛",        10,   os.path.join(folder, "collect_3.png"), os.path.join(folder, "collect_detail_3.png"),   ("小型魔物身上的毛,可以用來做衣服的原料,可向收集商購買。",),   (Black,))
)

item_list = (usable_list, equip_list, collection_list)


