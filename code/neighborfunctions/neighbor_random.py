from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion


def neighbor_random(state, temperature):
    def getTypeFunc(k):
        if k == "FamilyHome":
            return FamilyHome
        elif k == "Bungalow":
            return Bungalow
        elif k == "Mansion":
            return Mansion

    def findValidHouse(plan, type_to_place, pre):

        h = None

        while True:
            if pre is None or random() < 0.5:
                x = int(random() * plan.WIDTH)
                y = int(random() * plan.HEIGHT)
            else:
                x = int(pre.getX() - 5 + 10 * random())
                y = int(pre.getY() - 5 + 10 * random())

            f = getTypeFunc(type_to_place)

            h = f(x, y)

            if type_to_place == "FamilyHome":
                # not flipping because different
                if plan.correctlyPlaced(h):
                    return h

            if random() < 0.5:
                h = h.flip()
            if plan.correctlyPlaced(h):
                return h
            h = h.flip()
            if plan.correctlyPlaced(h):
                return h

        return h

    def mutateAHouse(plan):

        ind = int(random() * plan.getNumberOfHouses())

        toberemoved = plan.getResidence(ind)

        type_to_place = toberemoved.getType()

        plan.removeResidence(toberemoved)

        h = findValidHouse(plan, type_to_place, toberemoved)

        if h is not None:
            plan.addResidence(h)

        return [plan, h is not None]

    def randomSwap(plan):

        while True:

            i1 = int(random() * plan.getNumberOfHouses())
            i2 = int(random() * plan.getNumberOfHouses())
            if i1 != i2:
                temp = plan.deepCopy()
                r1 = temp.getResidence(i1)
                r2 = temp.getResidence(i2)
                f1 = getTypeFunc(r1.getType())
                f2 = getTypeFunc(r2.getType())
                n1 = f1(r2.getX(), r2.getY())
                n2 = f2(r1.getX(), r1.getY())
                temp.removeResidence(r1)
                temp.removeResidence(r2)
                if temp.correctlyPlaced(n1):
                    temp.addResidence(n1)
                    if temp.correctlyPlaced(n2):
                        temp.addResidence(n2)
                        return [temp, True]

    for i in range(int(random() * 10)):

        if random() < 0.5:
            res = randomSwap(state)
        else:

            try:
                res = mutateAHouse(state)
            except Exception:
                break
        if res[1]:
            state = res[0].deepCopy()
        else:
            print "invalid"

    return state
