import random
import sys
from collections import deque
from copy import deepcopy
from os import system


global_time = 0.1

# SMART MOVEMENT FUNCTIONS

def check_opposite(miner):
    opposite = " "
    if miner["direction"] == "N":
        opposite = "S"

    elif miner["direction"] == "S":
        opposite = "N"

    elif miner["direction"] == "W":
        opposite = "E"

    elif miner["direction"] == "E":
        opposite = "W"

    return opposite


def scan_area(grid, miner):

    storage = []
    opposite = check_opposite(miner)
    for x in range(4):
        if miner["direction"] != opposite:
            scan(grid, miner)
            if miner["scan_result"] == "G":
                storage = [miner["direction"]]
                break
            elif miner["scan_result"] == "B" and miner["scan_coor"] not in miner["traversed"] and miner["scan_coor"] \
                    not in miner["reserved"]:
                storage.append(miner["direction"])
                move(grid, miner)
                if miner["beacon_hint"] == 0:
                    rotate(grid, miner)
                    rotate(grid, miner)
                    move(grid, miner)
                    rotate(grid, miner)
                    rotate(grid, miner)
                else:
                    break
            elif not miner["scan_result"] == "P" and not miner["scan_result"] == "Out of bounds" and \
                    miner["scan_coor"] not in miner["traversed"] and miner["scan_coor"] not in miner["reserved"]:
                storage.append(miner["direction"])
                miner["reserved"].append(deepcopy(miner["scan_coor"]))
        rotate(grid, miner)
    miner["smart_node_stack"].append(storage)


def beacon_to_gold(grid, miner):
    for x in range(4):
        count = 0
        rotate(grid, miner)
        for y in range(miner["beacon_hint"]):
            scan(grid, miner)
            if miner["scan_result"] == "P" or miner["scan_result"] == "Out of bounds":
                break
            if miner["scan_result"] == "G":
                move(grid, miner)
                break
            move(grid, miner)
            count += 1
            if miner["y_coor"] == grid["gold_y"] and miner["x_coor"] == grid["gold_x"]:
                break
        if miner["y_coor"] == grid["gold_y"] and miner["x_coor"] == grid["gold_x"]:
            break
        elif count > 0:
            rotate(grid, miner)
            rotate(grid, miner)
            for y in range(count):
                move(grid, miner)
            rotate(grid, miner)
            rotate(grid, miner)


def first_scan(grid, miner):
    storage = []
    for x in range(4):
        scan(grid, miner)
        if miner["scan_result"] == "G":
            storage = [miner["direction"]]
            break
        elif miner["scan_result"] == "B":
            storage.append(miner["direction"])
            move(grid, miner)
            if miner["beacon_hint"] == 0:
                rotate(grid, miner)
                rotate(grid, miner)
                move(grid, miner)
                rotate(grid, miner)
                rotate(grid, miner)
            else:
                break
        elif not miner["scan_result"] == "Out of bounds" and not miner["scan_result"] == "P":
            storage.append(miner["direction"])
        miner = rotate(grid, miner)
    miner["smart_node_stack"].append(storage)
