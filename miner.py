class Miner():

    def __init__(self, direction):
        self.position = (0, 0) # default 0,0
        self.direction = direction # UP, DOWN, LEFT or RIGHT
        self.actions = 0 # miner action count
        self.dead = False # if miner has moved into a pit
        self.victor = False # if miner has reached pot of gold

    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    def getMinerStatusDeath(self):
        return self.dead

    def getMinerStatusVictor(self):
        return self.victor

    def setPosition(self, positionX, positionY):
        self.position = (positionX, positionY)
        self.actions += 1
        
    def rotateDirection(self):
        if self.direction == "UP":
            self.direction = "LEFT"

        elif self.direction == "LEFT":
            self.direction == "DOWN"

        elif self.direction == "DOWN":
            self.direction == "RIGHT"
        
        else: # direction = RIGHT
            self.direction == "UP"

        self.actions += 1

    def setMinerDeath(self):
        self.dead = True

    def setMinerVictor(self):
        self.victor = True