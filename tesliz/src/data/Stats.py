

class Stats(object):
    points = 5
    def __init__(self):
        
        self.classevade = 0
        self.shieldevade = 0
        self.accessoryevade = 0
        self.power = 3
        self.belief = 50
        self.tohit = 100
        #self.points = 5
        self.maxpoints = 5

    def getPoints(self):
        return self.__points


    def setPoints(self, value):
        if self.maxpoints < value:
            value = self.maxpoints
        self.__points = value


    def delPoints(self):
        del self.__points
    points = property(getPoints, setPoints, delPoints, "Points's Docstring")


