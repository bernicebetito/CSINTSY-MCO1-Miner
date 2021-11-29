import random
import sys
from collections import deque
from copy import deepcopy
from os import system
from time import sleep

global_time = 0.1

# TODO: Modify Scan to one-tile only

# TODO: Modify move to separate rotate and move OR create a separate move function for random

# MAP DISPLAY FUNCTIONS


def clear_screen():
    if sys.platform == "win32":
        system('cls')
    else:
        system('clear')


def print_grid(grid, miner, print_string=""):
    clear_screen()

    print(" ___" * len(grid["layout"]))  # Will Print the top layer of stuff
    for x in range(len(grid["layout"])):
        print("|", end="")
        for y in range(len(grid["layout"])):  # Print the top of the grid per row
            if (miner["x_coor"] == y and miner["y_coor"] == x and miner["direction"] == "N") and miner["Lives"] > 0:
                print(" ^ |", end="")
            else:
                print("   |", end="")

        print("\n|", end="")

        for y in range(len(grid["layout"])):  # Print each row
            if (miner["x_coor"] == y and miner["y_coor"] == x and miner["direction"] == "W") and miner["Lives"] > 0:
                print("<" + grid["layout"][x][y] + " |", end="")
            elif (miner["x_coor"] == y and miner["y_coor"] == x and miner["direction"] == "E") and miner["Lives"] > 0:
                print(" " + grid["layout"][x][y] + ">|", end="")
            else:
                print(" " + grid["layout"][x][y] + " |", end="")

        print("\n|", end="")
        for y in range(len(grid["layout"])):
            if (miner["x_coor"] == y and miner["y_coor"] == x and miner["direction"] == "S") and miner["Lives"] > 0:
                print("_V_|", end="")
            else:
                print("___|", end="")

        print("")
    if print_string != "":
        print("Action: " + print_string)
    print("Total Moves:", miner["move_count"])
    print("Total Rotates:", miner["rotate_count"])
    print("Total Scans:", miner["scan_count"])
    print("Total lives:", miner["Lives"])

    sleep(global_time)


def preview_map(grid):
    print(" ___" * len(grid["layout"]))  # Will Print the top layer of stuff
    for x in range(len(grid["layout"])):
        print("|", end="")
        for y in range(len(grid["layout"])):  # Print the top of the grid per row
            print("   |", end="")

        print("\n|", end="")

        for y in range(len(grid["layout"])):  # Print each row
            if grid["layout"][x][y] != "M":
                print(" " + grid["layout"][x][y] + " |", end="")
            else:
                print("   |", end="")

        print("\n|", end="")
        for y in range(len(grid["layout"])):
            print("___|", end="")

        print("")
    print("")
    input("Press Enter to return to main menu")

# MINER ACTION FUNCTIONS


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
    # Change the miner's actual direction lmao
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


# MAP CREATION FUNCTIONS

def init(miner):
    clear_screen()
    grid = {
        "layout": [],
        "gold_x": -1,
        "gold_y": -1,
        "beacons": [],
        "pits": [],
        "stored_tile": " ",
        "initialized": False
    }  # RESET GRID
    size = 0

    while size > 64 or size < 8:
        size = int(input("Input Grid size (Size x Size): "))  # Setup Maze Layout
        if size > 64 or size < 8:
            print("Invalid size! Range must be from 8 to 64.")

    for x in range(size):
        grid["layout"].append([])
        for y in range(size):
            grid["layout"][x].append(" ")

    while 0 > grid["gold_x"] or grid["gold_x"] > len(grid["layout"]) - 1 or 0 > grid["gold_y"] or grid["gold_y"] \
            > len(grid["layout"]) - 1:
        clear_screen()
        grid["gold_x"], grid["gold_y"] = map(int, input("Input Gold X- and Y- Coordinates (Format: X Y): ").split())
        if 0 > grid["gold_x"] or grid["gold_x"] > len(grid["layout"]) - 1 or 0 > grid["gold_y"] or grid["gold_y"] \
                > len(grid["layout"]) - 1:
            print("Invalid coordinates, please enter a value between 0 to " + str(len(grid["layout"]) - 1) + ".")
    grid["layout"][grid["gold_y"]][grid["gold_x"]] = "G"

    clear_screen()
    coordinates = [-2, -2]
    print("Input Beacon X- and Y- Coordinates. (Format: X Y). ")
    print("Input -1 anywhere in the input to stop.")
    print("Input an existing coordinate to remove it from the list.")
    print("You cannot put a beacon on the location of the gold tile.")
    while coordinates[0] != -1 and coordinates[1] != -1:

        coordinates[0], coordinates[1] = map(int, input("Input: ").split())
        if (0 > coordinates[0] or coordinates[0] > len(grid["layout"]) - 1 or 0 > coordinates[1] or coordinates[1] >
            len(grid["layout"]) - 1) and (coordinates[0] != -1 and coordinates[1] != -1):
            print("Invalid coordinates, please enter a value between 0 to " + str(len(grid["layout"]) - 1) + ".")
        elif coordinates[0] == grid['gold_x'] and coordinates[1] == grid["gold_y"]:
            print("Tile already occupied by Gold tile, please input another tile.")
        elif coordinates in grid["beacons"]:
            grid["beacons"].remove(coordinates)
            print("Beacon at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ") removed.")
        elif coordinates[0] != -1 and coordinates[1] != -1:
            grid["beacons"].append(deepcopy(coordinates))
            print("Beacon added at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ").")

    for x in grid["beacons"]:
        grid["layout"][x[1]][x[0]] = "B"

    clear_screen()
    coordinates = [-2, -2]
    print("Input Pit X- and Y- Coordinates. (Format: X Y). ")
    print("Input -1 anywhere in the input to stop.")
    print("Input an existing coordinate to remove it from the list.")
    print("You cannot put a pit on the location of the gold tile.")
    print("You cannot put a pit on the location of a beacon.")
    while coordinates[0] != -1 and coordinates[1] != -1:

        coordinates[0], coordinates[1] = map(int, input("Input: ").split())
        if (0 > coordinates[0] or coordinates[0] > len(grid["layout"]) - 1 or 0 > coordinates[1] or coordinates[1] >
            len(grid["layout"]) - 1) and (coordinates[0] != -1 and coordinates[1] != -1):
            print("Invalid coordinates, please enter a value between 0 to " + str(len(grid["layout"]) - 1) + ".")
        elif coordinates[0] == grid['gold_x'] and coordinates[1] == grid["gold_y"]:
            print("Tile already occupied by Gold tile, please input another tile.")
        elif coordinates in grid["beacons"]:
            print("Tile already occupied by a beacon, please input another tile.")
        elif coordinates in grid["pits"]:
            grid["pits"].remove(coordinates)
            print("Pit at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ") removed.")
        elif coordinates[0] != -1 and coordinates[1] != -1:
            grid["pits"].append(deepcopy(coordinates))
            print("Pit added at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ").")

    for x in grid["pits"]:
        grid["layout"][x[1]][x[0]] = "P"

    if [0, 0] in grid["pits"]:
        grid["stored_tile"] = "P"
    elif [0, 0] in grid["beacons"]:
        grid["stored_tile"] = "B"

    clear_screen()
    print("Process complete, previewing grid...")
    sleep(1)
    preview_map(grid)
    grid["initialized"] = True
    backup_grid = deepcopy(grid)
    return grid, backup_grid, miner


def load_maze(grid, miner):
    clear_screen()
    print("Note: Duplicate values for beacon and pit coordinates will be ignored.")
    filename = input("Please load configuration file (e.g. config.txt, CASE-SENSITIVE): ")
    try:
        f = open(filename)

        # INITIALIZE BLOCK
        grid = {
            "layout": [],
            "gold_x": -1,
            "gold_y": -1,
            "beacons": [],
            "pits": [],
            "stored_tile": " ",
            "initialized": False
        }  # Reset Grid
        beacons = []
        pits = []
        try:
            grid_size = int(f.readline().rstrip('\n'))
        except ValueError:
            print("Expected a single number at grid size, received something else.")
            input("Press Enter to return to previous menu. ")
            return grid, deepcopy(grid), miner
        try:
            gold_x, gold_y = map(int, f.readline().rstrip('\n').split())
        except ValueError:
            print("Expected a coordinate at gold tile, received something else.")
            input("Press Enter to return to previous menu. ")
            return grid, deepcopy(grid), miner
        try:
            bcn_cnt = int(f.readline().rstrip('\n'))
        except ValueError:
            print("Expected a single number at beacon count, received something else. You may have put too many gold "
                  "coordinates.")
            input("Press Enter to return to previous menu. ")
            return grid, deepcopy(grid), miner
        for x in range(bcn_cnt):
            try:
                bcn_x, bcn_y = map(int, f.readline().rstrip('\n').split())
                beacons.append([bcn_x, bcn_y])
            except ValueError:
                print("Too few beacon coordinate values than declared. You may also have incorrectly typed a "
                      "coordinate.")
                input("Press Enter to return to previous menu. ")
                return grid, deepcopy(grid), miner
        pit_cnt = int(f.readline().rstrip('\n'))
        try:
            pass
        except ValueError:
            print("Expected a single number at pit count, received something else. You may have put too many beacon "
                  "coordinates.")
            input("Press Enter to return to previous menu. ")
            return grid, deepcopy(grid), miner
        for x in range(pit_cnt):
            try:
                pit_x, pit_y = map(int, f.readline().rstrip('\n').split())
                pits.append([pit_x, pit_y])
            except ValueError:
                print("Too few pit coordinate values than declared. You may also have incorrectly typed a coordinate.")
                input("Press Enter to return to Main Menu. ")
                return grid, deepcopy(grid), miner

        # ERROR-CHECKING BLOCK
        grid_error = False
        gold_tile_error = False
        beacon_error_coord = False
        pit_error_coord = False
        beacon_error_conflict = False
        pit_error_conflict = False

        if grid_size < 8 or grid_size > 64:
            grid_error = True
        if not grid_error and (gold_x < 0 or gold_x > grid_size or gold_y < 0 or gold_y > grid_size):
            gold_tile_error = True
        for x in beacons:
            if not grid_error and (x[0] < 0 or x[0] > grid_size or x[1] < 0 or x[1] > grid_size):
                beacon_error_coord = True
            if x[0] == gold_x and x[1] == gold_y:
                beacon_error_conflict = True
        for x in pits:
            if not grid_error and (x[0] < 0 or x[0] > grid_size or x[1] < 0 or x[1] > grid_size):
                pit_error_coord = True
            if (x[0] == gold_x and x[1] == gold_y) or x in beacons:
                pit_error_conflict = True

        if grid_error or gold_tile_error or beacon_error_coord or pit_error_coord or beacon_error_conflict \
                or pit_error_conflict:
            print("Errors found in configuration: ")
            if grid_error:
                print("- Invalid Grid Size, must only be from 8 to 64.")
            if gold_tile_error:
                print("- Invalid Gold Coordinates, coordinate must only be from 0 to " + str(grid_size) + ".")
            if beacon_error_coord:
                print("- Invalid Beacon coordinate found, coordinate must only be from 0 to " + str(grid_size) + ".")
            if beacon_error_conflict:
                print("- A beacon location conflicts with another tile! Please change the coordinates.")
            if pit_error_coord:
                print("- Invalid Pit coordinate found, coordinate must only be from 0 to " + str(grid_size) + ".")
            if pit_error_conflict:
                print("- A pit location conflicts with another tile! Please change the coordinates.")
            input("Press Enter to return to previous menu. ")

        else:  # Error checking was passed
            for x in range(grid_size):  # Create Grid
                grid["layout"].append([])
                for y in range(grid_size):
                    grid["layout"][x].append(" ")

            grid["layout"][gold_y][gold_x] = "G"  # Gold Creation
            grid["gold_x"] = gold_x
            grid["gold_y"] = gold_y

            for x in beacons:
                if x in grid["beacons"]:
                    continue
                else:
                    grid["beacons"].append(deepcopy(x))
                    grid["layout"][x[1]][x[0]] = "B"

            for x in pits:
                if x in grid["pits"]:
                    continue
                else:
                    grid["pits"].append(deepcopy(x))
                    grid["layout"][x[1]][x[0]] = "P"

                if [0, 0] in grid["pits"]:
                    grid["stored_tile"] = "P"
                elif [0, 0] in grid["beacons"]:
                    grid["stored_tile"] = "B"

            grid["initialized"] = True
            print("Configuration loaded! Previewing Grid.")
            grid["layout"][miner["y_coor"]][miner["x_coor"]] = "M"
            sleep(1)
            preview_map(grid)
        f.close()
    except FileNotFoundError:
        print("File does not exist. Returning to previous menu.")
        sleep(1)
    return grid, deepcopy(grid), miner


def modify_maze(grid, miner):
    choice = 0
    while choice != 5:
        clear_screen()
        print("Please choose what to modify.")
        print("| 1 - Change Gold Tile     |")
        print("| 2 - Modify Beacons       |")
        print("| 3 - Modify Pits          |")
        print("| 4 - Preview Grid         |")
        print("| 5 - Save Changes (if any)|")
        choice = int(input("Input Choice: "))
        if 1 > choice or choice > 5:
            print("Invalid choice. Please choose a number between 1 - 5.")
            sleep(1)
        else:
            if choice == 1:
                clear_screen()
                new_x = -2
                new_y = -2
                print("Current Gold Tile Location: (" + str(grid["gold_x"]) + ", " + str(grid["gold_y"]) + ")")
                print("You cannot put the gold tile on the location of a pit or beacon.")
                print("Input -1 anywhere in the input to cancel.")
                while (0 > new_x or new_x > len(grid["layout"]) or 0 > new_y or new_y > len(grid["layout"]) or
                       (grid["gold_x"] == new_x and grid["gold_y"] == new_y) or [new_x, new_y] in grid["beacons"] or
                       [new_x, new_y] in grid["pits"]) and (new_x != -1 and new_y != -1):
                    new_x, new_y = \
                        map(int, input("Input new Gold X- and Y- Coordinates (Format: X Y): ").split())
                    if (0 > new_x or new_x > len(grid["layout"]) - 1 or 0 > new_y or new_y > len(grid["layout"]) - 1) \
                            and (new_x != -1 and new_y != -1):
                        print("Invalid coordinates, please enter a value between 0 to " +
                              str(len(grid["layout"]) - 1) + ".")
                    elif grid["gold_x"] == new_x and grid["gold_y"] == new_y:
                        print("The gold tile is already there! Please choose another tile.")
                    elif [new_x, new_y] in grid["beacons"]:
                        print("There's a beacon at that tile! Please choose another tile.")
                    elif [new_x, new_y] in grid["pits"]:
                        print("There's a pit at that tile! Please choose another tile.")
                    elif new_x == -1 or new_x == -1:
                        print("Update cancelled.")
                        sleep(1)
                    else:
                        grid["layout"][grid["gold_y"]][grid["gold_x"]] = " "
                        if new_y == 0 and new_x == 0:
                            grid["stored_tile"] = "G"
                        elif grid["gold_y"] == 0 and grid["gold_x"] == 0:
                            grid["stored_tile"] = " "
                        grid["layout"][new_y][new_x] = "G"
                        grid["gold_y"] = new_y
                        grid["gold_x"] = new_x
                        print("Gold tile updated successfully!")
                        sleep(1)
                        break
            elif choice == 2:
                clear_screen()
                coordinates = [-2, -2]
                print("Current Beacon Locations: ")
                for x in grid["beacons"]:
                    print("- (" + str(x[0]) + ", " + str(x[1]) + ")")
                print("\nInput Beacon X- and Y- Coordinates. (Format: X Y). ")
                print("Input -1 anywhere in the input to stop.")
                print("Input an existing coordinate to remove it from the list.")
                print("You cannot put a beacon on the location of the gold tile.")
                print("You cannot put a beacon on the location of a pit.")
                while coordinates[0] != -1 and coordinates[1] != -1:
                    coordinates[0], coordinates[1] = map(int, input("Input: ").split())
                    if (0 > coordinates[0] or coordinates[0] > len(grid["layout"]) - 1 or 0 > coordinates[1] or
                        coordinates[1] >
                        len(grid["layout"]) - 1) and (coordinates[0] != -1 and coordinates[1] != -1):
                        print("Invalid coordinates, please enter a value between 0 to " + str(
                            len(grid["layout"]) - 1) + ".")
                    elif coordinates[0] == grid['gold_x'] and coordinates[1] == grid["gold_y"]:
                        print("Tile already occupied by Gold tile, please input another tile.")
                    elif coordinates in grid["beacons"]:
                        if coordinates[1] == 0 and coordinates[0] == 0:
                            grid["stored_tile"] = " "
                        grid["beacons"].remove(coordinates)
                        grid["layout"][coordinates[1]][coordinates[0]] = " "
                        print("Beacon at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ") removed.")
                    elif coordinates in grid["pits"]:
                        print("There's a pit at that tile. Please choose another tile.")
                    elif coordinates[0] != -1 and coordinates[1] != -1:
                        if coordinates[1] == 0 and coordinates[0] == 0:
                            grid["stored_tile"] = "B"
                        grid["beacons"].append(deepcopy(coordinates))
                        grid["layout"][coordinates[1]][coordinates[0]] = "B"
                        print("Beacon added at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ").")
                print("Changes applied!")
                sleep(1)
            elif choice == 3:
                clear_screen()
                coordinates = [-2, -2]
                print("Current Pit Locations: ")
                for x in grid["pits"]:
                    print("- (" + str(x[0]) + ", " + str(x[1]) + ")")
                print("\nInput Pit X- and Y- Coordinates. (Format: X Y). ")
                print("Input -1 anywhere in the input to stop.")
                print("Input an existing coordinate to remove it from the list.")
                print("You cannot put a pit on the location of the gold tile.")
                print("You cannot put a pit on the location of a beacon.")
                while coordinates[0] != -1 and coordinates[1] != -1:
                    coordinates[0], coordinates[1] = map(int, input("Input: ").split())
                    if (0 > coordinates[0] or coordinates[0] > len(grid["layout"]) - 1 or 0 > coordinates[1] or
                        coordinates[1] >
                        len(grid["layout"]) - 1) and (coordinates[0] != -1 and coordinates[1] != -1):
                        print("Invalid coordinates, please enter a value between 0 to " + str(
                            len(grid["layout"]) - 1) + ".")
                    elif coordinates[0] == grid['gold_x'] and coordinates[1] == grid["gold_y"]:
                        print("Tile already occupied by Gold tile, please input another tile.")
                    elif coordinates in grid["pits"]:
                        if coordinates[1] == 0 and coordinates[0] == 0:
                            grid["stored_tile"] = " "
                        grid["pits"].remove(coordinates)
                        grid["layout"][coordinates[1]][coordinates[0]] = " "
                        print("Pit at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ") removed.")
                    elif coordinates in grid["pits"]:
                        print("There's a beacon at that tile. Please choose another tile.")
                    elif coordinates[0] != -1 and coordinates[1] != -1:
                        if coordinates[1] == 0 and coordinates[0] == 0:
                            grid["stored_tile"] = "B"
                        grid["pits"].append(deepcopy(coordinates))
                        grid["layout"][coordinates[1]][coordinates[0]] = "P"
                        print("Beacon added at (" + str(coordinates[0]) + ", " + str(coordinates[1]) + ").")
                print("Changes applied!")
                sleep(1)
            elif choice == 4:
                clear_screen()
                preview_map(grid)
            elif choice != 5:
                print("Invalid choice, please choose a number between 1 - 5.")
                sleep(1)
    print("Changes saved!")
    sleep(1)

    return grid, deepcopy(grid), miner


def save_to_file(grid):
    clear_screen()
    filename = input("Enter Output Filename (add the .txt): ")
    original_stdout = sys.stdout

    f = open(filename, 'w')
    sys.stdout = f
    print(len(grid["layout"]))
    print(grid["gold_x"], grid["gold_y"])
    print(len(grid["beacons"]))
    for bcn in grid["beacons"]:
        print(bcn[0], bcn[1])
    print(len(grid["pits"]))
    for pit in grid["pits"]:
        print(pit[0], pit[1])

    f.close()
    sys.stdout = original_stdout

    input("File saved! Press enter to return to previous menu. ")


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


# MINER MODE FUNCTIONS


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
        print("It Ded! You Lose!")
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
        print("It Ded! You Lose!")
    print("Total Moves:", miner["move_count"])
    print("Total Rotates:", miner["rotate_count"])
    print("Total Scans:", miner["scan_count"])
    print("Total Actions:", miner["move_count"] + miner["rotate_count"] + miner["scan_count"])
    input("Press Enter to Return to Main Menu. ")
    input("Press Enter to return to Main Menu")

# MAIN MENU FUNCTION


def menu(option, grid, backup_grid, miner, backup_miner):
    global global_time
    clear_screen()

    if option == 1:
        choice = 0
        success = False
        while (1 > choice or choice > 5) or (not success):
            clear_screen()
            print("Please choose an option.")
            print("| 1 - Design a new Maze                |")
            print("| 2 - Load Maze from Configuration     |")
            if grid["initialized"]:
                print("| 3 - Modify Existing Maze             |")
                print("| 4 - Save Configuration to File       |")
                print("| 5 - Exit                             |")
            else:
                print("| 3 - Exit                             |")
            choice = int(input("Input Choice: "))
            if choice == 1:
                grid, backup_grid, miner = init(miner)
            elif choice == 2:
                grid, backup_grid, miner = load_maze(grid, miner)
            elif choice == 3 and grid["initialized"]:
                grid, backup_grid, miner = modify_maze(grid, miner)
            elif choice == 3 or (choice == 5 and grid["initialized"]):
                success = True
            elif choice == 4 and grid["initialized"]:
                save_to_file(grid)
            else:
                if grid["initialized"]:
                    print("Invalid choice. Please choose between 1 and 5.")
                else:
                    print("Invalid choice. Please choose between 1 and 3.")
                sleep(1)

    elif option == 2:
        if grid["initialized"]:
            preview_map(grid)
        else:
            print("Grid not yet initialized!")
            input("Press Enter to return to Main Menu. ")

    elif option == 3:
        if grid["initialized"]:
            print("Running Miner.")
            sleep(1)
            print("Mode: ", end="")
            sleep(0.5)
            print("Random")
            sleep(1.5)
            random_agent(backup_grid, backup_miner)
        else:
            print("Grid not yet initialized!")
            input("Press Enter to return to Main Menu. ")

    elif option == 4:
        if grid["initialized"]:
            print("Running Miner.")
            sleep(1)
            print("Mode: ", end="")
            sleep(0.5)
            print("Smart")
            sleep(1.5)
            smart(backup_grid, backup_miner)
        else:
            print("Grid not yet initialized!")
            input("Press Enter to return to Main Menu. ")
            input("Press Enter to return to Main Menu. ")

    elif option == 5:
        print("Current Action Delay: ", global_time, "seconds.")
        global_time = float(input("Input new delay (in seconds): "))
        input("Delay changed! Press enter to return to previous menu. ")

    elif option != 6:
        print("Invalid input")
        sleep(1)

    clear_screen()

    return grid, backup_grid, miner


def main():
    clear_screen()
    miner = {
        "x_coor": 0,
        "y_coor": 0,
        "direction": "N",
        "move_count": 0,
        "scan_count": 0,
        "rotate_count": 0,
        "scan_result": "NULL",
        "scan_coor": [],
        "beacon_hint": 0,
        "Lives": 1,
        "traversed": [],
        "reserved": [],
        "backtrack": [],
        "smart_node_stack": deque()
    }

    grid = {
        "layout": [],
        "gold_x": -1,
        "gold_y": -1,
        "beacons": [],
        "pits": [],
        "stored_tile": " ",
        "initialized": False
    }

    backup_grid = deepcopy(grid)
    backup_miner = deepcopy(miner)

    option = 0
    while option != 6:
        clear_screen()
        print("|       MAIN MENU      |")
        print("| 1 - Design/Load Maze |")
        print("| 2 - Preview Maze     |")
        print("| 3 - Run Random Agent |")
        print("| 4 - Run Smart Agent  |")
        print("| 5 - Change Speed     |")
        print("| 6 - Quit Sim         |")
        option = int(input("Input Choice: "))
        if 0 < option < 6:
            grid, backup_grid, miner = menu(option, grid, backup_grid, miner, backup_miner)
        elif option != 6:
            print("Invalid input")
            sleep(1)

    sys.exit()


main()
1