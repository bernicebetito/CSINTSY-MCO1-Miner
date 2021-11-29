import random
import sys
from collections import deque
from copy import deepcopy
from os import system
from time import sleep

global_time = 0.1

#Miner mode function
def smart(backup_grid, backup_miner):
    grid = deepcopy(backup_grid)
    miner = deepcopy(backup_miner)

    grid["layout"][miner["y_coor"]][miner["x_coor"]] = "M"

    if grid["stored_tile"] == "P":
        miner["Lives"] = 0
        grid["layout"][miner["y_coor"]][miner["x_coor"]] = "X"

    print_grid(grid, miner)
    if grid["stored_tile"] == "B":
        sleep(1)
        view_steps(grid, miner)

    if miner["Lives"] != 0 and miner["beacon_hint"] == 0 and not (miner["x_coor"] == grid["gold_x"] and
                                                                  miner["y_coor"] == grid["gold_y"]):
        first_scan(grid, miner)

        while len(miner["smart_node_stack"]) != 0 and miner["beacon_hint"] == 0 and miner["Lives"] != 0:
            current_list = miner["smart_node_stack"].pop()

            if len(current_list) == 0:  # If the miner does not have anything in its list
                if len(miner["backtrack"]) == 0:  # Check if it reached the start AGAIN
                    pass
                else:  # Backtrack
                    current_backtrack = miner["backtrack"].pop()
                    while miner["direction"] != current_backtrack:
                        rotate(grid, miner)
                    move(grid, miner)
            else:   # The miner can move
                while miner["direction"] not in current_list:  # Rotate the miner
                    rotate(grid, miner)

                #  The code below checks if the path is straight AND is part of a backtrack
                if len(current_list) > 1 or (len(miner["backtrack"]) and len(current_list) != 0):
                    miner["backtrack"].append(check_opposite(miner))

                current_list.remove(miner["direction"])  # Remove the path before moving
                miner["smart_node_stack"].append(current_list)
                miner["traversed"].append([miner["x_coor"], miner["y_coor"]])
                move(grid, miner)
                if miner["x_coor"] == grid["gold_x"] and miner["y_coor"] == grid["gold_y"]:
                    break
                scan_area(grid, miner)
                if miner["beacon_hint"] != 0:
                    break

    if miner["beacon_hint"] != 0:
        beacon_to_gold(grid, miner)

    if miner["x_coor"] == grid["gold_x"] and miner["y_coor"] == grid["gold_y"]:
        print("Golden Block Found!")
    elif miner["Lives"] == 0:
        print("It Died! You Lose!")
    else:
        print("Gold unreachable! Miner has stopped working.")
    print("Total Moves:", miner["move_count"])
    print("Total Rotates:", miner["rotate_count"])
    print("Total Scans:", miner["scan_count"])
    print("Total Actions:", miner["move_count"] + miner["rotate_count"] + miner["scan_count"])
    input("Press Enter to Return to Main Menu. ")


def random_agent(backup_grid, backup_miner):
    grid = deepcopy(backup_grid)
    miner = deepcopy(backup_miner)
    grid["layout"][miner["y_coor"]][miner["x_coor"]] = "M"

    if grid["stored_tile"] == "P":
        miner["Lives"] = 0
        grid["layout"][miner["y_coor"]][miner["x_coor"]] = "X"
    elif grid["stored_tile"] == "B":
        view_steps(grid, miner)

    if miner["Lives"] != 0 and not (miner["x_coor"] == grid["gold_x"] and
                                    miner["y_coor"] == grid["gold_y"]):
        print_grid(grid, miner)
        while (miner["x_coor"] != grid["gold_x"] or miner["y_coor"] != grid["gold_y"]) and miner["Lives"] == 1:
            miner, grid = action(miner, grid)

    if miner["x_coor"] == grid["gold_x"] or miner["y_coor"] == grid["gold_y"]:
        print("Golden Block Found!")
    if miner["Lives"] == 0:
        print("It Died! You Lose!")
    print("Total Moves:", miner["move_count"])
    print("Total Rotates:", miner["rotate_count"])
    print("Total Scans:", miner["scan_count"])
    print("Total Actions:", miner["move_count"] + miner["rotate_count"] + miner["scan_count"])
    input("Press Enter to Return to Main Menu. ")
    input("Press Enter to return to Main Menu")