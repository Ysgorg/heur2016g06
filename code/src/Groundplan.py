import math

from districtobjects.Residence import Residence
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Bungalow import Bungalow
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground

from districtobjects.Ground import Ground


class Groundplan(object):
    WIDTH = 200
    HEIGHT = 170
    AREA = WIDTH * HEIGHT
    MINIMUM_WATER_PERCENTAGE = 0.2
    MAXIMUM_WATER_BODIES = 4
    MINIMUM_FAMILYHOMES_PERCENTAGE = 0.50
    MINIMUM_BUNGALOW_PERCENTAGE = 0.30
    MINIMUM_MANSION_PERCENTAGE = 0.20
    MAXIMUM_PLAYGROUND_DISTANCE = 50

    def __init__(self, number_of_houses, playground):
        self.PLAYGROUND = playground

        self.ground = Ground(0, 0, self.WIDTH, self.HEIGHT)
        self.number_of_houses = number_of_houses

        self.number_of_familyhomes = 0
        self.number_of_bungalows = 0
        self.number_of_mansions = 0

        self.residences = []
        self.waterbodies = []
        self.playgrounds = []

    def deepCopy(self):
        plan = Groundplan(self.number_of_houses, self.PLAYGROUND)
        for i in self.residences:
            t = i.getType()
            if t == "FamilyHome":
                h = FamilyHome(i.getX(), i.getY())
            elif t == "Bungalow":
                h = Bungalow(i.getX(), i.getY())
            elif t == "Mansion":
                h = Mansion(i.getX(), i.getY())
            if i.flipped: h.flip()
            plan.addResidence(h)
        for i in self.waterbodies:
            wb = Waterbody(i.getX(), i.getY(), i.getWidth(), i.getHeight())
            if i.flipped: wb.flip()
            plan.addWaterbody(wb)
        for i in self.playgrounds:
            pg = Playground(i.getX(), i.getY())
            if i.flipped: pg.flip()
            plan.addPlayground(pg)
        return plan

    def getNumberOfHouses(self):
        return self.number_of_familyhomes + self.number_of_bungalows + self.number_of_mansions

    def __copy__(self):
        return type(self)

    def getWidth(self):
        return self.WIDTH

    def getHeight(self):
        return self.HEIGHT

    def getResidences(self):
        return self.residences

    def getResidence(self, index):
        return self.residences[index]

    def getWaterbodies(self):
        return self.waterbodies

    def getPlaygrounds(self):
        return self.playgrounds

    def numberOfHouses(self):
        return self.number_of_houses

    def addResidence(self, residence):
        if residence.getType() == "FamilyHome":
            self.number_of_familyhomes += 1
        elif residence.getType() == "Bungalow":
            self.number_of_bungalows += 1
        elif residence.getType() == "Mansion":
            self.number_of_mansions += 1
        self.residences.append(residence)

    def removeResidence(self, residence):

        if residence.getType() == "FamilyHome":
            self.number_of_familyhomes -= 1
        elif residence.getType() == "Bungalow":
            self.number_of_bungalows -= 1
        elif residence.getType() == "Mansion":
            self.number_of_mansions -= 1
        self.residences.remove(residence)

    def addWaterbody(self, waterbody):
        self.waterbodies.append(waterbody)

    def removeWaterbody(self, waterbody):
        self.waterbodies.remove(waterbody)

    def addPlayground(self, playground):
        self.playgrounds.append(playground)

    def removePlayground(self, playground):
        self.playgrounds.remove(playground)

    def isValid(self, verbose=False):
        if (len(self.waterbodies) > self.MAXIMUM_WATER_BODIES or
                    (float(self.number_of_familyhomes) / self.number_of_houses) < self.MINIMUM_FAMILYHOMES_PERCENTAGE or
                    (float(self.number_of_bungalows) / self.number_of_houses) < self.MINIMUM_BUNGALOW_PERCENTAGE or
                    (float(self.number_of_mansions) / self.number_of_houses) < self.MINIMUM_MANSION_PERCENTAGE):
            if verbose: print "problem: incorrect ratio / number of elements"
            return False
        else:
            waterbody_surface = 0
            for waterbody in self.waterbodies:
                if not self.correctlyPlaced(waterbody):
                    if verbose: print "problem: incorrectly placed water"
                    return False
                else:
                    waterbody_surface += waterbody.getSurface()

            if (float(waterbody_surface) / self.AREA) < self.MINIMUM_WATER_PERCENTAGE:
                if verbose: print "problem: water percent ", float(waterbody_surface) / self.AREA
                return False
            for residence in self.residences:
                if not self.correctlyPlaced(residence):
                    if verbose: print "problem: residence incorrectly placed"
                    return False

            return True

    def overlap(self,o1, o2, verbose=False):
        if o1 is o2: return False
        # def correct https://silentmatt.com/rectangle-intersection/
        return o1.x1 <= o2.x2 and o1.x2 >= o2.x1 and o1.y1 <= o2.y2 and o1.y2 >= o2.y1


    def correctlyPlaced(self, placeable, verbose=False):

        if placeable.y1 < self.ground.y1 or placeable.x2 > self.ground.x2 \
                or placeable.y2 > self.ground.y2 or placeable.x1 < self.ground.x1:
            return False

        if isinstance(placeable, Residence) and (placeable.y1 < placeable.getminimumClearance() or
                                                         placeable.x2 > self.ground.x2 - placeable.getminimumClearance() or
                                                         placeable.y2 > self.ground.y2 - placeable.getminimumClearance() or
                                                         placeable.x1 < placeable.getminimumClearance()):
            return False

        for waterbody in self.waterbodies:
            ratio = waterbody.getWidth() / waterbody.getWidth()
            # ignoring water side ratio for now
            if False and ratio != 0.25 and ratio != 4:
                if verbose:
                    print "problem: wrong water dimension"
                    return False
            if waterbody is not placeable and self.overlap(waterbody, placeable):
                return False

        self_clearance = 0

        if isinstance(placeable, Residence):
            self_clearance = placeable.getminimumClearance()

        for residence in self.residences:
            if residence is placeable: continue
            if self.overlap(residence, placeable, verbose):

                if verbose: print "overlap:", residence.x1, residence.x2, residence.y1, residence.y2, \
                    residence.getType(), "and", placeable.x1, placeable.x2, placeable.y1, placeable.y2, placeable.getType()
                return False
            if not isinstance(placeable, Waterbody):
                if self.getDistance(residence, placeable) < max(self_clearance, residence.getminimumClearance()):
                    return False

        if self.PLAYGROUND:

            if len(self.playgrounds) is 0: return False

            ok = False

            for playground in self.playgrounds:

                if self.overlap(placeable, playground):
                    if verbose: print "overlap!", playground.getX(), playground.getY(), isinstance(playground,
                                                                                                   Playground), placeable.getX(), placeable.getY(), placeable.getType()
                    return False

                if isinstance(placeable, Residence):
                    min_ok = placeable.getminimumClearance()
                    max_ok = self.MAXIMUM_PLAYGROUND_DISTANCE
                    distance = self.getDistance(playground, placeable)

                    if min_ok < distance <= max_ok:
                        ok = True
                        break

            if isinstance(placeable, Waterbody): ok = True

            if not ok: return False
        return True


    def getDistance(self,o1, o2):

        def dist(p1,p2): return ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 ) ** 0.5

        a1 = o1.y1 < o2.y2
        a2 = o1.x2 < o2.x1
        a3 = o1.y2 > o2.y1
        a4 = o1.x1 > o2.x2
        a5 = o1.y1 > o2.y2
        a6 = o1.x2 > o2.x1
        a7 = o1.x1 < o2.x2
        a8 = o1.y2 - o2.y1

        if self.overlap(o1,o2):     return 0
        elif (a1 and a2 and a3):    return o2.x1 - o1.x2
        elif (a1 and a3 and a4):    return o1.x1 - o2.x2
        elif (a5 and a6 and a7):    return o1.y1 - o2.y2
        elif (a6 and a8 and a7):    return o2.y1 - o1.y2
        elif (a1 and a6):           return dist((o1.x1, o1.y2), (o2.x2, o2.y1))
        elif (a1 and a7):           return dist((o1.x2, o1.y2), (o2.x1, o2.y1))
        elif (a6 and a3):           return dist((o1.x1, o1.y1), (o2.x2, o2.y2))
        elif (a3 and a7):           return dist((o1.x2, o1.y1), (o2.x1, o2.y2))


    def getPlanValue(self):
        planValue = 0
        for residence in self.residences:
            planValue += self.getResidenceValue(residence)
        if self.PLAYGROUND:
            for playground in self.playgrounds:
                planValue -= playground.getPrice()
        return planValue

    def getResidenceValue(self, residence):
        value_residence = residence.getValue()
        distance = self.getMinimumDistance(residence)
        value_increase = residence.getAddedValuePercentage() * value_residence
        return value_residence + (max(distance - residence.getminimumClearance(), 0)) * value_increase

    def getMinimumDistance(self, residence):
        minimum = residence.x1
        if residence.y1 < minimum: minimum = residence.y1
        if self.ground.x2 - residence.x2 < minimum: minimum = self.ground.x2 - residence.x2
        if self.ground.y2 - residence.y2 < minimum: minimum = self.ground.y2 - residence.y2
        for other in self.residences:
            if residence != other:
                distance = int(self.getDistance(residence, other))
                if distance < minimum:
                    minimum = distance
        return minimum
