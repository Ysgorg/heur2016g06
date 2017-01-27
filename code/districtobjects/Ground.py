from Placeable import Placeable


class Ground(Placeable):

    def __init__(self, x, y, width, height):
        super(Ground, self).__init__(x, y, width, height)
