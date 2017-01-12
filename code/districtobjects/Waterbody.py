from Placeable import Placeable


class Waterbody(Placeable):
    def __init__(self, x, y, width, height):
        super(Waterbody, self).__init__(x, y, width, height)

    def getType(self):
        return "Water"
