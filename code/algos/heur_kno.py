from math import ceil
from time import sleep, time

from math import floor

from algos.Grid import Grid
from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan


def optimize_wb_side(plan, wb1):
    while plan.correctlyPlaced(wb1):
        while plan.correctlyPlaced(wb1):
            wb1.x1 -= 1
            wb1.width += 1

        wb1.x1 += 1
        wb1.width -= 1

        wb1.x2 += 1
        wb1.width += 1
    wb1.x2 -= 1
    wb1.width -= 1
    return wb1


def in_corner(plan, x0, y0, x_dir, y_dir):
    x = x0 + x_dir
    y = y0 + y_dir

    x_offset = 0
    y_offset = 0
    if x_dir == -0.1: x_offset = Mansion(0, 0).width
    if y_dir == -0.1: y_offset = Mansion(0, 0).height
    while not plan.correctlyPlaced(Mansion(x - x_offset, y - y_offset)):
        # print x,y
        assert x >= 0 and x < plan.WIDTH
        assert y >= 0 and y < plan.HEIGHT
        x += x_dir
        y += y_dir
    m = Mansion(x - x_offset, y - y_offset)
    assert plan.correctlyPlaced(m)

    while plan.correctlyPlaced(m):
        m.minimumClearance += 0.1
    else:
        m.minimumClearance -= 0.1

    assert plan.correctlyPlaced(m)

    return m


def grow_waterbodies(plan):

    wbs = plan.waterbodies
    plan.waterbodies = []

    for wb in wbs:

        # enlarge if possible
        for i in range(5):

            while plan.correctlyPlaced(Waterbody(wb.x1 - 1, wb.y1, wb.width + 1, wb.height)):
                wb.x1 -= 1
                wb.width += 1
            while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1, wb.width + 1, wb.height)):
                wb.x2 += 1
                wb.width += 1
            while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1 - 1, wb.width, wb.height + 1)):
                wb.y1 -= 1
                wb.height += 1
            while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1, wb.width, wb.height + 1)):
                wb.y2 += 1
                wb.height += 1

        plan.waterbodies.append(wb)



def make_great_plan(frame):

    init_time = time()
    plan = Groundplan(30)


    """ place playgrounds in corners A and C """
    r = plan.MAXIMUM_PLAYGROUND_DISTANCE + 11  # largest dimension

    dummy_pg = Playground(0, 0)
    dummy_pg.flip()

    pg1 = Playground(r, r)
    pg2 = Playground(plan.WIDTH - r - dummy_pg.width, plan.HEIGHT - r - dummy_pg.height)

    pg1.flip()
    pg2.flip()

    # fill corners with water

    assert plan.correctlyPlaced(pg1)
    assert plan.correctlyPlaced(pg2)

    plan.playgrounds.append(pg1)
    plan.playgrounds.append(pg2)

    """ place water bodies in corners B and D, outside playground reach """

    wb_max_height = plan.HEIGHT - dummy_pg.height - r * 2.0
    wb__max_width = plan.WIDTH - dummy_pg.width - r * 2.0

    while max(wb__max_width, wb_max_height) / min(wb__max_width, wb_max_height) > 4.0:
        if wb__max_width > wb_max_height:
            wb__max_width -= 0.1
            wb_max_height += 0.1
        else:
            wb__max_width += 0.1
            wb_max_height -= 0.1

    wb1 = optimize_wb_side(plan,  Waterbody(0, plan.HEIGHT - wb_max_height, wb__max_width, wb_max_height))
    wb2 = optimize_wb_side(plan, Waterbody(plan.WIDTH - wb__max_width, 0, wb__max_width, wb_max_height))

    assert plan.correctlyPlaced(wb1)
    assert plan.correctlyPlaced(wb2)

    plan.waterbodies.append(wb1)
    plan.waterbodies.append(wb2)

    """ place place mansions in all corners (beginning width B and D) """


    num_mansions = 0
    required_num_mansions = plan.MINIMUM_MANSION_PERCENTAGE * plan.NUMBER_OF_HOUSES
    per_corner = int((required_num_mansions-4)/2)
    grids = []


    corners = [
        [plan.WIDTH, 0, -0.1, 0.1,1], # high priority
        [0, plan.HEIGHT, 0.1, -0.1,1], # high priority
        [0, 0, 0.1, 0.1,0],
        [plan.WIDTH, plan.HEIGHT, -0.1, -0.1,0]
    ]

    for c in corners:

        if num_mansions >= required_num_mansions: break

        m = in_corner(plan, c[0], c[1], c[2], c[3])

        assert plan.correctlyPlaced(m)

        init_coords = [c[0], c[1]]

        m.minimumClearance = plan.compute_clearance(m)
        num_rows = 1
        if c[4] > 0:
            num_cols = 2
        else: num_cols = per_corner

        if num_mansions+num_rows*num_cols>required_num_mansions:break

        g = Grid(num_rows,num_cols, Mansion, m.minimumClearance, [0 if c[2]<0 else 1, 0 if c[3]<0 else 1], init_coords, plan)

        if c[4]<1:
            while g.expand(1.0):
                frame.repaint(plan)
                if g.residences[0].minimumClearance > 30: break
                pass

        for s in g.residences: assert plan.correctlyPlaced(s,verbose=False)
        grids.append(g)

        num_mansions += 1




    """ expand the two waterbodies as much as possible """

    grow_waterbodies(plan)

    total_water_area = sum([i.width * i.height for i in plan.waterbodies])

    """ assert everything is as expected """

    for g in grids: assert g.is_correct()

    print "took", (time() - init_time)*1000, 'ms'

    print 'put', int(total_water_area / (plan.AREA * plan.MINIMUM_WATER_PERCENTAGE) * 100), '% of water'
    if frame is not None: frame.repaint(plan)

    input('press any key to terminate')
    return plan
