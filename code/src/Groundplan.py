from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Ground import Ground
from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Residence import Residence
from districtobjects.Waterbody import Waterbody


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
    MINIMUM_WATERBODY_RATIO = 4

    def __init__(self, number_of_houses, playground):
        self.params = []
        self.PLAYGROUND = playground
        self.NUMBER_OF_HOUSES = number_of_houses

        self.ground = Ground(0, 0, self.WIDTH, self.HEIGHT)

        self.number_of_familyhomes = 0
        self.number_of_bungalows = 0
        self.number_of_mansions = 0
        self.num_houses = 0

        self.residences = []
        self.waterbodies = []
        self.playgrounds = []

    @staticmethod
    def getResidenceFunc(t):

        if t == "FamilyHome":
            return FamilyHome
        elif t == "Bungalow":
            return Bungalow
        elif t == "Mansion":
            return Mansion

    def deepCopy(self):
        plan = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND)
        for i in self.residences:
            h = self.getResidenceFunc(i.getType())(i.getX(), i.getY())
            if i.flipped:
                h.flip()
            h.original_min_clearance = i.original_min_clearance
            h.minimumClearance = i.minimumClearance
            plan.addResidence(h)
        for i in self.waterbodies:
            wb = Waterbody(i.getX(), i.getY(), i.getWidth(), i.getHeight())
            if i.flipped:
                wb.flip()
            plan.addWaterbody(wb)
        for i in self.playgrounds:
            pg = Playground(i.getX(), i.getY())
            if i.flipped:
                pg.flip()
            plan.addPlayground(pg)
        plan.params = self.params
        return plan

    def getNumberOfHouses(self):
        return self.num_houses

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
        return self.num_houses

    def addWaterbody(self, waterbody):
        self.waterbodies.append(waterbody)

    def addPlayground(self, playground):
        self.playgrounds.append(playground)

    def removeWaterbody(self, waterbody):
        self.waterbodies.remove(waterbody)

    def removePlayground(self, playground):
        self.playgrounds.remove(playground)

    def addResidence(self, residence):
        t = residence.getType()
        if t == "FamilyHome":
            self.number_of_familyhomes += 1
        elif t == "Bungalow":
            self.number_of_bungalows += 1
        elif t == "Mansion":
            self.number_of_mansions += 1
        self.num_houses += 1
        self.residences.append(residence)

    def removeResidence(self, residence):
        t = residence.getType()
        if t == "FamilyHome":
            self.number_of_familyhomes -= 1
        elif t == "Bungalow":
            self.number_of_bungalows -= 1
        elif t == "Mansion":
            self.number_of_mansions -= 1
        self.num_houses -= 1
        self.residences.remove(residence)

    def isValid(self, stage='full'):

        def correctNumElements():

            def correctProportion(num_elements, threshold):
                if self.NUMBER_OF_HOUSES < 1 : return False
                return float(num_elements) / self.NUMBER_OF_HOUSES == threshold

            if (len(self.waterbodies) <= self.MAXIMUM_WATER_BODIES
                and correctProportion(self.number_of_familyhomes, self.MINIMUM_FAMILYHOMES_PERCENTAGE)
                and correctProportion(self.number_of_bungalows, self.MINIMUM_BUNGALOW_PERCENTAGE)
                and correctProportion(self.number_of_mansions, self.MINIMUM_MANSION_PERCENTAGE)
                and self.num_houses == self.NUMBER_OF_HOUSES
                    ):
                return True
            else:
                return False

        def enoughWater():
            total_wb_area = 0
            for wb in self.waterbodies:
                if not self.correctlyPlaced(wb):
                    return False
                total_wb_area += wb.getSurface()
            return (float(total_wb_area) / self.AREA) >= self.MINIMUM_WATER_PERCENTAGE

        def residencesCorrectlyPlaced():
            for r in self.residences:
                if not self.correctlyPlaced(r):
                    return False
            return True

        return enoughWater() and (stage == 'base' or (residencesCorrectlyPlaced() and correctNumElements()))

    @staticmethod
    def overlap(o1, o2):
        return o1 is not o2 and o1.x1 <= o2.x2 and o1.x2 >= o2.x1 and o1.y1 <= o2.y2 and o1.y2 >= o2.y1

    def correctlyPlaced(self, o):

        if ((o.y1 < self.ground.y1 or o.x2 > self.ground.x2 or o.y2 > self.ground.y2 or o.x1 < self.ground.x1)
            or (isinstance(o, Residence) and (o.y1 < o.minimumClearance or
                                                      o.x2 > self.ground.x2 -
                                                          o.minimumClearance or o.y2 > self.ground.y2 -
                                                              o.minimumClearance
                                              or o.x1 < o.minimumClearance))):
            return False

        if isinstance(o, Waterbody):
            smaller = min(o.width, o.height)
            greater = max(o.width, o.height)
            ratio = float(greater) / smaller
            if ratio > self.MINIMUM_WATERBODY_RATIO:
                return False

        for wb in self.waterbodies:
            if wb != o and self.overlap(wb, o):
                return False

        self_clearance = o.minimumClearance if (
            isinstance(o, Residence)) else 0

        if not isinstance(o, Waterbody):
            for r in self.residences:
                if r is o:
                    continue
                if self.overlap(r, o) or self.getDistance(r, o) < max(self_clearance, r.minimumClearance):
                    return False

        if self.PLAYGROUND:

            if len(self.playgrounds) is 0:
                return False

            ok = False if isinstance(o, Residence) else True

            for pg in self.playgrounds:

                if self.overlap(o, pg):
                    return False

                if not ok and isinstance(o, Residence):
                    if self.getDistance(pg, o) <= self.MAXIMUM_PLAYGROUND_DISTANCE:
                        ok = True
                        continue

            if not ok:
                return False

        return True

    def getDistance(self, o1, o2):

        def dist(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        a1 = o1.y1 < o2.y2
        a2 = o1.x2 < o2.x1
        a3 = o1.y2 > o2.y1
        a4 = o1.x1 > o2.x2
        a5 = o1.y1 > o2.y2
        a6 = o1.x2 > o2.x1
        a7 = o1.x1 < o2.x2
        a8 = o1.y2 - o2.y1

        if self.overlap(o1, o2):
            return 0
        elif a1 and a2 and a3:
            return o2.x1 - o1.x2
        elif a1 and a3 and a4:
            return o1.x1 - o2.x2
        elif a5 and a6 and a7:
            return o1.y1 - o2.y2
        elif a6 and a8 and a7:
            return o2.y1 - o1.y2
        elif a1 and a6:
            return dist((o1.x1, o1.y2), (o2.x2, o2.y1))
        elif a1 and a7:
            return dist((o1.x2, o1.y2), (o2.x1, o2.y1))
        elif a6 and a3:
            return dist((o1.x1, o1.y1), (o2.x2, o2.y2))
        elif a3 and a7:
            return dist((o1.x2, o1.y1), (o2.x1, o2.y2))

    def getPlanValue(self):

        planValue = 0
        for residence in self.residences:
            planValue += self.getResidenceValue(residence)
        if self.PLAYGROUND:
            for playground in self.playgrounds:
                planValue -= playground.getPrice()
        return planValue

    def getUsableArea(self):
        usableArea = 0

        bm = [[0 for y in range(self.HEIGHT)] for x in range(self.WIDTH)]

        for x in range(0, self.WIDTH):
            for y in range(0, self.HEIGHT):
                m = Mansion(x, y)
                b = Bungalow(x, y)
                h = FamilyHome(x, y)

                if self.correctlyPlaced(m):
                    bm[x][y] = 1
                if self.correctlyPlaced(h):
                    bm[x][y] = 1
                if self.correctlyPlaced(b):
                    bm[x][y] = 1

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if bm[x][y]:
                    usableArea += 1

        return usableArea

    def getResidenceValue(self, residence):
        value_residence = residence.getValue()
        distance = self.getMinimumDistance(residence)
        value_increase = residence.getAddedValuePercentage() * value_residence
        return value_residence + (max(distance - residence.original_min_clearance, 0)) * value_increase

    def getMinimumDistance(self, residence):
        minimum = residence.x1
        if residence.y1 < minimum:
            minimum = residence.y1
        if self.ground.x2 - residence.x2 < minimum:
            minimum = self.ground.x2 - residence.x2
        if self.ground.y2 - residence.y2 < minimum:
            minimum = self.ground.y2 - residence.y2
        for other in self.residences:
            if residence != other:
                distance = int(self.getDistance(residence, other))
                if distance < minimum:
                    minimum = distance
        return minimum
