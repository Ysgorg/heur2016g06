import math

from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan


def get_valid_water_dimensions(plan, num_bodies):
    # input plan and desired number of water bodies
    # output the dimensions that give exactly MINIMUM_WATER_PERCENTAGE
    x = math.sqrt(((plan.HEIGHT * plan.WIDTH * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies) / 4)
    return [x, x * 4]


class base_b(object):
    def __init__(self):
        pass

    @staticmethod
    def developGroundplan():

        flip = False

        plan = Groundplan(40, True)
        dims = get_valid_water_dimensions(plan, 1)
        plan = Groundplan(40, True)
        wb = Waterbody(0, 0, dims[0], dims[1])
        plan.addWaterbody(wb)

        dummy_pg = Playground(0, 0)
        if flip: dummy_pg = dummy_pg.flip()

        pgy1 = plan.HEIGHT / 3 - dummy_pg.getHeight() / 2
        pgy2 = plan.HEIGHT / 3 * 2 - dummy_pg.getHeight() / 2

        pgx = plan.WIDTH / 2 + dims[0] / 2 - dummy_pg.getWidth() / 2

        factor = 5

        pg1 = Playground(pgx + factor, pgy1 + factor)
        if flip: pg1 = pg1.flip()
        plan.addPlayground(pg1)
        pg2 = Playground(pgx - factor, pgy2 - factor)
        if flip: pg2 = pg2.flip()
        plan.addPlayground(pg2)

        return plan
