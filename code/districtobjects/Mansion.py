from Residence import Residence


class Mansion(Residence):
    def __init__(self, x=-1, y=-1):
        super(Mansion, self).__init__(x,
                                      y,
                                      width=11.0,
                                      height=10.5,
                                      ID="Mansion",
                                      value=610000,
                                      minimumClearance=6,
                                      addedValuePercentage=0.06,
                                      color="Cyan")
