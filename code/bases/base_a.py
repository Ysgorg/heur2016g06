from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan


class base_a(object):
    def __init__(self, enable_playground, num_houses):
        self.enable_playground = enable_playground
        self.num_houses = num_houses
        # self.frame = GroundplanFrame(self.plan)
        # self.frame.setPlan()
        # self.frame.root.mainloop()

    @staticmethod
    def placeWater(plan):
        w = int(plan.WIDTH / 2)
        h = int(plan.HEIGHT / 5)
        plan.addWaterbody(Waterbody(0, 0, w, h))
        plan.addWaterbody(Waterbody(w, plan.HEIGHT - h, w, h))
        return plan

    @staticmethod
    def placePlaygrounds(plan):
        center_y = plan.HEIGHT / 2
        dummy_pg = Playground(0, 0)
        y = int(center_y - dummy_pg.getHeight() / 2)
        x1 = int((plan.WIDTH / 3) - dummy_pg.getWidth() / 2)
        x2 = int((plan.WIDTH / 3) * 2 - dummy_pg.getWidth() / 2)
        plan.addPlayground(Playground(x1, int(y + int(plan.HEIGHT / 5) / 2)))
        plan.addPlayground(Playground(x2, int(y - int(plan.HEIGHT / 5) / 2)))
        return plan

    def developGroundplan(self,timeout=1000):
        plan = Groundplan(self.num_houses, self.enable_playground)
        self.placePlaygrounds(plan)
        self.placeWater(plan)
        return plan
