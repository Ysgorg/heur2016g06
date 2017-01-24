from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from src.timeout import timeout


class algo_Evolver(object):
    ITERATIONS_BEFORE_RESET = 1

    @staticmethod
    @timeout(1)
    def findValidHouse(plan, type_to_place, pre):

        h = None

        tries = 0

        while True:

            if pre is None or random() < 0.5:
                x = int(random() * plan.WIDTH)
                y = int(random() * plan.HEIGHT)
            else:
                x = int(pre.getX() - 5 + 10 * random())
                y = int(pre.getY() - 5 + 10 * random())

            if type_to_place is "FamilyHome":
                # skip flipping because FamilyHome has w==h
                h = FamilyHome(x, y)
                h.minimumClearance = pre.minimumClearance

                if plan.correctlyPlaced(h,"extraroom"): return h

            elif type_to_place is "Bungalow":
                h = Bungalow(x, y)
            elif type_to_place is "Mansion":
                h = Mansion(x, y)

            h.minimumClearance = pre.minimumClearance

            if random() < 0.5: h = h.flip()
            if plan.correctlyPlaced(h,"extraroom"): break
            h = h.flip()
            if plan.correctlyPlaced(h,"extraroom"): break
            tries += 1
            if tries > 100:break
        return h

    def mutateAHouse(self, plan, i):

        ind = int(random() * plan.NUMBER_OF_HOUSES)
        toberemoved = plan.getResidence(ind)
        type_to_place = toberemoved.getType()
        plan.removeResidence(toberemoved)

        h = self.findValidHouse(plan, type_to_place, toberemoved)

        if h is not None: plan.addResidence(h)

        return [plan, h is not None]

    def getPlan(self): return self.plan

    # input key to continue existing thread of evolution
    #@timeout(1)
    def __init__(self, base, max_iterations=100000,frame=None):

        iterations = 0

        i = 0

        # generate a new plan or load plan from previous run (continue previous evolution)
        plan = base.deepCopy()

        while True:
            print i
            res = self.mutateAHouse(plan, i)
            if res[1]:  # if succeeded in house mutation
                if res[0].isValid() and res[0].getPlanValue() > plan.getPlanValue():
                    plan = res[0].deepCopy()
                    frame.repaint(plan)
            iterations += 1
            if max_iterations < iterations:
                break
            i+=1

        self.plan = plan