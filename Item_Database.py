import os

folder = "Item_Image"

usable_list = (
  # 編號  名稱       補的HP    補的SP  售價          縮圖路徑                            大圖路徑          詳細說明
    (0,  "蘋果",    (16, 22),  None,  7, os.path.join(folder, "usable_1.png"), None, "清爽香甜的水果,可恢復少量的HP。"),
    (1,  "紅蘿蔔",  (18, 20),  None,  7, os.path.join(folder, "usable_2.png"), None, "紅色的蔬菜。味道香甜,常被拿來作菜食用 可恢復少量的HP。"),
    (2,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_3.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (3,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_4.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (4,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_5.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (5,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_6.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (6,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_7.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (7,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_8.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (8,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_9.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (9,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_10.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (10,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_11.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (11,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_12.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (12,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_13.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (13,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_14.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (14,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_15.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (15,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_16.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (16,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_17.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (17,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_18.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (18,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_19.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (19,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_20.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (20,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_21.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (21,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_1.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (22,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_2.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (23,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_3.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (24,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_4.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (25,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_5.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (26,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_6.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (27,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_7.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (28,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_8.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (29,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_9.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
    (30,  "香蕉",    (17, 21),  None,  7, os.path.join(folder, "usable_10.png"), None, "香甜好吃的水果,可恢復少量的HP。"),
)

equip_list = (
  # 編號  名稱       atk     def    增加hp  增加sp  str agi vit int dex luk  可使用職業    裝備位置  裝備需要等級  售價   縮圖路徑                              大圖路徑   詳細說明
    (0,  "棉襯衫",   None,   10,    None,  None,   0,  0,  0,  0,  0,  0,   range(30),  3,       1,          5,    os.path.join(folder, "equip_1.png"), None,     "純棉製成的衣服,穿著時非常舒服的衣物。"),
    (1,  "短劍",     17,     None,  None,  None,   0,  0,  0,  0,  0,  0,   range(30),  4,       1,          25,   os.path.join(folder, "equip_2.png"), None,     "為了方便任何人使用所製作出來的短劍。")
)

collection_list = (
  # 編號  名稱         售價  縮圖路徑,                               大圖路徑  詳細說明
    (0,  "傑勒比結晶", 3,    os.path.join(folder, "collect_1.png"), None,   "從一部份怪物身上得來的結晶,可向收集商購買。"),
    (1,  "黏稠液體",   35,   os.path.join(folder, "collect_2.png"), None,   "不知名的黏稠液體,可向收集商購買。"),
    (2,  "柔毛",      4,    os.path.join(folder, "collect_3.png"), None,   "相當柔軟的毛,可用來製作高級衣物。可向收集商購買。 "),
    (3,  "毛",        10,   os.path.join(folder, "collect_4.png"), None,   "小型魔物身上的毛,可以用來做衣服的原料,可向收集商購買。")
)

item_list = (usable_list, equip_list, collection_list)


