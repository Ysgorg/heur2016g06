from random import random

from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground

PLAYGROUND_RADIUS = Groundplan.MAXIMUM_PLAYGROUND_DISTANCE

# Coordinate offset from origin
X_OFFSET = -5
Y_OFFSET = -10

# Spreading buildings from center towards the edge
X_SPREAD = 10
Y_SPREAD = 10

PLAYGROUND_WIDTH = 30
PLAYGROUND_HEIGHT = 20

class DistrictPlanner(object):
    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True

    def __init__(self):
        self.plan = self.developGroundplan()
        self.frame = GroundplanFrame(self.plan)
        self.frame.setPlan()

        self.frame.root.mainloop()

    def placePlaygrounds(self, plan):
        print self, plan

        # Reach is defined by the the playground size, plus its usable radius
        playgroundReachX = PLAYGROUND_WIDTH + PLAYGROUND_RADIUS
        playgroundReachY = PLAYGROUND_HEIGHT + PLAYGROUND_RADIUS
        print "Playground reach:", playgroundReachX,",", playgroundReachY

        # Floor the total width and height by our playground reach to find optimal number to fit
        numberPlaygroundsX = plan.WIDTH // playgroundReachX
        numberPlaygroundsY = plan.HEIGHT // playgroundReachY
        totalPlaygrounds = numberPlaygroundsX * numberPlaygroundsY

        print "Total fully utilisable playgrounds:", totalPlaygrounds, "\n"

        for x in range(1, numberPlaygroundsX + 1):
            xSpread = X_SPREAD

            if (x <= numberPlaygroundsX/2): # if x is in the lower half, invert the offset
                xSpread = -xSpread

            locationX = ((PLAYGROUND_RADIUS * x) + X_OFFSET) + (PLAYGROUND_WIDTH * (x-1)) + xSpread

            for y in range(1, numberPlaygroundsY + 1):
                ySpread = Y_SPREAD

                if (y <= numberPlaygroundsY/2): # if y is in the lower half, invert the offset
                    ySpread = -ySpread

                locationY = ((PLAYGROUND_RADIUS * y) + Y_OFFSET) + (PLAYGROUND_HEIGHT * (y-1)) + ySpread

                print "Location:", x, "x", y, "\nCoordinates:", locationX, ",", locationY, "\n"
                plan.addPlayground(Playground(locationX, locationY))

        return plan

    def developGroundplan(self):
        plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.placePlaygrounds(plan)

        i = 0
        attempts = 0
        while (i < self.NUMBER_OF_HOUSES):
            attempts += 1
            x = 10 + random() * (plan.WIDTH - 50)
            y = 10 + random() * (plan.HEIGHT - 50)
            house = FamilyHome(x, y)
            if (plan.correctlyPlaced(house)):
                plan.addResidence(house)
                i += 1

        print "Placement attempts:", attempts

        return plan
