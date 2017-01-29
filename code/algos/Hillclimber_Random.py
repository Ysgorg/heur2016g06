from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from src.timeout import timeout


class HillClimber(object):
    name = "HillClimber"
    expects = ["Playgrounds", "Waterbodies"]
    puts = ["Residences"]

    def getPlan(self):
        return self.plan

    # input key to continue existing thread of evolution
    @timeout(3)
    def __init__(self, plan, constants, number_of_candidate_moves, frame=None):

        def best_among_candidates(plan, f, number_of_candidate_moves):
            best = None
            best_val = None
            for i in range(number_of_candidate_moves):
                h = f(random() * plan.WIDTH, random() * plan.HEIGHT)
                while not plan.correctlyPlaced(h): h = f(random() * plan.WIDTH, random() * plan.HEIGHT)
                temp = plan.deepCopy()
                temp.addResidence(h)
                val = temp.getPlanValue()
                if temp.isValid(): val *= 100
                if best is None or best_val < val:
                    best = h
                    best_val = val
            return best

        plan = plan.deepCopy()

        i = 0
        num_iterations = 0

        while num_iterations < constants['max_iterations'] and not plan.isValid() and len(
                plan.residences) < plan.NUMBER_OF_HOUSES:

            if i % 10 < 5:
                f = FamilyHome
            elif i % 10 < 8:
                f = Bungalow
            else:
                f = Mansion

            h = best_among_candidates(plan.deepCopy(), f, number_of_candidate_moves)
            plan.addResidence(h)

            if frame is not None: frame.repaint(plan)

            num_iterations += 1
            i += 1

        self.plan = plan
