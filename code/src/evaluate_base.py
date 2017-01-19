from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow


def evaluate_base(plan, visualize=True):
    # returns the proportion of area of a plan which can potentially be covered by a residence

    bm = [[0 for y in range(plan.HEIGHT)] for x in range(plan.WIDTH)]

    for x in range(0, plan.WIDTH):
        for y in range(0, plan.HEIGHT):
            m = Mansion(x, y)
            b = Bungalow(x, y)
            h = FamilyHome(x, y)

            if plan.correctlyPlaced(h):
                bm[x][y] = 1
                #bm[min(int(x + h.getWidth()), plan.WIDTH - 1)][min(int(y + h.getHeight()), plan.HEIGHT - 1)] = 1

            if plan.correctlyPlaced(m):
                bm[x][y] = 1
               # bm[min(int(x + m.getWidth()), plan.WIDTH - 1)][min(int(y + m.getHeight()), plan.HEIGHT - 1)] = 1

            if plan.correctlyPlaced(b):
                bm[x][y] = 1
                #bm[min(int(x + b.getWidth()), plan.WIDTH - 1)][min(int(y + b.getHeight()), plan.HEIGHT - 1)] = 1

    count = 0
    tot = plan.WIDTH * plan.HEIGHT
    for x in range(plan.WIDTH):
        for y in range(plan.HEIGHT):
            count += bm[x][y]

    useful_proportion = float(count) / tot
    print useful_proportion

    if visualize:

        from GroundplanFrame import GroundplanFrame
        frame = GroundplanFrame(plan)
        frame.repaint(plan)

        for x in range(plan.WIDTH):
            for y in range(plan.HEIGHT):
                if bm[x][y]: frame.mark(x, y, 'black')

        frame.updateit()

    return useful_proportion
