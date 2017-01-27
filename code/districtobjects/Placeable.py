class Placeable(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x1 = self.x
        self.x2 = self.x1 + self.width
        self.y1 = self.y
        self.y2 = self.y1 + self.height
        self.flipped = False

    def setX(self, x): self.x = x

    def getX(self): return self.x

    def setY(self, y): self.y = y

    def getY(self): return self.y

    def getWidth(self): return self.width

    def getHeight(self): return self.height

    def getSurface(self): return self.width * self.height

    def leftEdge(self): return self.x

    def rightEdge(self): return self.x + self.width

    def topEdge(self): return self.y

    def bottomEdge(self): return self.y + self.height

    def getOrientation(self): return self.flipped

    def flip(self):
        self.flipped = False if self.flipped else True
        self.width, self.height = self.height, self.width
        return self

    def toString(self):
        return str(self.getX()) + " " + str(self.rightEdge()) + " " + str(self.y1) + " " + str(self.bottomEdge())
