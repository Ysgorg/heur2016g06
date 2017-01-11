from src import Groundplan
from src import GroundplanFrame


class DistrictPlanner(object):
    NUMBER_OF_HOUSES = 40
    PLAYGROUND = False

    def __init__(self):
        self.plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.frame = GroundplanFrame(self.plan)
        self.frame.setPlan()

        """your code"""

        self.frame.root.mainloop()


DistrictPlanner()
