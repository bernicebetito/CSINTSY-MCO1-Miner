class Miner():

    def __init__(self, direction):
        self.position = (0, 0) # default 0,0 (row, col)
        self.direction = direction # UP, DOWN, LEFT or RIGHT
        self.actions = 0 # miner action count
        self.isDead = False # if miner has moved into a pit
        self.isVictor = False # if miner has reached pot of gold

    def getContent(self):
        return "MINER"

    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    def getActions(self):
        return self.actions

    def ifDead(self):
        return self.isDead

    def ifVictor(self):
        return self.isVictor

    def moveMiner(self):
        if self.direction == "UP":
            self.position[0] -= 1

        elif self.direction == "RIGHT":
            self.position[1] += 1

        elif self.direction == "DOWN":
            self.position[0] += 1
        
        else: # direction == LEFT
            self.position[1] -= 1

        self.incrementActions()
        
    def rotateDirection(self): # rotate 90 degrees clockwise
        if self.direction == "UP":
            self.direction = "RIGHT"

        elif self.direction == "RIGHT":
            self.direction == "DOWN"

        elif self.direction == "DOWN":
            self.direction == "LEFT"
        
        else: # direction == LEFT
            self.direction == "UP"

        self.incrementActions()

    def scan(self, grid, gridNumber):
        self.incrementActions()
        result = "EMPTY"

        if self.direction == "UP":
            tempCoords = self.getPosition
            tempRow = tempCoords[0] - 1
            tempCol = tempCoords[1]

            while tempRow >= 0:
                result = grid[tempRow][tempCol].getContent()

                if result != "EMPTY":
                    return result

                tempRow -= 1

        elif self.direction == "RIGHT":
            tempCoords = self.getPosition
            tempRow = tempCoords[0]
            tempCol = tempCoords[1] + 1

            while tempRow < gridNumber:
                result = grid[tempRow][tempCol].getContent()

                if result != "EMPTY":
                    return result

                tempCol += 1

        elif self.direction == "DOWN":
            tempCoords = self.getPosition
            tempRow = tempCoords[0] + 1
            tempCol = tempCoords[1]

            while tempRow < gridNumber:
                result = grid[tempRow][tempCol].getContent()

                if result != "EMPTY":
                    return result

                tempRow += 1
        
        else: # direction == LEFT
            tempCoords = self.getPosition
            tempRow = tempCoords[0]
            tempCol = tempCoords[1] - 1

            while tempRow < gridNumber:
                result = grid[tempRow][tempCol].getContent()

                if result != "EMPTY":
                    return result

                tempCol -= 1

        return result

    def incrementActions(self):
        self.actions += 1

    def setMinerDeath(self):
        self.dead = True

    def setMinerVictor(self):
        self.victor = True