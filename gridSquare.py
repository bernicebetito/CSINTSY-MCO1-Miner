class gridSquare():
    
    def __init__(self, content):
        self.content = content # miner, beacon, pit, gold or empty
        self.containsMiner = False

        
        if self.content == "MINER":
            self.containsMiner = True

    def getContent(self):
        return self.content

    def ifContainsMiner(self):
        return self.containsMiner

    def setMiner(self):
        if self.containsMiner == False:
            self.containsMiner = True

        else:
            self.containsMiner = False