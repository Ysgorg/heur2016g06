import time
from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

from src.DistrictPlanner import DistrictPlanner
from src.ConfigLogger import ConfigLogger

#
class Evolver(object):

    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True
    LOG_KEY = "evolver"
    ITERATIONS_BEFORE_RESET = 30

    def findValidHouse(self, plan, type_to_place):

        iterations_since_last_success = 0

        h = None

        while True:
            x = int(random() * plan.WIDTH)
            y = int(random() * plan.HEIGHT)

            if type_to_place is "FamilyHome":   h = FamilyHome(x, y)
            elif type_to_place is "Bungalow":   h = Bungalow(x, y)
            if type_to_place is "Mansion":      h = Mansion(x, y)

            if (type_to_place != "FamilyHome" # because FamilyHome has w==h
                and random() < 0.5): h = h.flip()
            if plan.correctlyPlaced(h): break
            elif type_to_place != "FamilyHome": # because FamilyHome has w==h
                h = h.flip()
                if plan.correctlyPlaced(h): break
            iterations_since_last_success += 1

        return h


    def mutateWater(self,plan):

        # get number of water bodies
        num_wbs = len(plan.getWaterbodies())

        # remove a random water body
        if num_wbs > 0:
            plan.removeWaterbody(plan.getWaterbodies()[int(random() * num_wbs)])
            num_wbs -= 1

        # dimensions of water bodies
        v1 = int(plan.WIDTH / 4)
        v2 = int(plan.HEIGHT / 5)

        # try many times to place wbs until 4 have been placed
        while True:

            if num_wbs >= 4: break

            x = int(random() * plan.WIDTH)
            y = int(random() * plan.HEIGHT)

            # randomly decide rotation
            if random() < 0.5: wb = Waterbody(x, y, v1, v2)
            else: wb = Waterbody(x, y, v2, v1)

            if plan.correctlyPlaced(wb):
                plan.addWaterbody(wb)
                num_wbs+=1

        return plan

    def getOrMakePlan(self,key):

        if ConfigLogger().exists(key):return ConfigLogger.loadConfig(key)
        else:
            ConfigLogger().createConfigLog(key)
            return DistrictPlanner().developGroundplan()

    def mutateAHouse(self,plan,i):

        if plan.getNumberOfHouses() is self.NUMBER_OF_HOUSES:
            ind = int(random() * self.NUMBER_OF_HOUSES)
            toberemoved = plan.getResidence(ind)
            type_to_place = toberemoved.getType()
            plan.removeResidence(toberemoved)

        else:
            if i % 10 < 5:type_to_place = "FamilyHome"
            elif i % 10 < 8:type_to_place = "Bungalow"
            else:type_to_place = "Mansion"

        h = self.findValidHouse(plan,type_to_place)

        if h is not None: plan.addResidence(h)

        return [plan,h is not None]

    # input key to continue existing thread of evolution
    def __init__(self, key="test", visualize=True):

        i = 0
        deaths = 0

        # generate a new plan or load plan from previous run (continue previous evolution)
        plan = self.getOrMakePlan(key)

        # init vars to remember the best plan found so far and it's value
        best_val = plan.getPlanValue()

        # init visualizers. disable for higher performance
        if visualize:
            frame = GroundplanFrame(plan) # window for current plan
            best_frame = GroundplanFrame(plan) # window for the best plan so far
            best_frame.repaint(plan)

        iterations_since_best = 0 # number of iterations since plan==best_plan

        while True:

            # mutate
            plan = self.mutateWater(plan)
            res = self.mutateAHouse(plan,i)
            if res[1]: # if succeeded in house mutation
                plan = res[0]
                i+=1

            if plan.isValid():

                iterations_since_best += 1

                if plan.getPlanValue() > best_val:
                    print "[+]\t",round(best_val),'\t->\t',round(plan.getPlanValue()),',\t',deaths,'\t',iterations_since_best
                    best_val = plan.getPlanValue()
                    if visualize: best_frame.repaint(plan)
                    iterations_since_best = 0
                    deaths = 0
                    ConfigLogger.appendToConfigLog(key, plan, {"mutations":iterations_since_best,"deaths":deaths})

                elif iterations_since_best > self.ITERATIONS_BEFORE_RESET:
                    # no better plan was found. return to previous best
                    plan = self.getOrMakePlan(key)
                    deaths +=1
                    iterations_since_best = 0

                if visualize: frame.repaint(plan)