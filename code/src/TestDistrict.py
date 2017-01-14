



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

        plan = Groundplan(40, True)
        dims = get_valid_water_dimensions(plan,1)
        plan = Groundplan(40,True)
        wb = Waterbody(0,0,dims[0],dims[1])
        plan.addWaterbody(wb)

        dummy_pg = Playground(0,0).flip()

        pgy = plan.HEIGHT/2 - dummy_pg.getHeight()/2
        pgx = plan.WIDTH/2 + dims[0]/2 - dummy_pg.getWidth()/2

        pg = Playground(pgx,pgy).flip()
        plan.addPlayground(pg)

        frame = GroundplanFrame(plan)
        frame.repaint(plan)

        return plan