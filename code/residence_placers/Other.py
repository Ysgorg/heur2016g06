from time import time, sleep

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from useful_scripts.Grid import Grid
from useful_scripts.grow_waterbodies import grow_waterbodies
from useful_scripts.place_grid_in_corner import corner_grid


def get_req_num_residences(plan,r):

    if r is Mansion : return plan.MINIMUM_MANSION_PERCENTAGE * plan.NUMBER_OF_HOUSES
    if r is Bungalow : return plan.MINIMUM_BUNGALOW_PERCENTAGE* plan.NUMBER_OF_HOUSES
    if r is FamilyHome : return plan.MINIMUM_FAMILYHOMES_PERCENTAGE * plan.NUMBER_OF_HOUSES


def place_wbs(plan):

    wb1 = Waterbody(0, plan.height - 2, 1, 1)
    wb2 = Waterbody(plan.width - 2, 0, 1, 1)

    assert plan.correctlyPlaced(wb1)
    assert plan.correctlyPlaced(wb2)

    plan.waterbodies.append(wb1)
    plan.waterbodies.append(wb2)
    return plan


def place_pgs(plan):
    """ place playground seeds in corners A and C """
    r = plan.MAXIMUM_PLAYGROUND_DISTANCE + 11  # largest dimension

    dummy_pg = Playground(0, 0)
    dummy_pg.flip()

    pg1 = Playground(r, r)
    pg2 = Playground(plan.width - r - dummy_pg.width, plan.height - r - dummy_pg.height)

    pg1.flip()
    pg2.flip()

    # fill corners with water

    assert plan.correctlyPlaced(pg1)
    assert plan.correctlyPlaced(pg2)

    plan.playgrounds.append(pg1)
    plan.playgrounds.append(pg2)
    return plan


def place_mansion_rows_in_corners(plan,frame,slow):



    grids = []

    corners = [
        [Mansion,   float(plan.width-1), 0.0,           -1, 1, 1],  # high priority
        [Mansion,   0.0,        float(plan.height),    1,-1, 1],  # high priority
        [Mansion,   0.0,        0.0,            1, 1, 0],
        [Mansion,   float(plan.width), float(plan.height),   -1,-1, 0]
    ]

    for c in corners:

        grid = corner_grid(plan,c[0],1,2+c[5],c[1],c[2],c[3],c[4],frame,slow)
        if grid is False: continue
        try:
            assert len(grid.residences)>0
            assert len(grid.residences[0])>0
            grids.append(grid)
        except: pass
    return grids


def doit(frame,num,slow):

    init_time = time()

    plan = Groundplan(num)
    if frame:
        frame.repaint(plan)
        if slow: sleep(0.2)
    plan = place_pgs(plan)
    if frame:
        frame.repaint(plan)
        if slow: sleep(0.2)
    plan = place_wbs(plan)
    if frame:
        frame.repaint(plan)
        if slow: sleep(0.2)

    grids = [g for g in place_mansion_rows_in_corners(plan,frame,slow) if g is not False] # filter out Falses
    if frame:
        frame.repaint(plan)
        if slow: sleep(0.2)
    print len(grids)
    for g in grids:
        while g.expand():
            frame.repaint(plan)


    plan.waterbodies.append(Waterbody(139,48,1,1))
    plan.waterbodies.append(Waterbody(46,120,1,1))

    num_to_place = [get_req_num_residences(plan,R) for R in [FamilyHome,Bungalow,Mansion]]

    if frame:
        frame.repaint(plan)
        if slow: sleep(1)

    grow_waterbodies(plan,frame)

    """ assert everything is as expected"""

    print "took", (time() - init_time) * 1000, 'ms'
    print 'put', int(sum([i.width * i.height for i in plan.waterbodies]) / (plan.AREA * plan.MINIMUM_WATER_PERCENTAGE) * 100), '% of water'
    print 'valid:',plan.isValid()
    if frame is not None: frame.repaint(plan)

    return plan


def make_great_plan(frame,slow):
    for nh in [(i+1)*10 for i in range(10)]:
        print 'num houses:',nh
        doit(frame,nh,slow)
        sleep(1)
