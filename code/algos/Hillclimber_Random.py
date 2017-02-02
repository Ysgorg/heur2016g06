from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from src.timeout import timeout


class HillClimber(object):
    name = "HillClimber"
    expects = ["Playgrounds", "Waterbodies"]
    puts = ["Residences"]

    def getPlan(self): return self.plan

    def best_among_candidates(plan, f, number_of_candidate_moves,frame):
        best = None
        best_val = None
        for i in range(number_of_candidate_moves):
            #print i
            h = f(random() * plan.WIDTH, random() * plan.HEIGHT)
            while not plan.correctlyPlaced(h): h = f(random() * plan.WIDTH, random() * plan.HEIGHT)
            temp = plan.deepCopy()
            temp.residences.append(h)

            if frame is not None: frame.repaint(temp)
            val = temp.getPlanValue()
            if temp.isValid(): val *= 100
            if best is None or best_val < val:
                best = h
                best_val = val
        return best

    def decide_residence_type(self,i):
        if i % 10 < 5:    return FamilyHome
        elif i % 10 < 8:  return Bungalow
        else:             return Mansion

    # input key to continue existing thread of evolution
    @timeout(3)
    def __init__(self, plan, constants, number_of_candidate_moves, frame=None):
        plan = plan.deepCopy()
        i = 0
        while i < constants['max_iterations'] and not plan.isValid() and len(plan.residences) < plan.NUMBER_OF_HOUSES:
            f = self.decide_residence_type(i)
            h = self.best_among_candidates(plan.deepCopy(), f, number_of_candidate_moves,frame)
            plan.residences.append(h)
            if frame is not None: frame.repaint(plan)
            i += 1
        self.plan = plan
