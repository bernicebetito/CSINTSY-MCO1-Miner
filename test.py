import miner, gridSquare, random, math, pygame, os

pygame.init()
pygame.display.set_caption('MCO1: Miner')
miner_element = miner.Miner("RIGHT")

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
                gridElement = miner_element
            elif row_ctr == pos_miner[0] and col_ctr == pos_miner[1]:
                if gridSquare.gridSquare(columns) == "PIT":
                    gridElement = gridSquare.gridSquare("LOSE")
                elif gridSquare.gridSquare(columns) == "GOLD":
                    gridElement = gridSquare.gridSquare("WIN")
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


grid = generateGrid(8)
done = False
while not done:
    trueGrid = generateGridSquares(grid)
    print("\n\n")
    for row in trueGrid:
        for column in row:
            if column.getContent() == "LOSE" or column.getContent() == "WIN":
                done = True
            print(column.getContent(), end=" ")
        print("\n")

    choice = random.randint(1, 2)
    if choice == 1:
        miner_element.rotateDirection()
    elif choice == 2:
        if miner_element.getDirection() == "UP":
            if miner_element.getPosition()[0] == 0:
                done = True
        elif miner_element.getDirection() == "LEFT":
            if miner_element.getPosition()[0] == 0:
                done = True
        miner_element.moveMiner()