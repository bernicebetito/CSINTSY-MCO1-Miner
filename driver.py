import miner, gridSquare, random, math

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
        tempRow +=1

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

def generateGrid(gridNumber):
    pits = math.floor(gridNumber * 0.25)
    beacons = math.floor(gridNumber * 0.1)

    samplingList = ["PIT", "GOLD", "EMPTY"]
    counts = {"PIT" : 0, "BEACON" : 0, "GOLD" : 0, "EMPTY": 0}
    maxcounts = {"PIT" : pits, "BEACON" : beacons, "GOLD" : 1, "EMPTY": 999999}

    grid = []

    for rows in range(gridNumber):
        column = []

        for columns in range(gridNumber):
            if rows == 0 and columns == 0: # miner
                column.append("MINER")
                continue

            sample = random.sample(samplingList, 1)

            if counts[sample[0]] < maxcounts[sample[0]]:
                column.append(sample[0])
                counts[sample[0]] += 1

            else:
                column.append("EMPTY")

        grid.append(column)

    while counts["BEACON"] <= maxcounts["BEACON"]:
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

def generateGridSquares(grid): # returns a grid of gridSquare class elements using a grid blueprint
    trueGrid = []
    for rows in grid:
        column = []
        for columns in rows:
            gridElement = gridSquare.gridSquare(columns)
            column.append(gridElement)

        trueGrid.append(column)
    
    return trueGrid

grid = generateGrid(16)
for column in grid:
    print(column)

trueGrid = generateGridSquares(grid)
for row in trueGrid:
    for column in row:
        print(column.getContent(), end=" ")
    print("\n")




            

            