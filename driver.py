import miner, gridSquare, random, math, pygame, os


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


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('MCO1: Miner')
done = False

font_main = pygame.font.SysFont(None, 50)
text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
font_sub = pygame.font.SysFont(None, 25)
text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))

font_icons = pygame.font.SysFont(None, 35)
pit_icon = font_icons.render("P", True, (120, 85, 137))
beacon_icon = font_icons.render("B", True, (73, 109, 219))

directory = os.getcwd()
miner_icon = pygame.image.load(directory + r'\assets\miner_icon.png')
miner_icon = pygame.transform.scale(miner_icon, (25, 25))

gold_icon = pygame.image.load(directory + r'\assets\gold_icon.png')
gold_icon = pygame.transform.scale(gold_icon, (25, 25))

font_direction = pygame.font.SysFont(None, 30)
curr_direction = font_direction.render("Current Direction: East", True, (240, 246, 246))

box_width = 35
box_height = 35
box_margin = 7

n = 8
grid = generateGrid(n)
for column in grid:
    print(column)

trueGrid = generateGridSquares(grid)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((25, 25, 25))

    screen.blit(text_main, (320 - text_main.get_width() // 2, text_main.get_height() // 2))
    screen.blit(text_sub, (320 - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))

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
                            [((box_margin + box_width) * col_ctr + box_margin) + (320 - ((box_margin + box_width) * 8) // 2) + 8,
                             ((box_margin + box_height) * row_ctr + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                             box_width,
                             box_height])
            else:
                pygame.draw.rect(screen, (200, 200, 200),
                                 [((box_margin + box_width) * col_ctr + box_margin) + (320 - ((box_margin + box_width) * 8) // 2),
                                  ((box_margin + box_height) * row_ctr + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20,
                                  box_width,
                                  box_height])
            col_ctr += 1
        row_ctr += 1

    direction_height = ((box_margin + box_height) * n + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 30
    screen.blit(curr_direction, (320 - curr_direction.get_width() // 2, direction_height))
    pygame.display.flip()