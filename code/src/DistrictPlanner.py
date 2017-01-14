from random import random

from math import ceil

from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

PLAYGROUND_RADIUS = Groundplan.MAXIMUM_PLAYGROUND_DISTANCE

# Coordinate offset from origin
X_OFFSET = -5
Y_OFFSET = 0

# I didn't know what to name this. It shifts the playgrounds in the first half of the x-axis by the given value, allowing for diagonal placement
Y_INVERT = 0

# Spreading buildings from center towards the edge
X_SPREAD = 5
Y_SPREAD = 5

PLAYGROUND_WIDTH = 30
PLAYGROUND_HEIGHT = 20

# Neccecsary water as a percentage out of 1
TOTAL_WATER = 0.2
MAX_WATER_BODIES = 10

class DistrictPlanner(object):
    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True

    def __init__(self):
        self.plan = self.developGroundplan()
       # self.frame = GroundplanFrame(self.plan)
       # self.frame.setPlan()

#        self.frame.root.mainloop()

    def placeWater(self, plan):
        bestArea = (plan.WIDTH * plan.HEIGHT * TOTAL_WATER * 1.2) # Worst case area to consider (1.2 * requirement as arbitrary upper bound)
        req_area = plan.WIDTH * plan.HEIGHT * TOTAL_WATER # Best case / Minimum required area
        print "Required water area:", req_area

        for j in range(1, MAX_WATER_BODIES+1):
            for i in range(1, plan.WIDTH):
                width = i
                height = width/4
                area = width*height
                if (area >= req_area and area < bestArea):
                    bestArea = area
                    bestWidth = width
                    bestHeight = height
                    noWaterBodies = j
                    print "New best water distribution found! [", noWaterBodies, "bodies,", bestWidth, "width,", bestHeight, "height,", bestArea, "area ]"

        # Starting position
        x = 0
        y = plan.HEIGHT - bestHeight

        for i in range(1, noWaterBodies+1):
          wb = Waterbody(x, y, bestWidth, bestHeight)

          if plan.correctlyPlaced(wb):
            plan.addWaterbody(wb)
            print "Waterbody", i, "placed"
            x += bestWidth+1 # +1 so that the bodies are not touching

        return plan

    def placePlaygrounds(self, plan):
        # Reach is defined by the the playground size, plus its usable radius
        playgroundReachX = PLAYGROUND_WIDTH + PLAYGROUND_RADIUS
        playgroundReachY = PLAYGROUND_HEIGHT + PLAYGROUND_RADIUS
        print "Playground reach:", playgroundReachX, ",", playgroundReachY

        utilisableX = plan.WIDTH
        utilisableY = plan.HEIGHT * TOTAL_WATER

        print "Utilisable area:", utilisableX, "x", utilisableY, "=", utilisableX * utilisableY

        # Floor the total utiliable width and height by our playground reach to find optimal number to fit
        #numberPlaygroundsX = int(utilisableX) // playgroundReachX
        #numberPlaygroundsY = int(utilisableY) // playgroundReachY

        # Ceil the total utilisable width and height by our playground reach to find optimal number to fit
        numberPlaygroundsX = int(ceil(utilisableX / playgroundReachX))
        numberPlaygroundsY = int(ceil(utilisableY / playgroundReachY))
        totalPlaygrounds = numberPlaygroundsX * numberPlaygroundsY

        print "Total utilisable playgrounds:", totalPlaygrounds, numberPlaygroundsX, "x", numberPlaygroundsY, "\n"

        for x in range(1, numberPlaygroundsX + 1):
            xSpread = X_SPREAD
            yOffset = Y_OFFSET

            if x <= numberPlaygroundsX / 2:  # if x is in the lower half, invert the offset
                xSpread = -xSpread
                yOffset += Y_INVERT

            locationX = ((PLAYGROUND_RADIUS * x) + X_OFFSET) + (PLAYGROUND_WIDTH * (x - 1)) + xSpread

            for y in range(1, numberPlaygroundsY + 1):
                ySpread = Y_SPREAD

                if y <= numberPlaygroundsY / 2:  # if y is in the lower half, invert the offset
                    ySpread = -ySpread

                locationY = ((PLAYGROUND_RADIUS * y) + yOffset) + (PLAYGROUND_HEIGHT * (y - 1)) + ySpread

                print "Location:", x, "x", y, "\nCoordinates:", locationX, ",", locationY, "\n"
                plan.addPlayground(Playground(locationX, locationY))

        return plan

    def developGroundplan(self):
        plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        self.placePlaygrounds(plan)
        self.placeWater(plan)
        return plan
