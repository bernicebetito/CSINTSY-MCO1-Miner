class Miner():

    def __init__(self, direction):
        self.position = (0, 0) # default 0,0
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
            self.position[1] -= 1

        elif self.direction == "RIGHT":
            self.position[0] += 1

        elif self.direction == "DOWN":
            self.position[1] += 1
        
        else: # direction == LEFT
            self.position[0] -= 1

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

    def incrementActions(self):
        self.actions += 1

    def setMinerDeath(self):
        self.dead = True

    def setMinerVictor(self):
        self.victor = True