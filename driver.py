import miner, gridSquare, random, math, pygame, os

pygame.init()
pygame.display.set_caption('MCO1: Miner')


# searching for gold for beacon placement
def searchTop(grid, currentRow, currentCol):
    tempRow = currentRow - 1
    while tempRow >= 0:
        if grid[tempRow][currentCol] == "GOLD":
            return True
        tempRow -= 1

    return False


def searchBottom(grid, currentRow, currentCol, gridNumber):
    tempRow = currentRow + 1
    while tempRow < gridNumber:
        if grid[tempRow][currentCol] == "GOLD":
            return True
        tempRow += 1

    return False


def searchRight(grid, currentRow, currentCol, gridNumber):
    tempCol = currentCol + 1
    while tempCol < gridNumber:
        if grid[currentRow][tempCol] == "GOLD":
            return True
        tempCol += 1

    return False


def searchLeft(grid, currentRow, currentCol):
    tempCol = currentCol - 1
    while tempCol >= 0:
        if grid[currentRow][tempCol] == "GOLD":
            return True
        tempCol -= 1

    return False


def generateGrid(gridNumber):  # generate grid blueprint
    pits = math.ceil(gridNumber * 0.25)
    beacons = math.ceil(gridNumber * 0.1)

    # samplingList = ["PIT", "GOLD", "EMPTY"]
    counts = {"PIT": 0, "BEACON": 0, "GOLD": 0, "EMPTY": 0}
    maxcounts = {"PIT": pits, "BEACON": beacons, "GOLD": 1, "EMPTY": 999999}

    grid = []

    # place miner and fill in grid with empty elements
    for rows in range(gridNumber):
        column = []

        for columns in range(gridNumber):
            if rows == 0 and columns == 0:  # miner
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
    for rows in grid:
        column = []
        for columns in rows:
            if columns == "MINER":
                gridElement = miner.Miner("RIGHT")

            else:
                gridElement = gridSquare.gridSquare(columns)

            column.append(gridElement)

        trueGrid.append(column)

    return trueGrid


def miner_screen(n_str, random_status, smart_status):
    n = int(n_str)
    algo = "RANDOM"

    if random_status:
        algo = "RANDOM"
    elif smart_status:
        algo = "SMART"

    done = False

    """
    51 - 64 = 7 7 2
    41 - 50 = 8 8 3
    31 - 40 = 10 10 4
    26 - 30 = 14 14 5
    21 - 25 = 18 18 5
    16 - 20 = 23 23 5
    11 - 15 = 30 30 7
    10 <= 35 35 7
    """

    box_size = 7
    box_margin = 2

    if n <= 50 and n >= 41:
        box_size = 8
        box_margin = 3
    elif n <= 40 and n >= 31:
        box_size = 10
        box_margin = 4
    elif n <= 30 and n >= 26:
        box_size = 14
        box_margin = 5
    elif n <= 25 and n >= 21:
        box_size = 18
        box_margin = 5
    elif n <= 20 and n >= 16:
        box_size = 23
        box_margin = 5
    elif n <= 15 and n >= 11:
        box_size = 30
        box_margin = 7
    elif n <= 10:
        box_size = 35
        box_margin = 7

    font_icons = pygame.font.SysFont(None, box_size)

    directory = os.getcwd()
    miner_icon = pygame.image.load(directory + r'\assets\miner_icon.png')
    miner_icon = pygame.transform.scale(miner_icon, (box_size, box_size))

    gold_icon = pygame.image.load(directory + r'\assets\gold_icon.png')
    gold_icon = pygame.transform.scale(gold_icon, (box_size, box_size))

    pit_icon = pygame.image.load(directory + r'\assets\pit_icon.png')
    pit_icon = pygame.transform.scale(pit_icon, (box_size, box_size))

    beacon_icon = pygame.image.load(directory + r'\assets\beacon_icon.png')
    beacon_icon = pygame.transform.scale(beacon_icon, (box_size, box_size))

    font_direction = pygame.font.SysFont(None, 30)
    curr_direction = font_direction.render("Current Direction: East", True, (240, 246, 246))

    grid = generateGrid(n)
    for column in grid:
        print(column)

    trueGrid = generateGridSquares(grid)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((25, 25, 25))

        dash_margin = (n * (box_size + box_margin) + (320 - ((box_margin + box_size) * n) // 2))
        dash_margin = (1024 + dash_margin) / 2

        screen.blit(text_main, (dash_margin - text_main.get_width() // 2, text_main.get_height() // 2))
        screen.blit(text_sub, (dash_margin - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))
        screen.blit(curr_direction, (dash_margin - curr_direction.get_width() // 2, text_main.get_height() + text_sub.get_height() + 110 // 2))

        row_ctr = 0
        for row in trueGrid:
            col_ctr = 0
            for column in row:
                if column.getContent() == "MINER" or column.getContent() == "GOLD" or column.getContent() == "PIT" or column.getContent() == "BEACON":
                    if column.getContent() == "MINER":
                        print_icon = miner_icon
                    elif column.getContent() == "GOLD":
                        print_icon = gold_icon
                    elif column.getContent() == "PIT":
                        print_icon = pit_icon
                    elif column.getContent() == "BEACON":
                        print_icon = beacon_icon

                    screen.blit(print_icon,
                                [((box_margin + box_size) * col_ctr + box_margin) + (320 - ((box_margin + box_size) * n) // 2),
                                 ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                 box_size,
                                 box_size])
                else:
                    pygame.draw.rect(screen, (200, 200, 200),
                                     [((box_margin + box_size) * col_ctr + box_margin) + (320 - ((box_margin + box_size) * n) // 2),
                                      ((box_margin + box_size) * row_ctr + box_margin) + 20,
                                      box_size,
                                      box_size])
                col_ctr += 1
            row_ctr += 1

        pygame.display.flip()


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

    active_text = False
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
                    active_text = True
                else:
                    active_text = False

                if random_rect.collidepoint(event.pos):
                    active_random = True
                    active_smart = False
                elif smart_rect.collidepoint(event.pos):
                    active_smart = True
                    active_random = False

                if enter_rect.collidepoint(event.pos):
                    if len(n_text) > 0 and str.isnumeric(n_text):
                        if int(n_text) >= 8 and int(n_text) <= 64:
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

        if active_text:
            n_color = n_active
        else:
            n_color = n_passive

        if active_random:
            random_color = algo_active
            random_color_text = algo_text_active
        else:
            random_color = algo_passive
            random_color_text = algo_text_passive

        if active_smart:
            smart_color = algo_active
            smart_color_text = algo_text_active
        else:
            smart_color = algo_passive
            smart_color_text = algo_text_passive

        pygame.draw.rect(screen, n_color, input_rect)

        text_surface = base_font.render(n_text, True, (33, 37, 41))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        screen.blit(text_algo, (512 - text_algo.get_width() // 2,
                                text_main.get_height() + text_sub.get_height() + text_surface.get_height() + 510 // 2))
        pygame.draw.rect(screen, random_color, random_rect)
        button_random = base_font.render(text_random, True, random_color_text)
        screen.blit(button_random, (random_rect.x + 13, random_rect.y + 5))

        pygame.draw.rect(screen, smart_color, smart_rect)
        button_smart = base_font.render(text_smart, True, smart_color_text)
        screen.blit(button_smart, (smart_rect.x + 20, smart_rect.y + 5))

        pygame.draw.rect(screen, (142, 202, 230), enter_rect)
        button_enter = base_font.render(text_enter, True, (255, 255, 255))
        screen.blit(button_enter, (enter_rect.x + 28, enter_rect.y + 5))

        pygame.display.flip()

    if not close_app:
        miner_screen(n_text, active_random, active_smart)


homescreen()