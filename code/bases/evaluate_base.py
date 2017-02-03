from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion


def evaluate_base(plan, frame):
    # returns the proportion of area of a plan which can potentially be
    # covered by a residence

    bm = [[0 for y in range(plan.height)] for x in range(plan.width)]

    for x in range(0, plan.width):
        for y in range(0, plan.height):
            m = Mansion(x, y)
            b = Bungalow(x, y)
            h = FamilyHome(x, y)

            if plan.correctlyPlaced(h):
                bm[x][y] = 1
                bm[min(int(x + h.width), plan.width - 1)][
                    min(int(y + h.height), plan.height - 1)] = 1

            if plan.correctlyPlaced(m):
                bm[x][y] = 1
                bm[min(int(x + m.width), plan.width - 1)][
                    min(int(y + m.height), plan.height - 1)] = 1

            if plan.correctlyPlaced(b):
                bm[x][y] = 1
                bm[min(int(x + b.width), plan.width - 1)][
                    min(int(y + b.height), plan.height - 1)] = 1

    count = 0
    tot = plan.width * plan.height
    for x in range(plan.width):
        for y in range(plan.height):
            count += bm[x][y]

    useful_proportion = float(count) / tot

    print "Useful proportion:", useful_proportion, "Count:", count

    if frame is not None:

        frame.repaint(plan)

        for x in range(plan.width):
            for y in range(plan.height):
                if bm[x][y]:
                    frame.mark(x, y, 'black')

        frame.updateit()

    return useful_proportion
