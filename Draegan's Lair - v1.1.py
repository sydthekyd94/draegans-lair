# #       # # #      # # #    # # # #   # # # #    # # #    #    #   ##   # # # #
#    #    #    #    #     #   #         #         #     #   # #  #    #   #
#    #    # # #     # # # #   # # # #   #   # #   # # # #   #  # #        # # # #
#    #    #    #    #     #   #         #     #   #     #   #   ##              #
# #       #     #   #     #   # # # #   # # # #   #     #   #    #        # # # #

#         # # #     # # # #   # # #
#        #     #       #      #    #
#        # # # #       #      # # #
#        #     #       #      #    #
# # #    #     #    # # # #   #     #

# Draegan's Lair
# A Python Game by SydtheKyd

import os
import numpy
import msvcrt
import random
import copy

no_quotes = {39: None}

run = True
menu = True
play = False
rules = False
key = False
fight = False
sneak_attack = False
# hero_attack = False
enemy_attack = False
standing = True
buy = False
speak = False
boss = False
gate = False
inn = False

name = "Hero"
HP = 50
HPMAX = 50  # Should = starting HP
ATK = 30  # Should be 3
POT = 1  # 30HP
ELX = 0  # 50 HP
GOLD = 100  # 0 Gold standard
x = 0
y = 0
area_x = 4
area_y = 4
enemy_col = 100
enemy_row = 100
dest = "und"
enemy_dest = "und"
os.system("mode con cols=100 lines=50")  # width determined by cols and length determined by lines

# list of types of random encounter enemies
part1_ez_elist = ["Goblin", "Slime"]
part1_med_elist = ["Goblin", "Orc", "Slime"]
part1_hard_elist = ["Orc", "Troll", "Slime"]

part2_ez_elist = ["Troll", "Giant Spider"]
part2_med_elist = ["Troll", "Centaur", "Giant Spider"]
part2_hard_elist = ["Centaur", "Wyrm", "Giant Spider"]

mobs = {
    "Goblin": {
        "hp": 15,  # How much health
        "at": 3,  # Attack damage
        "go": 4},  # Gold gained from kill
    "Orc": {
        "hp": 35,  # How much health
        "at": 5,  # Attack damage
        "go": 9},  # Gold gained from kill
    "Slime": {
        "hp": 30,  # How much health
        "at": 2,  # Attack damage
        "go": 6},  # Gold gained from kill - 6 normally
    "Troll": {  # Goblin type of zone 2 / Troll type of zone 1
        "hp": 40,
        "at": 6,
        "go": 10},
    "Centaur": {  # Orc type of zone 2
        "hp": 90,
        "at": 9,
        "go": 16},
    "Giant Spider": {  # Slime type of zone 2
        "hp": 80,
        "at": 4,
        "go": 13},
    "Wyrm": {  # Troll type of zone 2
        "hp": 100,
        "at": 12,
        "go": 20},
    "Blackwood": {  # 1st BBEG
        "hp": 100,
        "at": 8,  # 8 normally
        "go": 25},
    "Draegan": {  # 2nd BBEG
        "hp": 200,
        "at": 16,
        "go": 50}
}

#         x = 0     1     2     3     4
game_map = [["1", "2", "3", "X", "X"],  # y = 0
            ["X", "4", "X", "X", "X"],  # y = 1
            ["6", "5", "X", "X", "X"],  # y = 2
            ["7", "X", "X", "X", "X"],  # y = 3
            ["8", "11", "12", "13", "14"],  # y = 4
            ["9", "X", "X", "X", "X"],  # y = 5
            ["10", "X", "X", "X", "X"]]  # y = 6
# safe spaces = 2, 7, 8 (2 and 8 are towns) / 6 and 14 are bosses
y_len = len(game_map) - 1
x_len = len(game_map[0]) - 1

area_1_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'e', 'e', 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X']]

area_2_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 'I', 'I', 1, 1, 1, 'X', 'X', 1, 1, 1, 1, 'X', 'X'],
              ['X', 'X', 1, 1, 1, 'I', 'I', 1, 'M', 1, 'X', 'X', 1, 1, 1, 1, 1, 'X'],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              ['X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 'X', 'X', 1, 1, 'X', 'X', 1, 'S', 'S', 1, 1, 1, 'X', 'X'],
              ['P', 'X', 1, 1, 'X', 'X', 1, 1, 'X', 'X', 1, 'S', 'S', 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

area_3_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'e', 'e', 'e', 1, 1, 1, 'X', 'X'],
              ['X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'e', 'X', 'e', 1, 1, 1, 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'e', 'e', 'e', 1, 1, 1, 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X']]

area_4_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 'X', 1, 1, 'e', 1, 1, 'X', 1, 1, 'e', 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 'X', 1, 1, 'X', 1, 1, 'X', 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 'e', 1, 1, 1, 'e', 1, 'X', 1, 1, 'X', 1, 1, 'X', 'X'],
              ['P', 'X', 1, 'e', 1, 1, 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 'X', 1, 1, 'X', 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

area_5_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 'e', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['X', 'X', 1, 1, 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              [1, 'G', 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'e', 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 1, 'e', 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 'e', 1, 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 'e', 1, 1, 'X', 'X', 'X', 1, 'e', 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 'e', 1, 1, 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X']]

area_6_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'X', 'X', 'X', 'X', 1, 1, 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'X', 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 'X'],
              ['P', 'X', 1, 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 'X'],
              ['P', 'X', 1, 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 1],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 'B', 'B', 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 'B', 'B', 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 'X', 'X', 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 'X', 'X', 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 'X', 'X', 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'G', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
               'X']]

area_6_copy = copy.deepcopy(area_6_map)

area_7_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

area_8_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 'M', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'I', 'I', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              ['P', 'X', 1, 'I', 'I', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'S', 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 1, 'S', 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

area_9_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 1, 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'e', 1, 'e', 1, 1, 'X'],
              ['P', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
              ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

area_10_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'e', 'e', 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 'e', 1, 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 'e', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 'e', 'e', 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 'e', 'e', 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'e', 'e', 1, 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X']]

area_11_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 'e', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 'X', 1, 1, 1, 'X', 'X', 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 1, 'X', 1, 1, 1, 'X'],
               ['P', 'X', 1, 'e', 'X', 1, 'e', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 'X', 1, 1, 'X', 1, 'e', 1, 1, 1, 'X'],
               ['X', 'X', 1, 'e', 1, 'X', 1, 1, 1, 1, 'X', 'X', 'X', 1, 1, 1, 1, 'X'],
               [1, 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 'X', 1, 1, 1, 1, 1, 1],
               ['X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'e', 1, 'X'],
               ['P', 'X', 1, 'X', 1, 1, 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 'X'],
               ['P', 'X', 1, 1, 'e', 'X', 'X', 'X', 1, 'X', 1, 1, 1, 1, 1, 1, 1, 'X'],
               ['P', 'X', 'X', 1, 1, 1, 'X', 1, 1, 1, 'e', 1, 1, 'X', 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 'e', 1, 'X', 'X', 1, 1, 1, 'e', 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X']]

area_12_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 1, 'X', 1, 1, 'X', 1, 1, 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 'e', 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 1, 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 1, 'e', 1, 1, 1, 'X', 1, 'e', 1, 'X', 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 1, 1, 1, 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['X', 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 'X', 1, 1, 'e', 1, 1, 'X', 'X'],
               [1, 1, 1, 1, 'e', 1, 1, 'X', 1, 1, 1, 1, 1, 1, 'X', 1, 1, 1],
               ['X', 'X', 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 'X', 1, 1, 1, 1, 'X'],
               ['P', 'X', 1, 1, 'X', 1, 1, 'e', 1, 1, 1, 'e', 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 1, 1, 1, 'e', 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 'X', 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 'X', 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X']]

area_13_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 'e', 1, 1, 1, 1, 'e', 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 1, 1, 1, 'e', 1, 1, 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 'e', 1, 1, 'X'],
               ['X', 'X', 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'e', 'X'],
               [1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 'G'],
               ['X', 'X', 1, 1, 1, 'e', 1, 'X', 'X', 'X', 'X', 'X', 'X', 1, 'e', 1, 1, 'X'],
               ['P', 'X', 1, 'e', 1, 1, 1, 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'e', 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 'e', 1, 1, 'e', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 'e', 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 'e', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X']]

area_14_map = [['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 'B', 'B', 'B', 1, 1, 1, 1, 1, 'X', 'X'],
               ['X', 'X', 1, 1, 1, 1, 1, 1, 'B', 'B', 'B', 1, 1, 1, 1, 1, 'X', 'X'],
               [1, 1, 1, 1, 1, 1, 1, 1, 'B', 'B', 'B', 1, 1, 1, 1, 1, 'X', 'X'],
               ['X', 'X', 1, 1, 1, 1, 1, 1, 'B', 'B', 'B', 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X'],
               ['P', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 1, 1, 1, 1, 1, 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
               ['P', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                'X']]

area_14_copy = copy.deepcopy(area_14_map)

biome = {
    "X": {  # Inaccessible areas
        "t": "ERROR",
        "e": False,
        "n": True,  # if new to zone
        "s": "You shouldn't be here..."},  # text to display if new
    "1": {  # starting zone
        "m": area_1_map,  # Map of Area
        "t": "PLAINS",  # Name of the Zone
        "e": True,
        "n": True,
        "s": "Something is moving around in the dark..."},  # Flag if mobs can spawn in the area or not
    "2": {  # First town
        "m": area_2_map,
        "t": "TOWN OF EASTHALLOW",
        "e": False,
        "n": True,
        "s": "The town seems mostly abandoned. A man calls you over!"},
    "3": {  # Side zone 1
        "m": area_3_map,
        "t": "MONSTER CAVE",
        "e": True,
        "n": True,
        "s": "Towards the back of the cave you see a firepit surrounded by monsters!"},
    "4": {  # Main Quest Area 1
        "m": area_4_map,
        "t": "WOODS",
        "e": True,
        "n": True,
        "s": "From behind the trees, you see bright eyes looking at you..."},
    "5": {  # Main Quest Area 2
        "m": area_5_map,
        "t": "SECRET TRAIL",
        "e": True,
        "n": True,
        "s": "The ground beneath your feet smells toxic and the rocks are slimy."},
    "6": {  # Town 1 BBEG
        "m": area_6_map,
        "t": "BLACKWOOD'S LAB",
        "e": True,
        "n": True,
        "s": "The lab is full of monsters in test tubes, and a large creature in a lab coat roars at you!"},
    "7": {  # Safe zone route to Town 2
        "m": area_7_map,
        "t": "UNDERGROUND TUNNEL",
        "e": False,
        "n": True,
        "s": "The path under the sewer grate seems quiet and safe."},
    "8": {  # Town 2
        "m": area_8_map,
        "t": "TOWN OF ARMAGH",
        "e": False,
        "n": True,
        "s": "This town seems even more abandoned than the last. A man with a pitchfork calls you over."},
    "9": {  # Side zone 2
        "m": area_9_map,
        "t": "HILLS",
        "e": True,
        "n": True,
        "s": "Spiderwebs cover the grass of these hills..."},
    "10": {  # Side zone 2 cont.
        "m": area_10_map,
        "t": "HILLS",
        "e": True,
        "n": True,
        "s": "A large pack of monsters is approaching the town!"},
    "11": {  # Main Quest Area 3
        "m": area_11_map,
        "t": "WOODS",
        "e": True,
        "n": True,
        "s": "The trees of this forest are older, taller, and the woods seem darker..."},
    "12": {  # Main Quest Area 4
        "m": area_12_map,
        "t": "WOODS",
        "e": True,
        "n": True,
        "s": "You hear strange screeching sounds in the distance"},
    "13": {  # Main Quest Area 5
        "m": area_13_map,
        "t": "MARSH",
        "e": True,
        "n": True,
        "s": "Across from you is a watery marsh and more strange monsters are approaching!"},
    "14": {  # Final BBEG
        "m": area_14_map,
        "t": "DRAEGAN'S LAIR",
        "e": True,
        "n": True,
        "s": "This is the lair of the beast... Draegan."}
}
biome_BU = copy.deepcopy(biome)

micro_biome = {
    "X": "Inaccessible",
    0: "Hero",
    1: "Free Space",
    'e': "Enemy",
    "M": "Mayor",
    "S": "Shop",
    "B": "Boss",
    "G": "Gate",
    "I": "Inn",
    "P": "Padding"
}


def clear():
    if os.name in ("nt", 'dos'):
        os.system("cls")
    else:
        os.system('clear')


def draw():
    print('~' * 37)


def save():
    save_stats = [
        name,
        str(HP),
        str(HPMAX),
        str(ATK),
        str(POT),
        str(ELX),
        str(GOLD),
        str(x),
        str(y),
        str(area_x),
        str(area_y),
        str(key),
        str(area_1_map),
        str(area_2_map),
        str(area_3_map),
        str(area_4_map),
        str(area_5_map),
        str(area_6_map),
        str(area_7_map),
        str(area_8_map),
        str(area_9_map),
        str(area_10_map),
        str(area_11_map),
        str(area_12_map),
        str(area_13_map),
        str(area_14_map),
        str(biome)
    ]

    save_file = open("load.txt", "w")

    for item in save_stats:
        save_file.write(item + "\n")
    save_file.close()


def reset(reset_type):
    global area_6_copy, area_6_map, area_14_copy, area_14_map, formatted_map, biome, biome_BU, key, HP, HPMAX, \
        ATK, POT, ELX, GOLD, x, y, area_x, area_y, enemy_col, enemy_row, dest, enemy_dest, inn

    area_6_copy = copy.deepcopy(area_6_map)  # Creates a backup of the boss room
    area_14_copy = copy.deepcopy(area_14_map)  # Creates a backup of the boss room
    if reset_type == "soft":  # INN
        while inn:
            clear()
            draw()
            print(" Welcome to the Inn!")
            draw()
            print(" I hear that monsters come back overnight.")
            print(" If you need more monsters to kill, maybe getting some rest would be best!")
            print(" Also, any injuries you received fighting will be healed.")
            draw()
            print(" 1 - REST")
            print(" 2 - LEAVE")
            draw()

            inn_choice = msvcrt.getch().decode('ASCII').upper()

            if inn_choice == "1":
                biome = copy.deepcopy(biome_BU)
                area_6_map = copy.deepcopy(area_6_copy)
                area_14_map = copy.deepcopy(area_14_copy)
                biome = copy.deepcopy(biome)
                HP = HPMAX
                biome[game_map[y][x]]["m"][area_y][area_x] = "H"
                biome[game_map[y][x]]["n"] = False
                if game_map[y][x] == "8":
                    biome[game_map[3][0]]["m"][0][8] = 'X'
                    biome[game_map[3][0]]["n"] = True
                    biome[game_map[3][0]]["s"] = 'The tunnel has caved in!'
                draw()
                print(" You decide to get some sleep.")
                print("\n ... \n")
                print(" Is it morning already?")
                draw()
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
                inn = False
            elif inn_choice == "2":
                print(" Thanks for stopping by, traveler!")
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
                inn = False

    elif reset_type == "hard":  # New Game
        file_exists = os.path.exists("load.txt")
        if file_exists:
            biome[game_map[y][x]]["m"][area_y][area_x] = 1
            y = 0
            x = 0
            area_x = 4
            area_y = 4
            biome[game_map[y][x]]["m"][area_y][area_x] = "H"
        biome = copy.deepcopy(biome_BU)
        key = False  # Should be false
        HP = 50  # should be 50
        HPMAX = 50  # Should = starting HP
        ATK = 3  # Should be 3
        POT = 1  # 30HP should be 1
        ELX = 0  # 50 HP should be 0
        GOLD = 0  # 0 Gold standard
        enemy_col = 100
        enemy_row = 100
        dest = "und"
        enemy_dest = "und"


def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    print(name + "'s HP refilled to " + str(HP) + "!")
    if not fight:
        print("\n Press any key to continue")
        msvcrt.getch().decode('ASCII').upper()


def battle():
    global fight, play, run, menu, sneak_attack, enemy_attack, HP, POT, ELX, GOLD, boss, key, formatted_map, \
        enemy_row, enemy_col, x, y, area_x, area_y

    enemy = part1_ez_elist[1]
    if game_map[y][x] == "1":
        enemy = random.choice(part1_ez_elist)
    elif game_map[y][x] in ("3", "4"):
        enemy = random.choice(part1_med_elist)
    elif game_map[y][x] == "5":
        enemy = random.choice(part1_hard_elist)
    elif game_map[y][x] in ("9", "11"):
        enemy = random.choice(part2_ez_elist)
    elif game_map[y][x] in ("10", "12"):
        enemy = random.choice(part2_med_elist)
    elif game_map[y][x] == "13":
        enemy = random.choice(part2_hard_elist)
    elif game_map[y][x] == "6":
        enemy = "Blackwood"
    elif game_map[y][x] == "14":
        enemy = "Draegan"
    else:
        fight = False

    hp = mobs[enemy]["hp"]
    hpmax = mobs[enemy]["hp"]
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]

    while fight:
        clear()
        draw()
        if sneak_attack:
            if enemy[0] not in ("A", "E", "I", "O", "U"):
                print(" A {0} has snuck up on you!\n".format(enemy))
            else:
                print(" An {0} has snuck up on you!\n".format(enemy))
        elif enemy_attack:
            if game_map[y][x] not in ("6", "14"):
                if enemy[0] not in ("A", "E", "I", "O", "U"):
                    print(" A {0} rushes towards you in an attack!\n".format(enemy))
                else:
                    print(" An {0} rushes towards you in an attack!\n".format(enemy))
        elif game_map[y][x] == "6":
            print(" Blackwood lunges at you, spraying acid and bile everywhere!\n")
        elif game_map[y][x] == "14":
            print(" Draegan lets out a terrifying roar!!\n")
        draw()
        print(" {0}\'s HP: {1}/{2}".format(name, str(HP), str(HPMAX)))
        print(" {0}\'s HP: {1}/{2}".format(enemy, str(hp), str(hpmax)))
        print(" POTIONS: {0} ~ ELIXIRS: {1}".format(str(POT), str(ELX)))
        draw()
        print(formatted_map.translate(no_quotes))
        draw()
        if HP > 5:
            print(" Q - ATTACK")
        elif HP <= 5:
            print(" Q - ATTACK  [LOW HEALTH WARNING!]")
        if POT > 0:
            print(" 1 - USE POTION (30 HP)")
        elif POT == 0:
            print("")
        if ELX > 0:
            print(" 2 - USE ELIXIR (50 HP)")
        elif ELX == 0:
            print("")
        draw()

        battle_choice = msvcrt.getch().decode('ASCII').upper()

        if battle_choice == "Q":  # Attack!
            hp -= ATK
            print(" {0} dealt {1} damage to the {2}.".format(name, str(ATK), enemy))
            if hp > 0:
                HP -= atk
                print(" {0} dealt {1} damage to {2}.".format(enemy, str(atk), name))
            print("\n Press any key to continue")
            msvcrt.getch().decode('ASCII').upper()
        elif battle_choice == "1":  # Use Potion
            if POT > 0:
                POT -= 1
                heal(30)
                HP -= atk
                print(" {0} dealt {1} damage to {2}.".format(enemy, str(atk), name))
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
            else:
                print(" No potions!")
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()

        elif battle_choice == "2":  # Use Elixir
            if ELX > 0:
                ELX -= 1
                heal(50)
                HP -= atk
                print(" {0} dealt {1} damage to {2}.".format(enemy, str(atk), name))
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
            else:
                print(" No Elixirs!")
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()

        if HP <= 0:
            print("\n {0} defeated {1}....".format(enemy, name))
            draw()
            if game_map[y][x] == "1":
                fight = False
                play = False
                run = False
                print(" GAME OVER")
                print("\n Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
            elif game_map[y][x] in ("3", "4", "5", "6"):
                if game_map[y][x] == "6":
                    biome[game_map[2][1]]["m"][8][1] = 'G'
                    formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                    formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                        replace('1', ' ').replace('P', ' ').replace('X', '░')
                boss = False
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                x = 1
                y = 0
                area_x = 5
                area_y = 8
                biome[game_map[y][x]]["m"][area_y][area_x] = "H"
                formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                    replace('1', ' ').replace('P', ' ').replace('X', '░')
                reset("soft")
                print(" You see a white light and pass out...")
                print("\n Press enter to continue")
                input().upper()
                clear()
                print(" You wake up in the inn with the Mayor staring down at you...")
                print("\n")
                print(" Don't scare me like that! I thought you were dead! Here, take this - you might need it later")
                POT += 1
                if GOLD >= 15:
                    GOLD -= 15
                else:
                    GOLD = 0
                HP = 1
                draw()
                print("\n\n")
                print(" The Mayor gave you a health potion!")
                print("\n")
                print(" Your pockets feel lighter ...")
                draw()
                print("\n Press enter to continue")
                input().upper()
                clear()
                fight = False
            elif game_map[y][x] in ("9", "10", "11", "12", "13", "14"):
                if game_map[y][x] == "14":
                    biome[game_map[y][x-1]]["m"][8][17] = 'G'
                    formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                    formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                        replace('1', ' ').replace('P', ' ').replace('X', '░')
                boss = False
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                x = 0
                y = 4
                area_x = 5
                area_y = 8
                biome[game_map[y][x]]["m"][area_y][area_x] = "H"
                formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                    replace('1', ' ').replace('P', ' ').replace('X', '░')
                reset("soft")
                print(" You see a white light and pass out...")
                print("\n Press enter to continue")
                input().upper()
                clear()
                print(" You wake up in the inn with the Mayor staring down at you...")
                print("\n")
                print(" Don't scare me like that! I thought you were dead! Here, take this - you might need it later")
                POT += 1
                if GOLD >= 30:
                    GOLD -= 30
                else:
                    GOLD = 0
                HP = 1
                draw()
                print("\n\n")
                print(" The Mayor gave you a health potion!")
                print("\n")
                print(" Your pockets feel lighter ...")
                draw()
                print("\n Press enter to continue")
                input().upper()
                clear()
                fight = False

        if hp <= 0:
            if not sneak_attack:
                biome[game_map[y][x]]["m"][enemy_row][enemy_col] = 1
            if enemy not in ("Blackwood", "Draegan"):
                print("\n {0} defeated the {1}!".format(name, enemy))
            elif enemy == "Blackwood":
                print("\n Blackwood explodes in a shower of strange ooze!")
            elif enemy == "Draegan":
                print(" Draegan lets out one final roar then collapses!")
            draw()
            fight = False
            GOLD += g
            print(" You\'ve found {0} gold!".format(str(g)))
            if random.randint(0, 100) < 30:
                POT += 1
                print(" You've found a potion!")
            if random.randint(0, 100) < 10:
                ELX += 1
                print(" You've found an elixir!")
            if boss:
                if game_map[y][x] == "14":
                    for boss_row in biome[game_map[y][x]]["m"]:
                        b_row = biome[game_map[y][x]]["m"].index(boss_row)
                        for boss_col in biome[game_map[y][x]]["m"][b_row]:
                            b_col = biome[game_map[y][x]]["m"][b_row].index(boss_col)
                            if biome[game_map[y][x]]["m"][b_row][b_col] in ("B", "G"):
                                biome[game_map[y][x]]["m"][b_row][b_col] = 1
                    formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                    formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                        replace('1', ' ').replace('P', ' ').replace('X', '░')
                    draw()
                    print(" Congratulations, you've finished the game!")
                    biome[game_map[y][x]]["n"] = True
                    biome[game_map[y][x]]["s"] = 'Draegan has been vanquished!'
                    key = False
                    boss = False
                    play = False
                    menu = True
                    save()
                else:
                    for boss_row in biome[game_map[y][x]]["m"]:
                        b_row = biome[game_map[y][x]]["m"].index(boss_row)
                        for boss_col in biome[game_map[y][x]]["m"][b_row]:
                            b_col = biome[game_map[y][x]]["m"][b_row].index(boss_col)
                            if biome[game_map[y][x]]["m"][b_row][b_col] in ("B", "G"):
                                biome[game_map[y][x]]["m"][b_row][b_col] = 1
                    biome[game_map[2][0]]["m"][8][17] = 'X'
                    biome[game_map[y][x]]["n"] = True
                    biome[game_map[y][x]]["s"] = "The way you came is now blocked, but there is a mysterious grate"
                    formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                    formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', ''). \
                        replace('1', ' ').replace('P', ' ').replace('X', '░')
                    draw()
                    print("\n You defeated the boss!")
                    key = False
                    boss = False
            print("\n Press any key to continue")
            msvcrt.getch().decode('ASCII').upper()
            clear()
            enemy_col = 100
            enemy_row = 100
            sneak_attack = False
            enemy_attack = False


def shop():
    global buy, GOLD, POT, ELX, ATK

    while buy:  # Show the shop!
        clear()
        draw()
        print(" Welcome to the Shop!")
        draw()
        print(" GOLD: " + str(GOLD))
        print(" POTIONS: " + str(POT))
        print(" ELIXIRS: " + str(ELX))
        print(" ATK: " + str(ATK))
        draw()
        if game_map[y][x] == "2":
            print(" 1 - BUY POTION (30 HP) - 5 GOLD")
            print(" 2 - BUY ELIXIR (50 HP) - 8 GOLD")
            print(" 3 - UPGRADE WEAPON (+2 ATK) - 10 GOLD")
            print(" 4 - LEAVE")
        elif game_map[y][x] == "8":
            print(" 1 - BUY POTION (30 HP) - 15 GOLD")
            print(" 2 - BUY ELIXIR (50 HP) - 24 GOLD")
            print(" 3 - UPGRADE WEAPON (+2 ATK) - 30 GOLD")
            print(" 4 - LEAVE")
        draw()

        shop_choice = msvcrt.getch().decode('ASCII').upper()

        if shop_choice == "1":
            if game_map[y][x] == "2":
                if GOLD >= 5:
                    POT += 1
                    GOLD -= 5
                    print(" The shopkeeper hands you a potion!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
            elif game_map[y][x] == "8":
                if GOLD >= 15:
                    POT += 1
                    GOLD -= 15
                    print(" The shopkeeper hands you a potion!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
        elif shop_choice == "2":
            if game_map[y][x] == "2":
                if GOLD >= 8:
                    ELX += 1
                    GOLD -= 8
                    print(" The shopkeeper hands you an elixir!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
            elif game_map[y][x] == "8":
                if GOLD >= 24:
                    ELX += 1
                    GOLD -= 24
                    print(" The shopkeeper hands you an elixir!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
        elif shop_choice == "3":
            if game_map[y][x] == "2":
                if GOLD >= 10:
                    ATK += 2
                    GOLD -= 10
                    print(" The shopkeeper hands you your weapon!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
            elif game_map[y][x] == "8":
                if GOLD >= 30:
                    ATK += 2
                    GOLD -= 30
                    print(" The shopkeeper hands you your weapon!")
                    print("\n Press any key to pay the shopkeeper")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" You can't afford that!")
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
        elif shop_choice == "4":
            print(" Thanks for shopping!")
            print("\n Press any key to continue")
            msvcrt.getch().decode('ASCII').upper()
            buy = False


def mayor():
    global speak, key
    while speak:
        clear()
        draw()
        print(" Hello there, " + name + "!")
        draw()
        if not key:
            if game_map[y][x] == "2":
                if biome[game_map[y][x]]["n"]:
                    print(" I'm glad you made it past those monsters out there, we need your help!")
                    print(" To the south, an evil man is creating monsters in a Lab.")
                    print(" ... ")
                    print(" Blackwood!")
                    draw()
                    print(" Why don't you kill the monsters in the cave to the East...")
                    print(" Then when you are strong enough, come back to me.")
                    draw()

                if ATK < 10:
                    print(" You're not strong enough to face Blackwood yet!")
                    print(" Keep practicing and come back later.")
                    key = False
                else:
                    print(" You are strong enough to take on Blackwood now!")
                    print(" Take this key but be careful!")
                    key = True
            if game_map[y][x] == '8':
                if biome[game_map[y][x]]["n"]:
                    print(" You were able to take down the evil Blackwood? We need someone like you!")
                    print(" To the east there is an ancient beast")
                    print(" ... ")
                    print(" Draegan!")
                    draw()
                    print(" Why don't you kill the monsters in the hills to the South...")
                    print(" Then when you are strong enough, come back to me.")
                    draw()

                if ATK < 50:
                    print(" You're not strong enough to face Draegan yet!")
                    print(" Keep practicing and come back later.")
                    key = False
                else:
                    print(" You are strong enough to take on Draegan now!")
                    print(" Take this key but be careful.")
                    key = True

            draw()
            if (game_map[y][x] == "2" and ATK >= 10) or (game_map[y][x] == "8" and ATK >= 50):
                print(" 1 - Take Key and leave")
            else:
                print(" 1 - Leave")
            draw()

        elif key:
            if game_map[y][x] == "2":
                print(" I already gave you the key - go defeat Blackwood!")
            elif game_map[y][x] == "8":
                print(" I already gave you the key - go defeat Draegan!")
            draw()
            print(" 1 - Leave")

        mayor_choice = msvcrt.getch().decode('ASCII').upper()

        if mayor_choice == "1":
            speak = False


def at_gate():
    global gate, key, formatted_map

    while gate:
        clear()
        draw()
        if game_map[y][x] == '5':
            print(" It's the door to Blackwood's Lab, what will you do?")
        elif game_map[y][x] == '13':
            print(" You are at the entrance to Draegan's Lair, what will you do?")
        elif game_map[y][x] == '6':
            print(" The door is locked!")
        draw()

        if key:
            print(" 1 - USE KEY")
        print(" 2 - TURN BACK")
        draw()

        gate_choice = msvcrt.getch().decode('ASCII').upper()

        if gate_choice == "1":
            if key:
                for gate_row in biome[game_map[y][x]]["m"]:
                    g_row = biome[game_map[y][x]]["m"].index(gate_row)
                    for gate_col in biome[game_map[y][x]]["m"][g_row]:
                        g_col = biome[game_map[y][x]]["m"][g_row].index(gate_col)
                        if biome[game_map[y][x]]["m"][g_row][g_col] == "G":
                            biome[game_map[y][x]]["m"][g_row][g_col] = 1
            print(" The gate is now open but the key turns to dust!")
            print("\n Press any key to continue")
            msvcrt.getch().decode('ASCII').upper()
            gate = False
            key = False
        if gate_choice == "2":
            gate = False
        formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
        formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', '').replace('1', ' ') \
            .replace('P', ' ').replace('X', '░')


def boss_fight():
    global boss, fight, key
    key = False

    while boss:
        if HP > 0:
            fight = True
            battle()
        else:
            quit()


def movement(move, tile):
    global x, y, area_x, area_y, standing, enemy_col, enemy_row

    if move == "W":  # North
        # Moving North in Area to free space
        if (tile == "Hero" and area_y != 0) or (tile == "Enemy" and enemy_row != 0):
            if tile == "Hero" and biome[game_map[y][x]]["m"][area_y - 1][area_x] == 1:
                biome[game_map[y][x]]["m"][area_y - 1][area_x] = "H"
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                area_y -= 1
            elif tile == "Enemy" and biome[game_map[y][x]]["m"][enemy_row - 1][enemy_col] == 1:
                biome[game_map[y][x]]["m"][enemy_row - 1][enemy_col] = "e"
                biome[game_map[y][x]]["m"][enemy_row][enemy_col] = 1
                enemy_row -= 1
        elif area_y == 0 and tile == "Hero":  # Moving North to new Area
            biome[game_map[y][x]]["m"][area_y][area_x] = 1
            biome[game_map[y][x]]["n"] = False
            y -= 1
            area_y = len(biome[game_map[y][x]]["m"]) - 1
            biome[game_map[y][x]]["m"][area_y][area_x] = "H"
            standing = True
    elif move == "D":  # East
        # Moving East in Area to free space
        if (tile == "Hero" and area_x != (len(biome[game_map[y][x]]["m"][0]) - 1)) or \
                (tile == "Enemy" and enemy_col != (len(biome[game_map[y][x]]["m"][0]) - 1)):
            if tile == "Hero" and biome[game_map[y][x]]["m"][area_y][area_x + 1] == 1:
                biome[game_map[y][x]]["m"][area_y][area_x + 1] = "H"
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                area_x += 1
            elif tile == "Enemy" and biome[game_map[y][x]]["m"][enemy_row][enemy_col + 1] == 1:
                biome[game_map[y][x]]["m"][enemy_row][enemy_col + 1] = "e"
                biome[game_map[y][x]]["m"][enemy_row][enemy_col] = 1
                enemy_col += 1
        elif area_x == (len(biome[game_map[y][x]]["m"][0]) - 1) and tile == "Hero":  # Moving East to new Area
            biome[game_map[y][x]]["m"][area_y][area_x] = 1
            biome[game_map[y][x]]["n"] = False
            x += 1
            area_x = 0
            biome[game_map[y][x]]["m"][area_y][area_x] = "H"
            standing = True
    elif move == "S":  # South
        # Moving South in Area to free space
        if (tile == "Hero" and area_y != len(biome[game_map[y][x]]["m"]) - 1) or \
                (tile == "Enemy" and enemy_row != len(biome[game_map[y][x]]["m"]) - 1):
            if tile == "Hero" and biome[game_map[y][x]]["m"][area_y + 1][area_x] == 1:
                biome[game_map[y][x]]["m"][area_y + 1][area_x] = "H"
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                area_y += 1
            elif tile == "Enemy" and biome[game_map[y][x]]["m"][enemy_row + 1][enemy_col] == 1:
                biome[game_map[y][x]]["m"][enemy_row + 1][enemy_col] = "e"
                biome[game_map[y][x]]["m"][enemy_row][enemy_col] = 1
                enemy_row += 1
        elif area_y == len(biome[game_map[y][x]]["m"]) - 1 and tile == "Hero":  # Moving South to new Area
            biome[game_map[y][x]]["m"][area_y][area_x] = 1
            biome[game_map[y][x]]["n"] = False
            y += 1
            area_y = 0
            biome[game_map[y][x]]["m"][area_y][area_x] = "H"
            standing = True
            if game_map[y][x] == "8":
                biome[game_map[3][0]]["m"][0][8] = 'X'
                biome[game_map[3][0]]["n"] = True
                biome[game_map[3][0]]["s"] = 'The tunnel has caved in!'
    elif move == "A":
        # Moving West in Area to free space
        if (tile == "Hero" and area_x != 0) or (tile == "Enemy" and enemy_col != 0):
            if tile == "Hero" and biome[game_map[y][x]]["m"][area_y][area_x - 1] == 1:
                biome[game_map[y][x]]["m"][area_y][area_x - 1] = "H"
                biome[game_map[y][x]]["m"][area_y][area_x] = 1
                area_x -= 1
            elif tile == "Enemy" and biome[game_map[y][x]]["m"][enemy_row][enemy_col - 1] == 1:
                biome[game_map[y][x]]["m"][enemy_row][enemy_col - 1] = "e"
                biome[game_map[y][x]]["m"][enemy_row][enemy_col] = 1
                enemy_col -= 1
        elif area_x == 0 and tile == "Hero":  # Moving West to new Area
            biome[game_map[y][x]]["m"][area_y][area_x] = 1
            biome[game_map[y][x]]["n"] = False
            x -= 1
            area_x = (len(biome[game_map[y][x]]["m"][0]) - 1)
            biome[game_map[y][x]]["m"][area_y][area_x] = "H"
            standing = True


while run:
    while menu:
        clear()
        print("\n\n    ░░░░░     ░░░░░░   ░░░░░░   ░░░░░░   ░░░░░░   ░░░░░░   ░    ░   ░░   ░░░░░░  \
         \n    ░     ░   ░    ░   ░    ░   ░        ░        ░    ░   ░░   ░    ░   ░       \
         \n    ░     ░   ░ ░░     ░░░░░░   ░░░░░    ░  ░░    ░░░░░░   ░ ░  ░        ░░░░░░  \
         \n    ░     ░   ░   ░    ░    ░   ░        ░    ░   ░    ░   ░  ░ ░             ░  \
         \n    ░░░░░     ░    ░   ░    ░   ░░░░░░   ░░░░░    ░    ░   ░   ░░        ░░░░░░  \n\n")

        print("\n\n                      ░         ░░░░░░   ░░░░░░   ░░░░░░                         \
         \n                      ░         ░    ░     ░░     ░    ░                         \
         \n                      ░         ░░░░░░     ░░     ░ ░░                           \
         \n                      ░         ░    ░     ░░     ░   ░                          \
         \n                      ░░░░░░    ░    ░   ░░░░░░   ░    ░                         \n\n")
        print('~' * 81)
        print("")
        print("                              1: NEW GAME")
        print("                              2: LOAD GAME")
        print("                              3: RULES / CONTROLS")
        print("                              4: QUIT GAME")
        print("")
        print('~' * 81)

        if rules:
            clear()
            draw()
            print(" Press WASD to move")
            print(" Press 0 while in game to save and return to main menu")
            print("")
            print(" On the map:")
            print(" H represents you, the hero!")
            print(" e represents an enemy to fight")
            print(" G represents a locked gate")
            print(" B represents a boss!")
            print("")
            print(" While in town:")
            print(" M represents The Mayor")
            print(" S represents The Shop")
            print(" I represents The Inn")
            print(" To interact with things in town, press 3 when you are near.")
            draw()
            print("\n Press any key to return to main menu")
            rules = False
            choice = ""
            msvcrt.getch().decode('ASCII').upper()
        else:
            choice = msvcrt.getch().decode('ASCII').upper()

        if choice == "1":  # New Game
            clear()
            existing_game = os.path.exists("load.txt")
            if existing_game:
                print(" Are you sure? This will reset all progress! [Y / N] ")
                new_game_choice = msvcrt.getch().decode('ASCII').upper()
                if new_game_choice == "Y":
                    reset("hard")
                    biome[game_map[y][x]]["m"][area_y][area_x] = "H"
                    draw()
                    print(" What's your name, hero?")
                    draw()
                    name = input("> ")
                    menu = False
                    play = True
                elif new_game_choice == "N":
                    choice = ""
                    print("\n Press any key to return to main menu")
                    msvcrt.getch().decode('ASCII').upper()
                else:
                    print(" Invalid Input, please type 'Y' or 'N'")
                    input("\n Returning to Main Menu... ")
            else:
                reset("hard")
                biome[game_map[y][x]]["m"][area_y][area_x] = "H"
                draw()
                print(" What's your name, hero?")
                draw()
                name = input("> ")
                menu = False
                play = True

        elif choice == "2":  # Load Game
            try:
                load_file = open("load.txt", "r")
                load_list = load_file.readlines()
                if len(load_list) == 27:
                    name = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    HPMAX = int(load_list[2][:-1])
                    ATK = int(load_list[3][:-1])
                    POT = int(load_list[4][:-1])
                    ELX = int(load_list[5][:-1])
                    GOLD = int(load_list[6][:-1])
                    x = int(load_list[7][:-1])
                    y = int(load_list[8][:-1])
                    area_x = int(load_list[9][:-1])
                    area_y = int(load_list[10][:-1])
                    key = bool(load_list[11][:-1])
                    area_1_map = list(load_list[12][:-1])
                    area_2_map = list(load_list[13][:-1])
                    area_3_map = list(load_list[14][:-1])
                    area_4_map = list(load_list[15][:-1])
                    area_5_map = list(load_list[16][:-1])
                    area_6_map = list(load_list[17][:-1])
                    area_7_map = list(load_list[18][:-1])
                    area_8_map = list(load_list[19][:-1])
                    area_9_map = list(load_list[20][:-1])
                    area_10_map = list(load_list[21][:-1])
                    area_11_map = list(load_list[22][:-1])
                    area_12_map = list(load_list[23][:-1])
                    area_13_map = list(load_list[24][:-1])
                    area_14_map = list(load_list[25][:-1])
                    biome = eval(load_list[26][:-1])
                    biome[game_map[y][x]]["m"][area_y][area_x] = "H"  # Setting Hero Position
                    load_file.close()
                    clear()
                    draw()
                    print(" Welcome back, " + name + "!")
                    print(" HP: {0}/{1} ~ ATK: {2}".format(str(HP), str(HPMAX), str(ATK)))
                    print(" LOCATION: {0}".format(biome[game_map[y][x]]["t"]))
                    draw()
                    print("\n Press any key to continue")
                    msvcrt.getch().decode('ASCII').upper()
                    menu = False
                    play = True
                else:
                    print(" Corrupt save file! Press any key to continue.")
                    msvcrt.getch().decode('ASCII').upper()
            except OSError:
                print(" No loadable save file! Press any key to continue")
                msvcrt.getch().decode('ASCII').upper()
        elif choice == "3":  # Rules / Controls
            rules = True
        elif choice == "4":  # Quit Game
            quit()

    while play:
        save()  # autosave
        clear()

        if not standing:
            if biome[game_map[y][x]]["e"]:
                if random.randint(1, 100) <= 3 and game_map[y][x] not in ("1", "6", "14"):  # sneak attack 3% chance
                    fight = True
                    sneak_attack = True
                    enemy_attack = False
                    battle()
            if (area_y - 1) >= 0 and area_y + 1 <= len(biome[game_map[y][x]]["m"]) - 1 \
                    and (area_x + 1) <= len(biome[game_map[y][x]]["m"][0]) - 1 and (area_x - 1) >= 0:
                if ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "e") or
                        (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "e") or
                        (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "e") or
                        (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "e")):
                    formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
                    formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', '') \
                        .replace('1', ' ').replace('P', ' ').replace('X', '░')
                    if biome[game_map[y][x]]["m"][area_y + 1][area_x] == "e":
                        enemy_row = copy.copy(area_y) + 1
                        enemy_col = copy.copy(area_x)
                    elif biome[game_map[y][x]]["m"][area_y - 1][area_x] == "e":
                        enemy_row = copy.copy(area_y) - 1
                        enemy_col = copy.copy(area_x)
                    elif biome[game_map[y][x]]["m"][area_y][area_x + 1] == "e":
                        enemy_row = copy.copy(area_y)
                        enemy_col = copy.copy(area_x) + 1
                    elif biome[game_map[y][x]]["m"][area_y][area_x - 1] == "e":
                        enemy_row = copy.copy(area_y)
                        enemy_col = copy.copy(area_x) - 1
                    fight = True
                    sneak_attack = False
                    enemy_attack = True
                    battle()

            # Enemy movement on map
            enemy_row = 0
            enemy_col = 0
            for row_tile in biome[game_map[y][x]]["m"]:
                e_row = biome[game_map[y][x]]["m"].index(row_tile)
                for col_tile in biome[game_map[y][x]]["m"][e_row]:
                    e_col = biome[game_map[y][x]]["m"][e_row].index(col_tile)
                    if biome[game_map[y][x]]["m"][e_row][e_col] == "e" \
                            and enemy_row != e_row and enemy_col != e_col:
                        enemy_row = copy.copy(e_row)
                        enemy_col = copy.copy(e_col)
                        e_dest_int = random.randint(0, 4)
                        if e_dest_int == 1:
                            enemy_dest = "W"
                        elif e_dest_int == 2:
                            enemy_dest = "D"
                        elif e_dest_int == 3:
                            enemy_dest = "A"
                        elif e_dest_int == 4:
                            enemy_dest = "S"
                        else:  # Enemy doesn't move
                            enemy_dest = 0

                        if enemy_dest in ("W", "D", "A", "S"):
                            movement(enemy_dest, "Enemy")

        if play:
            draw()
            print(" LOCATION: {0}".format(biome[game_map[y][x]]["t"]))
            if biome[game_map[y][x]]["n"]:
                print(" " + biome[game_map[y][x]]["s"])
            draw()
            print(" NAME: {0} ~ HP: {1}/{2} ~ ATK: {3} ~ GOLD: {4}".format(name, str(HP),
                                                                           str(HPMAX), str(ATK), str(GOLD)))
            if POT > 0:
                print(" POTIONS: {0} ~ Press 1 to drink (30 HP)".format(str(POT)))
            else:
                print(" POTIONS: {0}".format(str(POT)))
            if ELX > 0:
                print(" ELIXIRS: {0} ~ Press 2 to drink (50 HP)".format(str(ELX)))
            else:
                print(" ELIXIRS: {0}".format(str(ELX)))
            if (area_y != 0 and area_x != 0 and area_y != len(biome[game_map[y][x]]["m"]) - 1 and
                    area_x != (len(biome[game_map[y][x]]["m"][0]) - 1)):
                if ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "M") or
                        (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "M") or
                        (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "M") or
                        (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "M")):
                    draw()
                    print(" 3 - TALK TO MAYOR")
                elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "S") or
                      (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "S") or
                      (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "S") or
                      (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "S")):
                    draw()
                    print(" 3 - ENTER SHOP")
                elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "I") or
                      (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "I") or
                      (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "I") or
                      (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "I")):
                    draw()
                    print(" 3 - ENTER THE INN")
                elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "G") or
                      (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "G") or
                      (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "G") or
                      (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "G")):
                    draw()
                    print(" 3 - INSPECT GATE")
                elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "B") or
                      (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "B") or
                      (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "B") or
                      (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "B")):
                    draw()
                    print(" 3 - ATTACK!")
            draw()
            formatted_map = str(numpy.array(biome[game_map[y][x]]["m"]))
            formatted_map = formatted_map.replace(' [', '').replace('[', '').replace(']', '').replace('1', ' ') \
                .replace('P', ' ').replace('X', '░')
            print(formatted_map.translate(no_quotes))
            draw()
            if y > 0 and game_map[y - 1][x] != "X":
                print(" NORTH: {0}".format(biome[game_map[y - 1][x]]["t"]))
            else:
                print("")
            if x < x_len and game_map[y][x + 1] != "X":
                print(" EAST: {0}".format(biome[game_map[y][x + 1]]["t"]))
            else:
                print("")
            if y < y_len and game_map[y + 1][x] != "X":
                print(" SOUTH: {0}".format(biome[game_map[y + 1][x]]["t"]))
            else:
                print("")
            if x > 0 and game_map[y][x - 1] != "X":
                print(" WEST: {0}".format(biome[game_map[y][x - 1]]["t"]))
            else:
                print("")
            draw()
            print(" 0 - SAVE AND RETURN TO MENU")

            dest = msvcrt.getch().decode('ASCII').upper()

            # Return to Menu
            if dest == "0":
                play = False
                menu = True
                save()  # manual save

            # Potions and Elixirs
            elif dest in ("1", "2"):
                if dest == "1":  # Potion
                    if POT > 0:
                        POT -= 1
                        heal(30)
                    else:
                        print(" No Potions!")
                        print("\n Press any key to continue")
                        msvcrt.getch().decode('ASCII').upper()
                    standing = True
                else:  # Elixir
                    if ELX > 0:
                        ELX -= 1
                        heal(50)
                    else:
                        print(" No Elixirs!")
                        print("\n Press any key to continue")
                        msvcrt.getch().decode('ASCII').upper()
                    standing = True

            # Movement
            elif dest in ("W", "A", "S", "D"):
                standing = False
                movement(dest, "Hero")

            # Talk to Mayor / Enter Shop / Inspect Gate / Initiate Combat
            elif dest == "3":
                if (area_y != 0 and area_x != 0 and area_y != len(biome[game_map[y][x]]["m"]) - 1 and
                        area_x != (len(biome[game_map[y][x]]["m"][0]) - 1)):
                    if ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "M") or
                            (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "M") or
                            (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "M") or
                            (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "M")):
                        speak = True
                        mayor()

                    elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "S") or
                          (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "S") or
                          (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "S") or
                          (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "S")):
                        buy = True
                        shop()
                    elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "I") or
                          (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "I") or
                          (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "I") or
                          (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "I")):
                        inn = True
                        reset("soft")

                    elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "G") or
                          (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "G") or
                          (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "G") or
                          (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "G")):
                        gate = True
                        at_gate()

                    elif ((biome[game_map[y][x]]["m"][area_y + 1][area_x] == "B") or
                          (biome[game_map[y][x]]["m"][area_y - 1][area_x] == "B") or
                          (biome[game_map[y][x]]["m"][area_y][area_x - 1] == "B") or
                          (biome[game_map[y][x]]["m"][area_y][area_x + 1] == "B")):
                        boss = True
                        boss_fight()

            # Invalid input
            else:
                standing = True
