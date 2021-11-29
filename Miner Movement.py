import random
import sys
from collections import deque
from copy import deepcopy
from os import system
from time import sleep

global_time = 0.1

# Miner Action
def scan(grid, miner):
    scan_result = "NULL"
    coordinate = []
    if miner["direction"] == "N":
        coordinate.append(miner["x_coor"])
        coordinate.append(miner["y_coor"] - 1)
        if miner["y_coor"] - 1 < 0:
            scan_result = "Out of bounds"
        else:
            if grid["layout"][miner["y_coor"] - 1][miner["x_coor"]] != " ":
                scan_result = grid["layout"][miner["y_coor"] - 1][miner["x_coor"]]

    elif miner["direction"] == "E":
        coordinate.append(miner["x_coor"] + 1)
        coordinate.append(miner["y_coor"])
        if miner["x_coor"] + 1 > len(grid["layout"]) - 1:
            scan_result = "Out of bounds"
        else:
            if grid["layout"][miner["y_coor"]][miner["x_coor"] + 1] != " ":
                scan_result = grid["layout"][miner["y_coor"]][miner["x_coor"] + 1]

    elif miner["direction"] == "S":
        coordinate.append(miner["x_coor"])
        coordinate.append(miner["y_coor"] + 1)
        if miner["y_coor"] + 1 > len(grid["layout"]) - 1:
            scan_result = "Out of bounds"
        else:
            if grid["layout"][miner["y_coor"] + 1][miner["x_coor"]] != " ":
                scan_result = grid["layout"][miner["y_coor"] + 1][miner["x_coor"]]

    elif miner["direction"] == "W":
        coordinate.append(miner["x_coor"] - 1)
        coordinate.append(miner["y_coor"])
        if miner["x_coor"] - 1 < 0:
            scan_result = "Out of bounds"
        else:
            if grid["layout"][miner["y_coor"]][miner["x_coor"] - 1] != " ":
                scan_result = grid["layout"][miner["y_coor"]][miner["x_coor"] - 1]

    miner["scan_count"] += 1
    print_grid(grid, miner, "Scanned")
    print("Scan Result: " + scan_result)
    miner["scan_result"] = scan_result
    miner["scan_coor"] = deepcopy(coordinate)
    sleep(1)


def beacon_checker(grid, miner):
    i = 1
    scan_result = ""
    for bcn in grid["beacons"]:
        if miner["x_coor"] == bcn[0] and miner["y_coor"] == bcn[1]:
            if grid["gold_y"] - bcn[1] > 0:  # check below beacon
                while bcn[1] + i <= grid["gold_y"] and bcn[1] + i <= len(grid["layout"]):
                    if grid["layout"][bcn[1] + i][bcn[0]] != " " and grid["layout"][bcn[1] + i][bcn[0]] != "B":
                        scan_result = grid["layout"][bcn[1] + i][bcn[0]]
                        break
                    i += 1

            elif grid["gold_y"] - bcn[1] < 0:  # check above beacon
                while bcn[1] - i >= grid["gold_y"] and bcn[1] - i >= 0:
                    if grid["layout"][bcn[1] - i][bcn[0]] != " " and grid["layout"][bcn[1] - i][bcn[0]] != "B":
                        scan_result = grid["layout"][bcn[1] - i][bcn[0]]
                        break
                    i += 1

            elif grid["gold_x"] - bcn[0] > 0:  # check right of beacon
                while bcn[0] + i <= grid["gold_x"] and bcn[0] + i <= len(grid["layout"]):
                    if grid["layout"][bcn[1]][bcn[0] + i] != " " and grid["layout"][bcn[1]][bcn[0] + i] != "B":
                        scan_result = grid["layout"][bcn[1]][bcn[0] + i]
                        break
                    i += 1

            elif grid["gold_x"] - bcn[0] < 0:  # check left of beacon
                while bcn[0] - i >= grid["gold_x"] and bcn[0] - i >= 0:
                    if grid["layout"][bcn[1]][bcn[0] - i] != " " and grid["layout"][bcn[1]][bcn[0] - i] != "B":
                        scan_result = grid["layout"][bcn[1]][bcn[0] - i]
                        break
                    i += 1
    return scan_result


def view_steps(grid, miner):
    hint = 0
    for bcn in grid["beacons"]:
        if miner["x_coor"] == bcn[0] and miner["y_coor"] == bcn[1]:
            if grid["gold_x"] - bcn[0] == 0:
                if grid["gold_y"] - bcn[1] >= 0:

                    if beacon_checker(grid, miner) == 'G':
                        hint = grid["gold_y"] - bcn[1]
                else:
                    if beacon_checker(grid, miner) == 'G':
                        hint = bcn[1] - grid["gold_y"]

            elif grid["gold_y"] - bcn[1] == 0:
                if grid["gold_x"] - bcn[0] >= 0:

                    if beacon_checker(grid, miner) == 'G':
                        hint = grid["gold_x"] - bcn[0]

                else:
                    if beacon_checker(grid, miner) == 'G':
                        hint = bcn[0] - grid["gold_x"]
    miner["beacon_hint"] = hint
    print("Beacon Hint:", hint)
    sleep(1)
    return hint


def rotate(grid, miner):
    if miner["direction"] == "N":
        miner["direction"] = "E"
    elif miner["direction"] == "E":
        miner["direction"] = "S"
    elif miner["direction"] == "S":
        miner["direction"] = "W"
    elif miner["direction"] == "W":
        miner["direction"] = "N"
    miner["rotate_count"] += 1
    print_grid(grid, miner, "Rotated")
    return miner


def action(miner, grid):
    # choice = 1
    choice = random.randint(0, 2)
    if choice == 2:
        scan(grid, miner)

    elif choice == 1:
        move(grid, miner)

    elif choice == 0:
        rotate(grid, miner)

    return miner, grid


def move(grid, miner):
    # Change the miner's actual direction 
    # Make the miner move only
    if miner["direction"] == "N":
        if miner["y_coor"] - 1 < 0:
            print("Out of Bounds")
            miner["move_count"] += 1

        elif grid["layout"][miner["y_coor"] - 1][miner["x_coor"]] == "P":
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = " "
            miner["Lives"] = 0
            miner["move_count"] += 1

        else:
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"] - 1][miner["x_coor"]]
            grid["layout"][miner["y_coor"] - 1][miner["x_coor"]] = "M"
            miner["y_coor"] = miner["y_coor"] - 1
            miner["move_count"] += 1
            print_grid(grid, miner, "Moved North")

    elif miner["direction"] == "E":
        if miner["x_coor"] + 1 >= len(grid["layout"]):
            print("Out of Bounds")
            miner["move_count"] += 1

        elif grid["layout"][miner["y_coor"]][miner["x_coor"] + 1] == "P":
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"]][miner["x_coor"] + 1]
            grid["layout"][miner["y_coor"]][miner["x_coor"] + 1] = "X"
            miner["x_coor"] = miner["x_coor"] + 1
            miner["move_count"] += 1
            miner["Lives"] = 0
            print_grid(grid, miner, "Moved East")

        else:
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"]][miner["x_coor"] + 1]
            grid["layout"][miner["y_coor"]][miner["x_coor"] + 1] = "M"
            miner["x_coor"] = miner["x_coor"] + 1
            miner["move_count"] += 1
            print_grid(grid, miner, "Moved East")

    elif miner["direction"] == "S":
        if miner["y_coor"] + 1 >= len(grid["layout"]):
            print("Out of Bounds")
            miner["move_count"] += 1

        elif grid["layout"][miner["y_coor"] + 1][miner["x_coor"]] == "P":
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"] + 1][miner["x_coor"]]
            grid["layout"][miner["y_coor"] + 1][miner["x_coor"]] = "X"
            miner["y_coor"] = miner["y_coor"] + 1
            miner["Lives"] = 0
            miner["move_count"] += 1

        else:
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"] + 1][miner["x_coor"]]
            grid["layout"][miner["y_coor"] + 1][miner["x_coor"]] = "M"
            miner["y_coor"] = miner["y_coor"] + 1
            miner["move_count"] += 1
            print_grid(grid, miner, "Moved South")

    elif miner["direction"] == "W":
        if miner["x_coor"] - 1 < 0:
            miner["move_count"] += 1
            print("Out of Bounds")

        elif grid["layout"][miner["y_coor"]][miner["x_coor"] - 1] == "P":
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = " "
            miner["Lives"] = 0
            miner["move_count"] += 1
        else:
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = grid["stored_tile"]
            grid["stored_tile"] = grid["layout"][miner["y_coor"]][miner["x_coor"] - 1]
            grid["layout"][miner["y_coor"]][miner["x_coor"] - 1] = "M"
            miner["x_coor"] = miner["x_coor"] - 1
            miner["move_count"] += 1
            print_grid(grid, miner, "Moved West")

    if [miner["x_coor"], miner["y_coor"]] in grid["beacons"]:
        view_steps(grid, miner)
    if [miner["x_coor"], miner["y_coor"]] in grid["pits"]:
        miner["lives"] = 0

    return miner, grid