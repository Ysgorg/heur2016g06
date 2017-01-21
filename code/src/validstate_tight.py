from random import random

import time

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody

# a modified evolver, returns first valid solution it finds
from src.GroundplanFrame import GroundplanFrame


class validstate_tight(object):
    # input key to continue existing thread of evolution

    def getPlan(self):
        return self.plan


    def genPlan(self,timeout):

        def next_to_place(i):
            v = i%10
            if v<5 : return FamilyHome
            elif v<8 : return Bungalow
            else: return Mansion

        i = 0
        r = next_to_place(i)
        x=0
        frame = GroundplanFrame(self.plan)

        while x < self.plan.WIDTH:
            y=0
            while y < self.plan.HEIGHT:

                r1 = r(x,y)
                if self.plan.correctlyPlaced(r1):
                    x1 = x
                    r2 = r(x1,y)
                    while self.plan.correctlyPlaced(r2):
                        x1 -= 1
                        r2 = r(x1,y)
                    x1+=1

                    self.plan.addResidence(r(x1,y))
                    #frame.repaint(self.plan)
                    if self.plan.NUMBER_OF_HOUSES == self.plan.getNumberOfHouses():
                        return
                    y+=r1.height
                    i+=1
                    r = next_to_place(i)
                else: y+=1
            x+=1

    def __init__(self, plan,timeout):

        self.plan = plan
        self.genPlan(timeout)

        i = 0
