import os                                           # Built-in Library
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"   # Block the information from importing pygame
import pygame

center_x, center_y = 679, 583           # prontera
map_size = 50
step = 56

center2_x, center2_y = 484, 805         # morroc

# type = 1(城市), 2(原野)
map_data = \
    [    # en_name,      zh_name,                             type   BGM                              可前往的地圖編號       在地圖總覽中的座標位置
        [0,  "prontera",     "盧恩　米德加茲王國　首都　普隆德拉", 1,     "prontera",                      [2,   6,  7,  9],    pygame.Rect(center_x,             center_y,             map_size, map_size)],
        [1,  "prt_fild00",   "普隆德拉　區域0",                 2,     "prt_fild_00_02_03_04_07",       [5,  15, 58, 60],    pygame.Rect(center_x - 2 * step,  center_y - 1 * step,  map_size, map_size)],
        [2,  "prt_fild01",   "普隆德拉　區域1",                 2,     "prt_fild_01_05_06_08",          [0,   3, 60, 61],    pygame.Rect(center_x,             center_y - 1 * step,  map_size, map_size)],
        [3,  "prt_fild02",   "普隆德拉　區域2",                 2,     "prt_fild_00_02_03_04_07",       [2,   4,  7],        pygame.Rect(center_x + 1 * step,  center_y - 1 * step,  map_size, map_size)],
        [4,  "prt_fild03",   "普隆德拉　區域3",                 2,     "prt_fild_00_02_03_04_07",       [3],                 pygame.Rect(center_x + 2 * step,  center_y - 1 * step,  map_size, map_size)],
        [5,  "prt_fild04",   "普隆德拉　區域4",                 2,     "prt_fild_00_02_03_04_07",       [1,   6, 16],        pygame.Rect(center_x - 2 * step,  center_y,             map_size, map_size)],
        [6,  "prt_fild05",   "普隆德拉　區域5",                 2,     "prt_fild_01_05_06_08",          [0,   5,  8, 60],    pygame.Rect(center_x - 1 * step,  center_y,             map_size, map_size)],
        [7,  "prt_fild06",   "普隆德拉　區域6",                 2,     "prt_fild_01_05_06_08",          [0,   3],            pygame.Rect(center_x + 1 * step,  center_y,             map_size, map_size)],
        [8,  "prt_fild07",   "普隆德拉　區域7",                 2,     "prt_fild_00_02_03_04_07",       [6,   9, 10, 17],    pygame.Rect(center_x - 1 * step,  center_y + 1 * step,  map_size, map_size)],
        [9,  "prt_fild08",   "普隆德拉　區域8",                 2,     "prt_fild_01_05_06_08",          [0,   8, 13, 28],    pygame.Rect(center_x,             center_y + 1 * step,  map_size, map_size)],
        [10, "prt_fild09",   "普隆德拉　區域9",                 2,     "prt_fild_09_10_11",             [8,  11, 28],        pygame.Rect(center_x - 1 * step,  center_y + 2 * step,  map_size, map_size)],
        [11, "prt_fild10",   "普隆德拉　區域10",                2,     "prt_fild_09_10_11",             [10, 12, 17],        pygame.Rect(center_x - 2 * step,  center_y + 2 * step,  map_size, map_size)],
        [12, "prt_fild11",   "普隆德拉　區域11",                2,     "prt_fild_09_10_11",             [11, 18, 26],        pygame.Rect(center_x - 3 * step,  center_y + 2 * step,  map_size, map_size)],
        [13, "izlude",       "衛星都市　伊斯魯德",              1,     "izlude",                         [9],                pygame.Rect(center_x + 1 * step,  center_y + 1 * step,  map_size, map_size)],
        [14, "geffen",       "魔法之都　吉芬",                  1,     "geffen",                        [15, 19, 22],        pygame.Rect(center_x - 4 * step,  center_y - 1 * step,  map_size, map_size)],
        [15, "gef_fild00",   "吉芬　區域0",                    2,     "gef_fild_00_04_07",              [1,  14, 57],       pygame.Rect(center_x - 3 * step,  center_y - 1 * step,  map_size, map_size)],
        [16, "gef_fild01",   "吉芬　區域1",                    2,     "gef_fild_01_05_06_08_09",        [5,  18, 24],       pygame.Rect(center_x - 3 * step,  center_y,             map_size, map_size)],
        [17, "gef_fild02",   "吉芬　區域2",                    2,     "gef_fild_02_03_10",              [8,  11, 18],       pygame.Rect(center_x - 2 * step,  center_y + 1 * step,  map_size, map_size)],
        [18, "gef_fild03",   "吉芬　區域3",                    2,     "gef_fild_02_03_10",              [12, 16, 17, 25],   pygame.Rect(center_x - 3 * step,  center_y + 1 * step,  map_size, map_size)],
        [19, "gef_fild04",   "吉芬　區域4",                    2,     "gef_fild_00_04_07",              [14, 20, 52, 57],   pygame.Rect(center_x - 4 * step,  center_y - 2 * step,  map_size, map_size)],
        [20, "gef_fild05",   "吉芬　區域5",                    2,     "gef_fild_01_05_06_08_09",        [19, 21, 22],       pygame.Rect(center_x - 5 * step,  center_y - 2 * step,  map_size, map_size)],
        [21, "gef_fild06",   "吉芬　區域6",                    2,     "gef_fild_01_05_06_08_09",        [20, 23],           pygame.Rect(center_x - 6 * step,  center_y - 2 * step,  map_size, map_size)],
        [22, "gef_fild07",   "吉芬　區域7",                    2,     "gef_fild_00_04_07",              [14, 20, 23],       pygame.Rect(center_x - 5 * step,  center_y - 1 * step,  map_size, map_size)],
        [23, "gef_fild08",   "吉芬　區域8",                    2,     "gef_fild_01_05_06_08_09",        [21, 22],           pygame.Rect(center_x - 6 * step,  center_y - 1 * step,  map_size, map_size)],
        [24, "gef_fild09",   "吉芬　區域9",                    2,     "gef_fild_01_05_06_08_09",        [16, 25],           pygame.Rect(center_x - 4 * step,  center_y,             map_size, map_size)],
        [25, "gef_fild10",   "吉芬　區域10",                   2,     "gef_fild_02_03_10",              [18, 24, 26],       pygame.Rect(center_x - 4 * step,  center_y + 1 * step,  map_size, map_size)],
        [26, "gef_fild11",   "吉芬　區域11",                   2,     "gef_fild_11",                    [12, 25],           pygame.Rect(center_x - 4 * step,  center_y + 2 * step,  map_size, map_size)],
        [27, "morroc",       "沙漠之都　夢羅克",                1,     "morroc",                        [31, 33, 38, 39],    pygame.Rect(center2_x,             center2_y,             map_size, map_size)],
        [28, "moc_fild01",   "夢羅克　區域1",                  2,     "moc_fild_01_07",                [9, 10, 44],         pygame.Rect(center_x,              center_y + 2 * step,   map_size, map_size)],
        [29, "moc_fild02",   "夢羅克　區域2",                  2,     "moc_fild_02_03_13",             [28, 34, 44],        pygame.Rect(center2_x + 4 * step,  center2_y - 1 * step,  map_size, map_size)],
        [30, "moc_fild03",   "夢羅克　區域3",                  2,     "moc_fild_02_03_13",             [34, 41],            pygame.Rect(center2_x + 5 * step,  center2_y,             map_size, map_size)],
        [31, "moc_fild07",   "夢羅克　區域7",                  2,     "moc_fild_01_07",                [27],                pygame.Rect(center2_x,             center2_y - 1 * step,  map_size, map_size)],
        [32, "moc_fild11",   "夢羅克　區域11",                 2,     "moc_fild_11_12_17_18_19",       [33, 36],            pygame.Rect(center2_x + 1 * step,  center2_y + 1 * step,  map_size, map_size)],
        [33, "moc_fild12",   "夢羅克　區域12",                 2,     "moc_fild_11_12_17_18_19",       [27, 32, 37],        pygame.Rect(center2_x,             center2_y + 1 * step,  map_size, map_size)],
        [34, "moc_fild13",   "夢羅克　區域13",                 2,     "moc_fild_02_03_13",             [29, 30],            pygame.Rect(center2_x + 4 * step,  center2_y,             map_size, map_size)],
        [35, "moc_fild16",   "夢羅克　區域16",                 2,     "moc_fild_16",                   [36],                pygame.Rect(center2_x + 2 * step,  center2_y + 2 * step,  map_size, map_size)],
        [36, "moc_fild17",   "夢羅克　區域17",                 2,     "moc_fild_11_12_17_18_19",       [32, 35, 37],        pygame.Rect(center2_x + 1 * step,  center2_y + 2 * step,  map_size, map_size)],
        [37, "moc_fild18",   "夢羅克　區域18",                 2,     "moc_fild_11_12_17_18_19",       [33, 36],            pygame.Rect(center2_x,             center2_y + 2 * step,  map_size, map_size)],
        [38, "moc_fild19",   "史芬克斯密穴口",                 1,     "moc_fild_11_12_17_18_19",        [27],               pygame.Rect(center2_x - 1 * step,  center2_y,             map_size, map_size)],
        [39, "moc_ruins",    "金字塔迷宮口",                   1,     "moc_fild_11_12_17_18_19",       [27],                pygame.Rect(center2_x - 1 * step,  center2_y - 1 * step,  map_size, map_size)],
        [40, "payon",        "山岳之都　斐揚",                 1,     "payon",                          [41, 47, 50],       pygame.Rect(center2_x + 6 * step,  center2_y - 1 * step,  map_size, map_size)],
        [41, "pay_fild01",   "斐揚　區域1",                    2,     "pay_fild_01_02_03_04_08",       [30, 40, 42, 46],    pygame.Rect(center2_x + 6 * step,  center2_y,             map_size, map_size)],
        [42, "pay_fild02",   "斐揚　區域2",                    2,     "pay_fild_01_02_03_04_08",       [41, 43],            pygame.Rect(center2_x + 6 * step,  center2_y + 1 * step,  map_size, map_size)],
        [43, "pay_fild03",   "斐揚　區域3",                    2,     "pay_fild_01_02_03_04_08",       [42, 45, 46, 51],    pygame.Rect(center2_x + 7 * step,  center2_y + 1 * step,  map_size, map_size)],
        [44, "pay_fild04",   "斐揚　區域4",                    2,     "pay_fild_01_02_03_04_08",       [28, 29],            pygame.Rect(center_x + 1 * step,   center_y + 2 * step,   map_size, map_size)],
        [45, "pay_fild06",   "斐揚　區域6",                    2,     "pay_fild_06_07_09_10",          [43],                pygame.Rect(center2_x + 7 * step,  center2_y + 2 * step,  map_size, map_size)],
        [46, "pay_fild07",   "斐揚　區域7",                    2,     "pay_fild_06_07_09_10",          [41, 43, 47, 49],    pygame.Rect(center2_x + 7 * step,  center2_y,             map_size, map_size)],
        [47, "pay_fild08",   "斐揚　區域8",                    2,     "pay_fild_01_02_03_04_08",       [40, 46, 48],        pygame.Rect(center2_x + 7 * step,  center2_y - 1 * step,  map_size, map_size)],
        [48, "pay_fild09",   "斐揚　區域9",                    2,     "pay_fild_06_07_09_10",          [47, 49],            pygame.Rect(center2_x + 8 * step,  center2_y - 1 * step,  map_size, map_size)],
        [49, "pay_fild10",   "斐揚　區域10",                   2,     "pay_fild_06_07_09_10",          [46, 48],            pygame.Rect(center2_x + 8 * step,  center2_y,             map_size, map_size)],
        [50, "payon",        "斐揚洞穴口",                     1,     "payon",                         [40],                pygame.Rect(center2_x + 6 * step,  center2_y - 2 * step,  map_size, map_size)],
        [51, "alberta",      "港口之都　艾爾貝塔",              1,     "alberta",                       [43],                pygame.Rect(center2_x + 8 * step,  center2_y + 1 * step,  map_size, map_size)],
        [52, "mjolnir_01",   "妙勒尼　山脈1",                  2,     "mjolnir_01_06_07_09",           [53],                pygame.Rect(center_x - 4 * step,   center_y - 3 * step,   map_size, map_size)],
        [53, "mjolnir_02",   "妙勒尼　山脈2",                  2,     "mjolnir_02_03_04_08",           [52, 54, 58],        pygame.Rect(center_x - 3 * step,   center_y - 3 * step,   map_size, map_size)],
        [54, "mjolnir_03",   "妙勒尼　山脈3",                  2,     "mjolnir_02_03_04_08",           [53, 58],            pygame.Rect(center_x - 2 * step,   center_y - 3 * step,   map_size, map_size)],
        [55, "mjolnir_04",   "妙勒尼　山脈4",                  2,     "mjolnir_02_03_04_08",           [54, 56, 59],        pygame.Rect(center_x - 1 * step,   center_y - 3 * step,   map_size, map_size)],
        [56, "mjolnir_05",   "妙勒尼　山脈5",                  2,     "mjolnir_05_10_11_12",           [55, 61, 63],        pygame.Rect(center_x,              center_y - 3 * step,   map_size, map_size)],
        [57, "mjolnir_06",   "妙勒尼　山脈6",                  2,     "mjolnir_01_06_07_09",           [15, 19, 53, 58],    pygame.Rect(center_x - 3 * step,   center_y - 2 * step,   map_size, map_size)],
        [58, "mjolnir_07",   "妙勒尼　山脈7",                  2,     "mjolnir_01_06_07_09",           [1, 53, 54, 57, 59], pygame.Rect(center_x - 2 * step,   center_y - 2 * step,   map_size, map_size)],
        [59, "mjolnir_08",   "妙勒尼　山脈8",                  2,     "mjolnir_02_03_04_08",           [55, 58, 60, 61],    pygame.Rect(center_x - 1 * step,   center_y - 2 * step,   map_size, map_size)],
        [60, "mjolnir_09",   "妙勒尼　山脈9",                  2,     "mjolnir_01_06_07_09",           [1, 2, 6, 59],       pygame.Rect(center_x - 1 * step,   center_y - 1 * step,   map_size, map_size)],
        [61, "mjolnir_10",   "妙勒尼　山脈10",                 2,     "mjolnir_05_10_11_12",           [2, 56, 59, 62],     pygame.Rect(center_x,              center_y - 2 * step,   map_size, map_size)],
        [62, "mjolnir_11",   "妙勒尼　山脈11",                 2,     "mjolnir_05_10_11_12",           [3, 61],             pygame.Rect(center_x + 1 * step,   center_y - 2 * step,   map_size, map_size)],
        [63, "mjolnir_12",   "妙勒尼　山脈12",                 2,     "mjolnir_05_10_11_12",           [56, 64],            pygame.Rect(center_x,              center_y - 4 * step,   map_size, map_size)],
        [64, "aldebaran",    "運河之都　艾爾帕蘭",              1,     "aldebaran",                     [63],                pygame.Rect(center_x,              center_y - 5 * step,   map_size, map_size)]
    ]


if __name__ == "__main__":
    print(len(map_data))
