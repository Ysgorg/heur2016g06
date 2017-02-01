from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame


def optimize_wb_side(plan, wb1):

    while plan.correctlyPlaced(wb1):
        while plan.correctlyPlaced(wb1):
            wb1.x1 -= 1
            wb1.x -= 1
            wb1.width +=1

        wb1.x += 1
        wb1.x1+=1
        wb1.width -=1

        wb1.x2 +=1
        wb1.width +=1
    wb1.x2 -= 1
    wb1.width -= 1
    return wb1


def in_corner(plan,x0, y0, x_dir, y_dir):
    x=x0+x_dir
    y=y0+y_dir
    frame = GroundplanFrame(plan)

    x_offset = 0
    y_offset = 0
    if x_dir == -0.1:x_offset = Mansion(0,0).width
    if y_dir == -0.1:y_offset = Mansion(0,0).height
    while not plan.correctlyPlaced(Mansion(x-x_offset,y-y_offset)):

        assert x >= 0
        assert y >= 0
        x+=x_dir
        y+=y_dir

    m = Mansion(x-x_offset,y-y_offset)

    while plan.correctlyPlaced(m):
        m.minimumClearance+=0.1
    else:
        m.minimumClearance-=0.1
    return m

def make_great_plan(frame):



    plan = Groundplan()

    r = plan.MAXIMUM_PLAYGROUND_DISTANCE + 11 # largest dimension


    dummy_pg=Playground(0,0)
    dummy_pg.flip()

    pg1 = Playground(r,r)

    pg2 = Playground(plan.WIDTH  - r- dummy_pg.width,plan.HEIGHT - r - dummy_pg.height)

    pg1.flip()
    pg2.flip()

    # fill corners with water

    assert plan.correctlyPlaced(pg1)
    assert plan.correctlyPlaced(pg2)

    plan.addPlayground(pg1)
    plan.addPlayground(pg2)

    wb_max_height = plan.HEIGHT - dummy_pg.height - r * 2.0
    wb__max_width = plan.WIDTH  - dummy_pg.width  - r * 2.0

    while max(wb__max_width,wb_max_height)/min(wb__max_width,wb_max_height) > 4.0:
        if wb__max_width > wb_max_height:
            wb__max_width-=0.1
            wb_max_height+=0.1
        else:
            wb__max_width+=0.1
            wb_max_height-=0.1

    wb1 = Waterbody(0,plan.HEIGHT-wb_max_height,wb__max_width,wb_max_height)
    wb2 = Waterbody(plan.WIDTH-wb__max_width,0,wb__max_width,wb_max_height)

    wb1 = optimize_wb_side(plan,wb1)
    wb2 = optimize_wb_side(plan,wb2)

    assert plan.correctlyPlaced(wb1)
    assert plan.correctlyPlaced(wb2)

    plan.addWaterbody(wb1)
    plan.addWaterbody(wb2)

    x_offset = Mansion(0,0).width

    plan.addResidence(in_corner(plan,wb1.x1,wb1.y1,0.1,-0.1))
    plan.addResidence(in_corner(plan,wb2.x1-Mansion(0,0).width,wb2.y2-Mansion(0,0).height,-0.1,0.1))
    plan.addResidence(in_corner(plan,plan.WIDTH,plan.HEIGHT,-0.1,-0.1))
    plan.addResidence(in_corner(plan,0,0,0.1,0.1))
    plan.addResidence(in_corner(plan,wb2.x2,wb2.y2,-0.1,0.1))
    plan.addResidence(in_corner(plan,wb1.x2,wb1.y1,0.1,-0.1))

    total_water_area = 0
    for i in plan.waterbodies: total_water_area+=i.width*i.height

    print 'put',int(total_water_area / (plan.AREA*plan.MINIMUM_WATER_PERCENTAGE)*100),'% of water'
    frame.repaint(plan)
    while True:pass
    return plan