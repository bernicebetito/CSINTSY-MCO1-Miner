import miner, gridSquare, random, math, pygame, os
import threading, queue, time

pygame.init()
pygame.display.set_caption('MCO1: Miner')
miner_element = miner.Miner("RIGHT")


# searching for gold for beacon placement
def searchTop(grid, currentRow, currentCol):
    result = False
    tempRow = currentRow - 1
    while tempRow >= 0:
        if grid[tempRow][currentCol] == "GOLD":
            result = True
            break
        if grid[tempRow][currentCol] == "PIT":
            result = False
            break
        if grid[tempRow][currentCol] == "BEACON":
            result = False
            break
        tempRow -= 1

    return result


def searchBottom(grid, currentRow, currentCol, gridNumber):
    result = False
    tempRow = currentRow + 1
    while tempRow < gridNumber:
        if grid[tempRow][currentCol] == "GOLD":
            result = True
            break
        if grid[tempRow][currentCol] == "PIT":
            result = False
            break
        if grid[tempRow][currentCol] == "BEACON":
            result = False
            break
        tempRow += 1

    return result


def searchRight(grid, currentRow, currentCol, gridNumber):
    result = False
    tempCol = currentCol + 1
    while tempCol < gridNumber:
        if grid[currentRow][tempCol] == "GOLD":
            result = True
            break
        if grid[currentRow][tempCol] == "PIT":
            result = False
            break
        if grid[currentRow][tempCol] == "BEACON":
            result = False
            break
        tempCol += 1

    return result


def searchLeft(grid, currentRow, currentCol):
    result = False
    tempCol = currentCol - 1
    while tempCol >= 0:
        if grid[currentRow][tempCol] == "GOLD":
            result = True
            break
        if grid[currentRow][tempCol] == "PIT":
            result = False
            break
        if grid[currentRow][tempCol] == "BEACON":
            result = False
            break
        tempCol -= 1

    return result


def find_gold(grid, currentRow, currentCol, n):
    beacon_list = []

    # Search Top
    tempRow = currentRow
    row_ctr = 0
    while tempRow >= 0:
        beacon_top = row_ctr
        row_ctr += 1
        if grid[tempRow][currentCol] == "GOLD":
            beacon_list.append(beacon_top)
            tempRow = -1
        tempRow -= 1

    # Seacrh Bottom
    tempRow = currentRow
    row_ctr = 0
    while tempRow < n:
        beacon_bottom = row_ctr
        row_ctr += 1
        if grid[tempRow][currentCol] == "GOLD":
            beacon_list.append(beacon_bottom)
            tempRow = n
        tempRow += 1

    # Search Right
    tempCol = currentCol
    col_ctr = 0
    while tempCol < n:
        beacon_right = col_ctr
        col_ctr += 1
        if grid[currentRow][tempCol] == "GOLD":
            beacon_list.append(beacon_right)
            tempCol = n
        tempCol += 1

    # Search Left
    tempCol = currentCol
    col_ctr = 0
    while tempCol >= 0:
        beacon_left = col_ctr
        col_ctr += 1
        if grid[currentRow][tempCol] == "GOLD":
            beacon_list.append(beacon_left)
            tempCol = -1
        tempCol -= 1

    if len(beacon_list) > 0:
        return min(beacon_list)
    else:
        return 0


def generateGrid(gridNumber):  # generate grid blueprint
    pits = math.ceil(gridNumber * 0.25)
    beacons = math.ceil(gridNumber * 0.1)
    pos_miner = miner_element.getPosition()

    # samplingList = ["PIT", "GOLD", "EMPTY"]
    counts = {"PIT": 0, "BEACON": 0, "GOLD": 0, "EMPTY": 0}
    maxcounts = {"PIT": pits, "BEACON": beacons, "GOLD": 1, "EMPTY": 999999}

    grid = []

    # place miner and fill in grid with empty elements
    for rows in range(gridNumber):
        column = []

        for columns in range(gridNumber):
            if rows == pos_miner[0] and columns == pos_miner[1]:  # miner
                column.append("MINER")
                continue

            column.append("EMPTY")

        grid.append(column)

    # replace some empty elements with pits
    while counts["PIT"] < maxcounts["PIT"]:
        randRow = random.randint(0, gridNumber - 1)
        randCol = random.randint(0, gridNumber - 1)

        if grid[randRow][randCol] == "EMPTY":
            grid[randRow][randCol] = "PIT"
            counts["PIT"] += 1

    # place gold
    while counts["GOLD"] < maxcounts["GOLD"]:
        randRow = random.randint(0, gridNumber - 1)
        randCol = random.randint(0, gridNumber - 1)

        if grid[randRow][randCol] == "EMPTY":
            grid[randRow][randCol] = "GOLD"
            counts["GOLD"] += 1

    # place beacons
    while counts["BEACON"] < maxcounts["BEACON"]:
        randRow = random.randint(0, gridNumber - 1)
        randCol = random.randint(0, gridNumber - 1)

        # grid square is in upper right
        if randRow == 0 and randCol == (gridNumber - 1) and grid[randRow][randCol] == "EMPTY":
            bottomResult = searchBottom(grid, randRow, randCol, gridNumber)
            leftResult = searchLeft(grid, randRow, randCol)

            if bottomResult == True or leftResult == True:
                grid[randRow][randCol] = "BEACON"
                counts["BEACON"] += 1

        # grid square is in lower left
        if randRow == (gridNumber - 1) and randCol == 0 and grid[randRow][randCol] == "EMPTY":
            topResult = searchTop(grid, randRow, randCol)
            rightResult = searchRight(grid, randRow, randCol, gridNumber)

            if topResult == True or rightResult == True:
                grid[randRow][randCol] = "BEACON"
                counts["BEACON"] += 1

        # grid square is in lower right
        if randRow == (gridNumber - 1) and randCol == 0 and grid[randRow][randCol] == "EMPTY":
            topResult = searchTop(grid, randRow, randCol)
            leftResult = searchLeft(grid, randRow, randCol)

            if topResult == True or leftResult == True:
                grid[randRow][randCol] = "BEACON"
                counts["BEACON"] += 1

        # grid square is anywhere where empty
        elif grid[randRow][randCol] == "EMPTY":
            topResult = searchTop(grid, randRow, randCol)
            rightResult = searchRight(grid, randRow, randCol, gridNumber)
            bottomResult = searchBottom(grid, randRow, randCol, gridNumber)
            leftResult = searchLeft(grid, randRow, randCol)

            if topResult == True or leftResult == True or bottomResult == True or leftResult == True:
                grid[randRow][randCol] = "BEACON"
                counts["BEACON"] += 1

    return grid


def generateGridSquares(grid):  # returns a grid of gridSquare class elements using a grid blueprint
    trueGrid = []
    pos_miner = miner_element.getPosition()

    row_ctr = 0
    for rows in grid:
        column = []
        col_ctr = 0
        for columns in rows:
            if columns == "MINER":
                if grid[row_ctr][col_ctr] != "BEACON":
                    gridElement = gridSquare.gridSquare("PREV")
                    grid[row_ctr][col_ctr] = "PREV"
                else:
                    gridElement = gridSquare.gridSquare("BEACON")
            elif row_ctr == pos_miner[0] and col_ctr == pos_miner[1]:
                if columns == "PIT":
                    gridElement = gridSquare.gridSquare("LOSE")
                    miner_element.setMinerDeath()
                elif columns == "GOLD":
                    gridElement = gridSquare.gridSquare("WIN")
                    miner_element.setMinerVictor()
                elif columns == "BEACON":
                    gridElement = gridSquare.gridSquare("BEACON")
                    grid[row_ctr][col_ctr] = "BEACON"
                else:
                    gridElement = miner_element
                    grid[row_ctr][col_ctr] = "MINER"
            else:
                gridElement = gridSquare.gridSquare(columns)

            column.append(gridElement)
            col_ctr += 1

        trueGrid.append(column)
        row_ctr += 1

    return trueGrid


def miner_screen(n_str, random_status, smart_status):
    n = int(n_str)
    algo = "RANDOM"

    if random_status:
        algo = "RANDOM"
    elif smart_status:
        algo = "SMART"

    done = False

    box_size = 7
    box_margin = 2

    if 50 >= n >= 41:
        box_size = 8
        box_margin = 3
    elif 40 >= n >= 31:
        box_size = 10
        box_margin = 4
    elif 30 >= n >= 26:
        box_size = 14
        box_margin = 5
    elif 25 >= n >= 21:
        box_size = 18
        box_margin = 5
    elif 20 >= n >= 16:
        box_size = 23
        box_margin = 5
    elif 15 >= n >= 11:
        box_size = 30
        box_margin = 7
    elif n <= 10:
        box_size = 35
        box_margin = 7

    directory = os.getcwd()
    miner_icon = pygame.image.load(directory + r'\assets\miner_icon.png')
    miner_icon = pygame.transform.scale(miner_icon, (box_size, box_size))

    gold_icon = pygame.image.load(directory + r'\assets\gold_icon.png')
    gold_icon = pygame.transform.scale(gold_icon, (box_size, box_size))

    pit_icon = pygame.image.load(directory + r'\assets\pit_icon.png')
    pit_icon = pygame.transform.scale(pit_icon, (box_size, box_size))

    beacon_icon = pygame.image.load(directory + r'\assets\beacon_icon.png')
    beacon_icon = pygame.transform.scale(beacon_icon, (box_size, box_size))

    font_dashboard = pygame.font.SysFont(None, 30)
    curr_direction = font_dashboard.render("Current Direction:", True, (240, 246, 246))

    ctr_header = font_dashboard.render("Counters", True, (240, 246, 246))
    rotate_ctr = font_dashboard.render("Rotate: ", True, (240, 246, 246))
    scan_ctr = font_dashboard.render("Scan: ", True, (240, 246, 246))
    move_ctr = font_dashboard.render("Move: ", True, (240, 246, 246))

    scan_header = font_dashboard.render("Scan Result: ", True, (240, 246, 246))
    scan_result = "NONE"
    beacon_header = font_dashboard.render("Beacon Hint: ", True, (240, 246, 246))
    beacon_result = "NONE"

    pace_header = font_dashboard.render("Choose Pace:", True, (240, 246, 246))

    rotate_ctr_int = 0
    scan_ctr_int = 0
    move_ctr_int = 0

    dash_margin = (n * (box_size + box_margin) + (320 - ((box_margin + box_size) * n) // 2))
    dash_margin = (1024 + dash_margin) / 2

    rotate_height = text_main.get_height() + text_sub.get_height() + curr_direction.get_height() + ctr_header.get_height()
    scan_height = rotate_height + rotate_ctr.get_height()
    move_height = scan_height + scan_ctr.get_height()
    scan_res_height = move_height + move_ctr.get_height()
    beacon_res_height = scan_res_height + scan_header.get_height()
    pace_height = beacon_res_height + beacon_header.get_height()

    pace_step = "Step by Step"
    step_rect = pygame.Rect(
        dash_margin - 285 // 2,
        pace_height + 650 // 2,
        130, 30
    )

    pace_fast = "Fast"
    fast_rect = pygame.Rect(
        dash_margin + 25 // 2,
        pace_height + 650 // 2,
        130, 30
    )

    pace_active = (255, 221, 0)
    pace_passive = (0, 80, 157)
    pace_text_active = (255, 255, 255)
    pace_text_passive = (33, 37, 41)

    pace = "NONE"

    step_color = pace_passive
    step_color_text = pace_text_passive
    fast_color = pace_passive
    fast_color_text = pace_text_passive

    miner_status = False
    miner_dead = False
    miner_won = False
    grid = generateGrid(n)
    trueGrid = generateGridSquares(grid)

    scan_result_smart = "INIT"
    smart_rotate_count = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if step_rect.collidepoint(event.pos) and pace == "NONE":
                    step_color = pace_active
                    step_color_text = pace_text_active
                    fast_color = pace_passive
                    fast_color_text = pace_text_passive
                    pace = "STEP"
                elif fast_rect.collidepoint(event.pos) and pace == "NONE":
                    step_color = pace_passive
                    step_color_text = pace_text_passive
                    fast_color = pace_active
                    fast_color_text = pace_text_active
                    pace = "FAST"

        screen.fill((25, 25, 25))

        screen.blit(text_main, (dash_margin - text_main.get_width() // 2, text_main.get_height() // 2))
        screen.blit(text_sub, (dash_margin - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))
        screen.blit(curr_direction, (dash_margin - curr_direction.get_width() // 2, text_main.get_height() + text_sub.get_height() + 110 // 2))

        direction = miner_element.getDirection()
        dir_render = font_dashboard.render(direction, True, (167, 201, 87))
        screen.blit(dir_render, (dash_margin - dir_render.get_width() // 2,
                                 text_main.get_height() + text_sub.get_height() + curr_direction.get_height() + 125 // 2))

        screen.blit(ctr_header, (dash_margin - ctr_header.get_width() // 2,
                                 text_main.get_height() + text_sub.get_height() + curr_direction.get_height() + 250 // 2))

        rotate_ctr_str = str(rotate_ctr_int)
        scan_ctr_str = str(scan_ctr_int)
        move_ctr_str = str(move_ctr_int)

        screen.blit(rotate_ctr, (dash_margin - rotate_ctr.get_width() + len(rotate_ctr_str) + 5 // 2, rotate_height + 300 // 2))
        rotate_ctr_num = font_dashboard.render(rotate_ctr_str, True, (255, 159, 28))
        screen.blit(rotate_ctr_num,
                    ((dash_margin - rotate_ctr.get_width() + len(rotate_ctr_str) + 5 // 2) + rotate_ctr.get_width(),
                     rotate_height + 300 // 2))

        screen.blit(scan_ctr, (dash_margin - scan_ctr.get_width() + len(scan_ctr_str) + 5 // 2, scan_height + 325 // 2))
        scan_ctr_num = font_dashboard.render(scan_ctr_str, True, (255, 159, 28))
        screen.blit(scan_ctr_num,
                    ((dash_margin - scan_ctr.get_width() + len(scan_ctr_str) + 5 // 2) + scan_ctr.get_width(),
                     scan_height + 325 // 2))

        screen.blit(move_ctr, (dash_margin - move_ctr.get_width() + len(move_ctr_str) + 5 // 2, move_height + 350 // 2))
        move_ctr_num = font_dashboard.render(move_ctr_str, True, (255, 159, 28))
        screen.blit(move_ctr_num,
                    ((dash_margin - move_ctr.get_width() + len(move_ctr_str) + 5 // 2) + move_ctr.get_width(),
                     move_height + 350 // 2))

        screen.blit(scan_header, (dash_margin - scan_header.get_width() + len(scan_result) // 2, scan_res_height + 450 // 2))
        scan_result_str = font_dashboard.render(scan_result, True, (106, 90, 205))
        screen.blit(scan_result_str,
                    ((dash_margin - scan_header.get_width() + len(scan_result) + 5 // 2) + scan_header.get_width(),
                     scan_res_height + 450 // 2))

        screen.blit(beacon_header, (dash_margin - beacon_header.get_width() + len(beacon_result) // 2, beacon_res_height + 475 // 2))
        beacon_result_str = font_dashboard.render(beacon_result, True, (106, 90, 205))
        screen.blit(beacon_result_str,
                    ((dash_margin - beacon_header.get_width() + len(beacon_result) + 5 // 2) + beacon_header.get_width(),
                    beacon_res_height + 475 // 2))

        screen.blit(pace_header, (dash_margin - pace_header.get_width() // 2, pace_height + 550 // 2))
        pygame.draw.rect(screen, step_color, step_rect)
        button_step = font_dashboard.render(pace_step, True, step_color_text)
        screen.blit(button_step, (step_rect.x + (130 - button_step.get_width()) // 2, step_rect.y + 5))

        pygame.draw.rect(screen, fast_color, fast_rect)
        button_fast = font_dashboard.render(pace_fast, True, fast_color_text)
        screen.blit(button_fast, (fast_rect.x + (130 - button_fast.get_width()) // 2, fast_rect.y + 5))

        row_ctr = 0
        for row in trueGrid:
            col_ctr = 0
            for column in row:
                if column.getContent() == "MINER" or column.getContent() == "GOLD" \
                        or column.getContent() == "PIT" or column.getContent() == "BEACON":
                    if column.getContent() == "MINER":
                        print_icon = miner_icon
                    elif column.getContent() == "GOLD":
                        print_icon = gold_icon
                    elif column.getContent() == "PIT":
                        print_icon = pit_icon
                    else:
                        print_icon = beacon_icon

                    screen.blit(print_icon,
                                [((box_margin + box_size) * col_ctr + box_margin) + (
                                            320 - ((box_margin + box_size) * n) // 2),
                                 ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                 box_size,
                                 box_size])
                elif column.getContent() == "PREV":
                    pygame.draw.rect(screen, (60, 60, 60),
                                     [((box_margin + box_size) * col_ctr + box_margin) + (
                                                 320 - ((box_margin + box_size) * n) // 2),
                                      ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                      box_size,
                                      box_size])
                elif column.getContent() == "LOSE":
                    pygame.draw.rect(screen, (255, 0, 0),
                                     [((box_margin + box_size) * col_ctr + box_margin) + (
                                                 320 - ((box_margin + box_size) * n) // 2),
                                      ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                      box_size,
                                      box_size])
                    miner_status = True
                    miner_dead = True
                elif column.getContent() == "WIN":
                    pygame.draw.rect(screen, (255, 165, 0),
                                     [((box_margin + box_size) * col_ctr + box_margin) + (
                                                 320 - ((box_margin + box_size) * n) // 2),
                                      ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                      box_size,
                                      box_size])
                    miner_status = True
                    miner_won = True
                else:
                    pygame.draw.rect(screen, (200, 200, 200),
                                     [((box_margin + box_size) * col_ctr + box_margin) + (320 - ((box_margin + box_size) * n) // 2),
                                      ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                      box_size,
                                      box_size])
                col_ctr += 1
            row_ctr += 1

        if algo == "RANDOM" and not miner_status and pace != "NONE": # Random Algo
            choice = random.randint(1, 3)
            if choice == 1:
                miner_element.rotateDirection()
                rotate_ctr_int += 1
            elif choice == 2:
                if miner_element.getDirection() == "UP":
                    if miner_element.getPosition()[0] > 0:
                        miner_element.moveMiner(grid)
                        trueGrid = generateGridSquares(grid)
                        move_ctr_int += 1
                elif miner_element.getDirection() == "LEFT":
                    if miner_element.getPosition()[1] > 0:
                        miner_element.moveMiner(grid)
                        trueGrid = generateGridSquares(grid)
                        move_ctr_int += 1
                elif miner_element.getDirection() == "DOWN":
                    if miner_element.getPosition()[0] < n - 1:
                        miner_element.moveMiner(grid)
                        trueGrid = generateGridSquares(grid)
                        move_ctr_int += 1
                elif miner_element.getDirection() == "RIGHT":
                    if miner_element.getPosition()[1] < n - 1:
                        miner_element.moveMiner(grid)
                        trueGrid = generateGridSquares(grid)
                        move_ctr_int += 1

            elif choice == 3:
                scan_result = miner_element.scan(grid)
                if scan_result == "PREV":
                    scan_result = "EMPTY"
                scan_ctr_int += 1

        elif algo == "SMART" and not miner_status and pace != "NONE": #Smart Algorithm (Greedy)
            if scan_result_smart == "INIT":
                scan_result_smart = miner_element.scan(grid)
                scan_ctr_int += 1
            elif grid[miner_element.getPosition()[0]][miner_element.getPosition()[1]] == "BEACON" and scan_result_smart != "GOLD":
                scan_result_smart = miner_element.scan(grid)
                scan_ctr_int += 1
                if scan_result_smart != "GOLD":
                    miner_element.rotateDirection()
                    rotate_ctr_int += 1
                    smart_rotate_count += 1
            elif scan_result_smart == "EMPTY" and smart_rotate_count == 4:
                miner_element.moveMiner(grid)
                trueGrid = generateGridSquares(grid)
                move_ctr_int += 1
                smart_rotate_count = 0
            elif scan_result_smart == "EMPTY" and smart_rotate_count != 4:
                miner_element.rotateDirection()
                rotate_ctr_int += 1
                smart_rotate_count += 1
                scan_result_smart = miner_element.scan(grid)
                scan_ctr_int += 1
            elif scan_result_smart == "PIT" or scan_result_smart == "PREV":
                miner_element.rotateDirection()
                rotate_ctr_int += 1
                scan_result_smart = miner_element.scan(grid)
                scan_ctr_int += 1
                smart_rotate_count += 1
            elif scan_result_smart == "GOLD" or scan_result_smart == "BEACON":
                miner_element.moveMiner(grid)
                trueGrid = generateGridSquares(grid)
                move_ctr_int += 1

            scan_result = scan_result_smart
            if scan_result == "PREV":
                scan_result = "EMPTY"
        else:
            if miner_dead:
                end_message = font_dashboard.render("Game Over!", True, (255, 0, 0))
                screen.blit(end_message, (320 - end_message.get_width() // 2, ((box_margin + box_size) * n + box_margin) + 30))
            elif miner_won:
                end_message = font_dashboard.render("Congratulations!", True, (255, 165, 0))
                screen.blit(end_message, (320 - end_message.get_width() // 2, ((box_margin + box_size) * n + box_margin) + 30))

        if grid[miner_element.getPosition()[0]][miner_element.getPosition()[1]] == "BEACON":
            beacon_hint = find_gold(grid, miner_element.getPosition()[0], miner_element.getPosition()[1], n)
            beacon_result = str(beacon_hint)

        pygame.display.flip()

        if pace == "STEP":
            pygame.time.delay(500)


def homescreen():
    global screen, font_main, text_main, font_sub, text_sub

    screen = pygame.display.set_mode((1024, 620))
    done = True

    font_main = pygame.font.SysFont(None, 50)
    text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
    font_sub = pygame.font.SysFont(None, 25)
    text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))

    font_input = pygame.font.SysFont(None, 25)
    text_input = font_input.render("Enter Number of Rows / Columns [8 - 64]:", True, (240, 246, 246))

    base_font = pygame.font.Font(None, 27)
    n_text = ''
    input_rect = pygame.Rect(
        824 // 2,
        text_main.get_height() + text_sub.get_height() + text_input.get_height() + 350 // 2,
        200, 30
    )

    text_algo = font_input.render("Choose Behavior:", True, (240, 246, 246))
    text_random = "Random"
    random_rect = pygame.Rect(
        800 // 2,
        text_main.get_height() + text_sub.get_height() + 600 // 2,
        100, 30
    )
    text_smart = "Smart"
    smart_rect = pygame.Rect(
        1024 // 2,
        text_main.get_height() + text_sub.get_height() + 600 // 2,
        100, 30
    )

    text_enter = "Start"
    enter_rect = pygame.Rect(
        924 // 2,
        text_main.get_height() + text_sub.get_height() + 750 // 2,
        100, 30
    )

    n_active = (248, 249, 250)
    n_passive = (73, 80, 87)
    n_color = n_passive

    algo_active = (255, 183, 3)
    algo_passive = (0, 80, 157)
    algo_text_active = (255, 255, 255)
    algo_text_passive = (33, 37, 41)

    random_color = algo_passive
    random_color_text = algo_text_passive
    smart_color = algo_passive
    smart_color_text = algo_text_passive

    active_random = False
    active_smart = False

    close_app = False

    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                close_app = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    n_color = n_active
                else:
                    n_color = n_passive

                if random_rect.collidepoint(event.pos):
                    random_color = algo_active
                    random_color_text = algo_text_active
                    smart_color = algo_passive
                    smart_color_text = algo_text_passive

                    active_random = True
                    active_smart = False
                elif smart_rect.collidepoint(event.pos):
                    random_color = algo_passive
                    random_color_text = algo_text_passive
                    smart_color = algo_active
                    smart_color_text = algo_text_active

                    active_random = False
                    active_smart = True

                if enter_rect.collidepoint(event.pos):
                    if len(n_text) > 0 and str.isnumeric(n_text):
                        if 8 <= int(n_text) <= 64:
                            if active_smart or active_random:
                                done = False
                                close_app = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    n_text = n_text[:-1]
                else:
                    n_text += event.unicode

        screen.fill((25, 25, 25))
        screen.blit(text_main, (512 - text_main.get_width() // 2, text_main.get_height() + 200 // 2))
        screen.blit(text_sub, (512 - text_sub.get_width() // 2, text_main.get_height() + text_sub.get_height() + 230 // 2))
        screen.blit(text_input, (512 - text_input.get_width() // 2, text_main.get_height() + text_sub.get_height() + 310 // 2))

        pygame.draw.rect(screen, n_color, input_rect)

        text_surface = base_font.render(n_text, True, (33, 37, 41))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        screen.blit(text_algo, (512 - text_algo.get_width() // 2,
                                text_main.get_height() + text_sub.get_height() + text_surface.get_height() + 510 // 2))
        pygame.draw.rect(screen, random_color, random_rect)

        button_random = base_font.render(text_random, True, random_color_text)
        screen.blit(button_random, (random_rect.x + (100 - button_random.get_width()) // 2, random_rect.y + 5))

        pygame.draw.rect(screen, smart_color, smart_rect)
        button_smart = base_font.render(text_smart, True, smart_color_text)
        screen.blit(button_smart, (smart_rect.x + (100 - button_smart.get_width()) // 2, smart_rect.y + 5))

        pygame.draw.rect(screen, (142, 202, 230), enter_rect)
        button_enter = base_font.render(text_enter, True, (255, 255, 255))
        screen.blit(button_enter, (enter_rect.x + (100 - button_enter.get_width()) // 2, enter_rect.y + 5))

        pygame.display.flip()

    if not close_app:
        miner_screen(n_text, active_random, active_smart)


homescreen()
