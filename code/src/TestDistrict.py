



import math

from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame


def get_valid_water_dimensions(plan, num_bodies):
    # input plan and desired number of water bodies
    # output the dimensions that give exactly MINIMUM_WATER_PERCENTAGE
    x = math.sqrt(((plan.HEIGHT * plan.WIDTH * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies )/ 4 )
    return [x,x*4]

class TestDistrict(object):

    def __init__(self):
        pass

    def developGroundplan(self):


        flip = False


        plan = Groundplan(40, True)
        dims = get_valid_water_dimensions(plan,1)
        plan = Groundplan(40,True)
        wb = Waterbody(0,0,dims[0],dims[1])
        plan.addWaterbody(wb)

        dummy_pg = Playground(0,0)
        if flip: dummy_pg=dummy_pg.flip()

        pgy1 = plan.HEIGHT/3 - dummy_pg.getHeight()/2
        pgy2 = plan.HEIGHT/3*2 - dummy_pg.getHeight()/2

        pgx = plan.WIDTH/2 + dims[0]/2 - dummy_pg.getWidth()/2

        factor = 5

        pg1 = Playground(pgx+factor,pgy1+factor)
        if flip: pg1=pg1.flip()
        plan.addPlayground(pg1)
        pg2 = Playground(pgx-factor,pgy2-factor)
        if flip: pg2=pg2.flip()
        plan.addPlayground(pg2)

        frame = GroundplanFrame(plan)
        from districtobjects.FamilyHome import FamilyHome
        from districtobjects.Bungalow import Bungalow
        from districtobjects.Mansion import Mansion
        frame.repaint(plan)

        for x in range(1,500):
            for y in range(1,500):
                m = Mansion(x,y)
                b = Bungalow(x,y)
                h = FamilyHome(x,y)
                #print "correct?:",plan.correctlyPlaced(h)
                if plan.correctlyPlaced(h):
                    frame.mark(x+7.5,y+7.5,h.color)
                if plan.correctlyPlaced(m):
                    frame.mark(x+13,y+13,m.color)
                if plan.correctlyPlaced(b):
                    frame.mark(x+10,y+10,b.color)

        frame.updateit()
        while True:pass
        return plan