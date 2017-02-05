from time import sleep

from districtobjects.Waterbody import Waterbody

def grow_waterbodies(plan,frame):

    wbs = plan.waterbodies
    plan.waterbodies = []

    def enough_water(plan,wb=None):
        wb_area = 0 if wb is None else wb.width*wb.height
        return (sum([i.width*i.height for i in plan.waterbodies])+wb_area)>=plan.MINIMUM_WATER_PERCENTAGE*plan.height*plan.width

    while not enough_water(plan):

        for wb in wbs:



            if enough_water(plan,wb):break
            for i in range(2):

                while plan.correctlyPlaced(Waterbody(wb.x1 - 1, wb.y1, wb.width + 1, wb.height)):
                    if enough_water(plan,wb):break
                    wb.x1 -= 1
                    wb.width += 1
                    if frame:
                        t = plan.deepCopy()
                        t.waterbodies.append(wb)
                        frame.repaint(t)
                while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1, wb.width + 1, wb.height)):
                    if enough_water(plan,wb):break
                    wb.x2 += 1
                    wb.width += 1

                    if frame:
                        t = plan.deepCopy()
                        t.waterbodies.append(wb)
                        frame.repaint(t)
                while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1 - 1, wb.width, wb.height + 1)):
                    if enough_water(plan,wb):break
                    wb.y1 -= 1
                    wb.height += 1

                    if frame:
                        t = plan.deepCopy()
                        t.waterbodies.append(wb)
                        frame.repaint(t)
                while plan.correctlyPlaced(Waterbody(wb.x1, wb.y1, wb.width, wb.height + 1)):

                    if enough_water(plan,wb):break
                    wb.y2 += 1
                    wb.height += 1

                    if frame:
                        t = plan.deepCopy()
                        t.waterbodies.append(wb)
                        frame.repaint(t)

            plan.waterbodies.append(wb)

    return plan
