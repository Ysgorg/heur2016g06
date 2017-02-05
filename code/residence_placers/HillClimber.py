from random import random
from time import sleep

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from src.Groundplan import Groundplan


def getTypeFunc(k):
    if k == "FamilyHome":
        return FamilyHome
    elif k == "Bungalow":
        return Bungalow
    elif k == "Mansion":
        return Mansion


def findValidHouse(plan, f, pre):
    h = None

    for count in range(100):
        if pre is None or random() < 0.5:
            x = int(random() * plan.width)
            y = int(random() * plan.height)
        else:
            x = int(pre.x1 - 5 + 10 * random())
            y = int(pre.y1 - 5 + 10 * random())

        h = f(x, y)
        if f is FamilyHome:
            # not flipping because different
            if plan.correctlyPlaced(h):
                return h

        if random() < 0.5:
            h = h.flip()
        if plan.correctlyPlaced(h): return h
        h = h.flip()
        if plan.correctlyPlaced(h): return h

    return None


def mutateAHouse(plan):
    ind = int(random() * len(plan.residences))

    toberemoved = plan.residences[ind]

    type_to_place = type(toberemoved)

    plan.removeResidence(toberemoved)

    h = findValidHouse(plan, type_to_place, toberemoved)

    assert plan.correctlyPlaced(h)

    if h is not None: plan.addResidence(h)

    return plan


def randomSwap(plan):
    for i in range(100):

        i1 = int(random() * len(plan.residences))
        i2 = int(random() * len(plan.residences))
        if i1 != i2:
            temp = plan.deepCopy()
            r1 = temp.residences[i1]
            r2 = temp.residences[i2]
            f1 = type(r1)
            f2 = type(r1)
            n1 = f1(r2.x1, r2.y1)
            n2 = f2(r1.x1, r1.y1)
            temp.removeResidence(r1)
            temp.removeResidence(r2)
            if temp.correctlyPlaced(n1):
                temp.addResidence(n1)
                if temp.correctlyPlaced(n2):
                    temp.addResidence(n2)
                    return temp


class HillClimber(object):
    name = "HillClimber"
    expects = ["Playgrounds", "Waterbodies"]
    puts = ["Residences"]

    iteration_value_rows = []

    def getPlan(self):
        return self.plan

    def best_among_candidates(self, plan, f, number_of_candidate_moves, frame,slow):

        best = None
        for i in range(number_of_candidate_moves):
            if len(plan.residences) < plan.NUMBER_OF_HOUSES:
                h = findValidHouse(plan.deepCopy(), self.decide_residence_type(len(plan.residences)), None)
                if h is not None:
                    assert plan.correctlyPlaced(h)
                    candidate = plan.deepCopy()
                    candidate.addResidence(h)
                else:
                    candidate = None
            else:
                candidate = (randomSwap(plan.deepCopy()) if random() < 0.5 else mutateAHouse(plan.deepCopy()))

            if candidate is None: continue
            if frame is not None:
                assert isinstance(candidate, Groundplan)
                frame.repaint(candidate)
                if slow:
                    sleep(0.1)

            assert isinstance(candidate, Groundplan)

            if best is None or (
                            best.isValid() and candidate.isValid() and candidate.getPlanValue() > best.getPlanValue()) \
                    or (not best.isValid() and (candidate.isValid() or candidate.getPlanValue() > best.getPlanValue())):
                best = candidate


        return best

    @staticmethod
    def decide_residence_type(i):
        if i % 10 < 5:
            return FamilyHome
        elif i % 10 < 8:
            return Bungalow
        else:
            return Mansion

    def __init__(self, plan, constants, frame=None,slow=False):
        plan = plan.deepCopy()
        i = 0

        while i < constants['max_iterations'] and not plan.isValid() and len(plan.residences) < plan.NUMBER_OF_HOUSES:
            f = self.decide_residence_type(i)
            r = self.best_among_candidates(plan.deepCopy(), f, constants['number_of_candidate_moves'], frame,slow)
            if r is not None: plan = r
            self.iteration_value_rows.append(plan.getPlanValue())
            if frame is not None: frame.repaint(plan)
            i += 1

        self.plan = plan
