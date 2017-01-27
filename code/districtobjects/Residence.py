from Placeable import Placeable


class Residence(Placeable):
    def __init__(self, x, y, width, height, ID, value, minimumClearance, addedValuePercentage, color):
        super(Residence, self).__init__(x, y, width, height)

        self.ID = ID
        self.value = value
        self.minimumClearance = minimumClearance
        self.addedValuePercentage = addedValuePercentage
        self.color = color
        self.original_min_clearance = minimumClearance

    def getType(self): return self.ID

    def getValue(self): return self.value

    def getminimumClearance(self): return self.minimumClearance

    def getAddedValuePercentage(self): return self.addedValuePercentage

    def getColor(self): return self.color
