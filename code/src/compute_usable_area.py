from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Bungalow import Bungalow

def compute_usable_area(plan):

    # returns the proportion of area of a plan which can potentially be covered by a residence

    bm = [[0 for x in range(plan.WIDTH)] for y in range(plan.HEIGHT)]

    for x in range(0,plan.WIDTH):
        for y in range(0,plan.HEIGHT):
            m = Mansion(x,y)
            b = Bungalow(x,y)
            h = FamilyHome(x,y)
            #print "correct?:",plan.correctlyPlaced(h)
            if plan.correctlyPlaced(h):

                try:
                    bm[x][y] = 1
                    bm[min(int(x+h.getWidth()),plan.WIDTH-2)][min(int(y+h.getHeight()),plan.HEIGHT-2)] = 1
                except Exception:pass
            if plan.correctlyPlaced(m):
                try:
                    bm[x][y] = 1
                    bm[min(int(x+m.getWidth()),plan.WIDTH-2)][min(int(y+h.getHeight()),plan.HEIGHT-2)] = 1
                except Exception:
                    pass
            if plan.correctlyPlaced(b):
                try:
                    bm[x][y] = 1
                    bm[min(int(x+b.getWidth()),plan.WIDTH-2)][min(int(y+b.getHeight()),plan.HEIGHT-2)] = 1
                except Exception:pass
    count = 0
    tot = plan.WIDTH*plan.HEIGHT
    for x in range(0,plan.WIDTH):
        for y in range(0,plan.HEIGHT):
            try:
                count+=bm[x][y]
            except Exception:
                tot-=1

    return float(count)/tot
