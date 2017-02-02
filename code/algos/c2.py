from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan

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

    x_offset = 0
    y_offset = 0
    if x_dir == -0.1:x_offset = Mansion(0,0).width
    if y_dir == -0.1:y_offset = Mansion(0,0).height
    while not plan.correctlyPlaced(Mansion(x-x_offset,y-y_offset)):
        #print x,y
        assert x >= 0 and x < plan.WIDTH
        assert y >= 0 and y < plan.HEIGHT
        x+=x_dir
        y+=y_dir

    m = Mansion(x-x_offset,y-y_offset)

    while plan.correctlyPlaced(m):
        m.minimumClearance+=0.1
    else:
        m.minimumClearance-=0.1
    return m

def make_great_plan(frame):



    plan = Groundplan(100)

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
    print plan.waterbodies

    corners = [
        [0,0,0.1,0.1],
        [plan.WIDTH,0,-0.1,0.1],
        [0,plan.HEIGHT,0.1,-0.1],
        [plan.WIDTH,plan.HEIGHT,-0.1,-0.1]
    ]

    num_mansions=0


    print num_mansions
    for c in corners:
        if num_mansions >= plan.MINIMUM_MANSION_PERCENTAGE * plan.NUMBER_OF_HOUSES:
            break
        print num_mansions
        try:
            m = in_corner(plan,c[0],c[1],c[2],c[3])

            print m.x1,m.x2,m.y1,m.y2
            print c[2],c[3]

            if c[2]>0:
                new_x = m.x2+m.minimumClearance
                new_x_dir = c[2]
            elif c[2] < 0:
                new_x = m.x1-m.minimumClearance
                new_x_dir = c[2]
            else:
                new_x = m.x1
                new_x_dir = 0

            new_y = m.y1
            new_y_dir = 0

            corners.append([new_x,new_y,new_x_dir,new_y_dir])
            plan.addResidence(m)
        except Exception:
            pass
        num_mansions+=1

    wbs = plan.waterbodies
    plan.waterbodies = []

    print wbs,plan.waterbodies

    for wb in wbs:
        print 'aaa'
        # enlarge if possible
        for i in range(5):
            print i
            while plan.correctlyPlaced(Waterbody(wb.x1-1,wb.y1,wb.width+1,wb.height)):
                wb.x-=1
                wb.x1-=1
                wb.width+=1
            while plan.correctlyPlaced(Waterbody(wb.x1,wb.y1,wb.width+1,wb.height)):
                wb.width+=1
                wb.x2+=1
            while plan.correctlyPlaced(Waterbody(wb.x1,wb.y1-1,wb.width,wb.height+1)):
                wb.y-=1
                wb.y1-=1
                wb.height+=1
            while plan.correctlyPlaced(Waterbody(wb.x1,wb.y1,wb.width,wb.height+1)):
                wb.y2+=1
                wb.height+=1

        plan.addWaterbody(wb)


    frame.repaint(plan)
    while True: pass
    total_water_area = 0
    for i in plan.waterbodies: total_water_area+=i.width*i.height

    print 'put',int(total_water_area / (plan.AREA*plan.MINIMUM_WATER_PERCENTAGE)*100),'% of water'
    frame.repaint(plan)
    while True:pass
    return plan