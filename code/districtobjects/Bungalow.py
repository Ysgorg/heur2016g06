from Residence import Residence


class Bungalow(Residence):
    def __init__(self, x=-1, y=-1):
        super(Bungalow, self).__init__(x,
                                       y,
                                       width=10.0,
                                       height=7.5,
                                       ID="Bungalow",
                                       value=399000,
                                       minimumClearance=3,
                                       addedValuePercentage=0.04,
                                       color="Magenta")
