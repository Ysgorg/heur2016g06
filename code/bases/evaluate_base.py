from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion


def evaluate_base(plan, frame):
    # returns the proportion of area of a plan which can potentially be
    # covered by a residence

    bm = [[0 for y in range(plan.HEIGHT)] for x in range(plan.WIDTH)]

    for x in range(0, plan.WIDTH):
        for y in range(0, plan.HEIGHT):
            m = Mansion(x, y)
            b = Bungalow(x, y)
            h = FamilyHome(x, y)

            if plan.correctlyPlaced(h):
                bm[x][y] = 1
                bm[min(int(x + h.width), plan.WIDTH - 1)][
                    min(int(y + h.height), plan.HEIGHT - 1)] = 1

            if plan.correctlyPlaced(m):
                bm[x][y] = 1
                bm[min(int(x + m.width), plan.WIDTH - 1)][
                    min(int(y + m.height), plan.HEIGHT - 1)] = 1

            if plan.correctlyPlaced(b):
                bm[x][y] = 1
                bm[min(int(x + b.width), plan.WIDTH - 1)][
                    min(int(y + b.height), plan.HEIGHT - 1)] = 1

    count = 0
    tot = plan.WIDTH * plan.HEIGHT
    for x in range(plan.WIDTH):
        for y in range(plan.HEIGHT):
            count += bm[x][y]

    useful_proportion = float(count) / tot

    print "Useful proportion:", useful_proportion, "Count:", count

    if frame is not None:

        frame.repaint(plan)

        for x in range(plan.WIDTH):
            for y in range(plan.HEIGHT):
                if bm[x][y]:
                    frame.mark(x, y, 'black')

        frame.updateit()

    return useful_proportion
