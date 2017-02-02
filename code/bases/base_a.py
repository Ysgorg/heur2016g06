from districtobjects.Playground import Playground
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan


class base_a(object):
    def __init__(self, num_houses, enable_playground, width, height):
        self.name = 'base_a'
        self.puts = ['Waterbodies', 'Playgrounds']

        self.enable_playground = enable_playground
        self.num_houses = num_houses
        self.width = width
        self.height = height
        self.plan = self.develop_ground_plan(width, height)

    def deepCopy(self):
        return self.plan.deepCopy()

    @staticmethod
    def place_water(plan):
        w = int(plan.WIDTH / 2)
        h = int(plan.HEIGHT / 5)
        plan.waterbodies.append(Waterbody(0, 0, w, h))
        plan.waterbodies.append(Waterbody(w, plan.HEIGHT - h, w, h))
        return plan

    @staticmethod
    def place_playgrounds(plan):
        center_y = plan.HEIGHT / 2
        dummy_pg = Playground(0, 0)
        y = int(center_y - dummy_pg.height / 2)
        x1 = int((plan.WIDTH / 3) - dummy_pg.width / 2)
        x2 = int((plan.WIDTH / 3) * 2 - dummy_pg.width / 2)
        plan.playgrounds.append(Playground(x1, int(y + int(plan.HEIGHT / 5) / 2)))
        plan.playgrounds.append(Playground(x2, int(y - int(plan.HEIGHT / 5) / 2)))
        return plan

    def develop_ground_plan(self, width, height):
        plan = Groundplan(self.num_houses, self.enable_playground, name=self.name, width=width, height=height,
                          puts=self.puts)
        if self.enable_playground:
            self.place_playgrounds(plan)
        self.place_water(plan)
        return plan
