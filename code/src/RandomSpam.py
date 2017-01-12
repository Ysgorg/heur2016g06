from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

from districtobjects.Playground import Playground

# 5:3:2
#
#
#

class RandomSpam(object):

    NUMBER_OF_HOUSES = 40
    PLAYGROUND = False

    def __init__(self):

        i = 0

        plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)

        frame = GroundplanFrame(plan)

        wb = Waterbody(0,0,plan.WIDTH/5,plan.HEIGHT)
        plan.addWaterbody(wb)

        while True:

            type_to_place = None


            if plan.getNumberOfHouses() is 40:
                ind = int(random()*40)

                toberemoved = plan.getResidence(ind)
                type_to_place = toberemoved.getType()

                plan.removeResidence(toberemoved)

            else:
                if i%10 < 5: type_to_place = "FamilyHome"
                elif i%10 < 8: type_to_place = "Bungalow"
                else: type_to_place = "Mansion"

            h = None
            iterations_since_last_success = 0
            while True:
                x = 10 + random() * (plan.WIDTH - 50)
                y = 10 + random() * (plan.HEIGHT - 50)

                if type_to_place is "FamilyHome": h = FamilyHome(x,y)
                elif type_to_place is "Bungalow": h = Bungalow(x,y)
                if type_to_place is "Mansion": h = Mansion(x,y)
                if random() < 0.5: h = h.flip()
                if plan.correctlyPlaced(h):
                    plan.addResidence(h)
                    i += 1
                    break
                else:
                    h = h.flip()
                    if plan.correctlyPlaced(h):
                        plan.addResidence(h)
                        i += 1
                        break
                if iterations_since_last_success > 300:
                    break
                iterations_since_last_success += 1

            if plan.isValid():
                print "valid! :D"
                return plan
            frame.repaint(plan)

