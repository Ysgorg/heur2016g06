from Residence import Residence


class FamilyHome(Residence):

    def __init__(self, x=-1, y=-1):
        super(FamilyHome, self).__init__(x,
                                         y,
                                         width=8.0,
                                         height=8.0,
                                         ID="FamilyHome",
                                         value=285000,
                                         minimumClearance=2,
                                         addedValuePercentage=0.03,
                                         color="Orange")
