import time
from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

from src.DistrictPlanner import DistrictPlanner
from src.ConfigLogger import ConfigLogger

#

class Evolver(object):

    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True
    LOG_KEY = "evolver"

    # input log_unique_key to continue existing thread of evolution
    def __init__(self,log_unique_key=None):

        i = 0
        if log_unique_key is None:
            log_unique_key = str(random()) # probably but not definetly unique
            ConfigLogger.createConfigLog(self.LOG_KEY+log_unique_key)
            plan = DistrictPlanner().developGroundplan()
        else:
            plan = ConfigLogger.loadConfig(self.LOG_KEY+log_unique_key)

        frame = GroundplanFrame(plan)

        best_val = 1
        best_plan = plan
        iterations_since_best = 0

        # separate window for the best found
        best_frame = GroundplanFrame(plan)
        millis = 0
        while True:

            if i % 20 == 0:
                prev = millis
                millis = int(round(time.time() * 1000))
                if millis != 0:
                    print "millis per turn: ", (millis - prev) / 20

            if iterations_since_best > 100:
                plan = best_plan
                print "returning to past best :", best_val
                iterations_since_best = 0

            num = len(plan.getWaterbodies())

            if num > 0: plan.removeWaterbody(plan.getWaterbodies()[int(random() * num)])

            for j in range(1, 30000):

                num = len(plan.getWaterbodies())
                if num >= 4:
                    break
                x = random() * plan.WIDTH
                y = random() * plan.HEIGHT
                if random() < 0.5:
                    wb = Waterbody(x, y, plan.WIDTH / 4, plan.HEIGHT / 5)
                else:
                    wb = Waterbody(x, y, plan.HEIGHT / 5, plan.WIDTH / 4)
                # plan.removeWaterbody(plan.getWaterbodies()[int(random()*num)])
                if plan.correctlyPlaced(wb):
                    plan.addWaterbody(wb)

            if plan.getNumberOfHouses() is self.NUMBER_OF_HOUSES:
                ind = int(random() * self.NUMBER_OF_HOUSES)

                toberemoved = plan.getResidence(ind)
                type_to_place = toberemoved.getType()

                plan.removeResidence(toberemoved)

            else:
                if i % 10 < 5:
                    type_to_place = "FamilyHome"
                elif i % 10 < 8:
                    type_to_place = "Bungalow"
                else:
                    type_to_place = "Mansion"

            h = None
            iterations_since_last_success = 0
            while True:
                x = random() * plan.WIDTH
                y = random() * plan.HEIGHT

                if type_to_place is "FamilyHome":
                    h = FamilyHome(x, y)
                elif type_to_place is "Bungalow":
                    h = Bungalow(x, y)
                if type_to_place is "Mansion": h = Mansion(x, y)
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
                iterations_since_best += 1
                val = plan.getPlanValue()
                if val > best_val:
                    best_val = val
                    best_plan = plan
                    best_frame.repaint(best_plan)
                    print "new best:", best_val, iterations_since_best
                    iterations_since_best = 0

                    ConfigLogger.appendToConfigLog(self.LOG_KEY+log_unique_key,best_plan)

            frame.repaint(plan)
