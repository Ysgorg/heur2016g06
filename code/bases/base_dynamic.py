import math

from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan

MIN_CHANGE = 0
MAX_CHANGE = 20

# Coordinate offset from origin
X_OFFSET = -5
Y_OFFSET = 0

# Spreading buildings from center towards the edge
X_SPREAD = 5
Y_SPREAD = 5


class base_dynamic(object):

    def __init__(self, num_houses, enable_playground, width, height):

        self.name = 'base_dynamic'
        self.puts = ['Waterbodies', 'Playgrounds']

        self.enable_playground = enable_playground
        self.num_houses = num_houses
        self.plan = self.develop_ground_plan(width, height)

    def deepCopy(self):
        return self.plan.deepCopy()

    @staticmethod
    def placeWater(plan, num_bodies):

        # input plan and desired number of water bodies
        # output the dimensions that give exactly MINIMUM_WATER_PERCENTAGE
        h = math.sqrt( ((plan.height * plan.width * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies) / 4)
        w = h * 4

        # Starting position
        x = 0
        y = plan.height - h

        for i in range(1, num_bodies + 1):
            wb = Waterbody(x, y, w, h)

            # if plan.correctlyPlaced(wb, verbose=True):
            plan.waterbodies.append(wb)
            #    print "Waterbody", i, "placed"
            x += w + 1  # +1 so that the bodies are not touching

        return plan

    @staticmethod
    def placePlaygrounds(plan, y_invert):

        dummy_pg = Playground(0, 0)

        playgroundReachX = dummy_pg.width + plan.MAXIMUM_PLAYGROUND_DISTANCE + 7.5
        playgroundReachY = dummy_pg.height + plan.MAXIMUM_PLAYGROUND_DISTANCE + 7.5

        utilisableX = plan.width
        utilisableY = plan.height-plan.MINIMUM_WATER_PERCENTAGE*plan.height#int(plan.height * (plan.AREA * plan.MINIMUM_WATER_PERCENTAGE))

        # Floor the total utilisable width and height by our playground reach
        # to find optimal number to fit

        numberPlaygroundsX = int(utilisableX // playgroundReachX)
        numberPlaygroundsY = int(utilisableY // playgroundReachY)

        for x in range(1, numberPlaygroundsX+1):

            xSpread = X_SPREAD
            yOffset = Y_OFFSET

            # if x is in the lower half, invert the offset
            if x <= numberPlaygroundsX / 2:
                xSpread = -xSpread
                yOffset += y_invert

            locationX = ((plan.MAXIMUM_PLAYGROUND_DISTANCE * x) + X_OFFSET) + ( plan.MAXIMUM_PLAYGROUND_DISTANCE * (x - 1)) + xSpread

            for y in range(1,numberPlaygroundsY+1):

                ySpread = Y_SPREAD

                # if y is in the lower half, invert the offset
                if y <= numberPlaygroundsY / 2:
                    ySpread = -ySpread

                locationY = ((plan.MAXIMUM_PLAYGROUND_DISTANCE * y) + yOffset) + (plan.MAXIMUM_PLAYGROUND_DISTANCE * (y - 1)) + ySpread

                playground = Playground(locationX, locationY)

                if plan.correctlyPlaced(playground):
                    plan.playgrounds.append(playground)
                    assert len(plan.playgrounds)>0


        return plan

    def develop_ground_plan(self, width, height):
        plan = Groundplan(self.num_houses, self.enable_playground, name=self.name, width=width, height=height, puts=self.puts).deepCopy()

        plan = self.placeWater(plan, 1).deepCopy()

        if plan.PLAYGROUND:
            plan = self.placePlaygrounds(plan, 0).deepCopy()
            assert len(plan.playgrounds)>0

        return plan
