from random import random

from code.districtobjects.Bungalow import Bungalow
from code.districtobjects.FamilyHome import FamilyHome
from code.districtobjects.Mansion import Mansion
from code.districtobjects.Waterbody import Waterbody
from code.src.Groundplan import Groundplan
from code.src.GroundplanFrame import GroundplanFrame

from code.districtobjects.Playground import Playground


class Example(object):
    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True

    def __init__(self):
        self.plan = self.developGroundplan()
        self.frame = GroundplanFrame(self.plan)
        self.frame.setPlan()

        self.frame.root.mainloop()

    def developGroundplan(self):
        plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)

        x = 10 + random() * (plan.WIDTH - 50)
        y = 10 + random() * (plan.HEIGHT - 50)
        plan.addResidence(Mansion(x, y))
        print "Placing a mansion at location:", x, ",", y

        x = 10 + random() * (plan.WIDTH - 50)
        y = 10 + random() * (plan.HEIGHT - 50)
        plan.addResidence(Bungalow(x, y).flip())
        print "Placing a bungalow at location:", x, ",", y

        x = 10 + random() * (plan.WIDTH - 50)
        y = 10 + random() * (plan.HEIGHT - 50)
        plan.addResidence(FamilyHome(x, y))
        print "Placing a family home at location:", x, ",", y

        x = 50 + random() * (plan.WIDTH - 100)
        y = 50 + random() * (plan.HEIGHT - 100)
        plan.addPlayground(Playground(x, y))
        print "Placing a playground at location: ", x, ",", y

        width = random() * 20 + 20
        height = random() * 30 + 30
        x = 10 + random() * (plan.WIDTH - width - 10)
        y = 10 + random() * (plan.HEIGHT - height - 10)
        plan.addWaterbody(Waterbody(x, y, width, height))
        print "Placing a waterbody at location: ", x, ",", y, "of size", width, "x", height

        if plan.isValid():
            print "Plan is valid"
        else:
            print "Plan is invalid"

        print "Value of plan is:", plan.getPlanValue()

        return plan


Example()
