class Placeable(object):

    def __init__(self, x, y, width, height, flipped=False):
        self.width = width
        self.height = height
        self.x1 = x
        self.x2 = self.x1 + self.width
        self.y1 = y
        self.y2 = self.y1 + self.height
        self.flipped = False
        if flipped: self.flip()

    def flip(self):
        self.flipped = False if self.flipped else True
        t = self.width
        self.width = self.height
        self.height = t

        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height

        return self

    def toString(self):
        return str(self.getX()) + " " + str(self.rightEdge()) + " " + str(self.y1) + " " + str(self.bottomEdge())
