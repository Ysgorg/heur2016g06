from Placeable import Placeable


class Playground(Placeable):

    def __init__(self, x, y, width=30.0, height=20.0, price=500000):
        super(Playground, self).__init__(x, y, width, height)
        self.price = price

    def getPrice(self): return self.price
