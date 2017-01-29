import inspect

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Ground import Ground
from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Residence import Residence
from districtobjects.Waterbody import Waterbody


class Groundplan(object):
    def toString(self):
        return [[name, thing] for name, thing in inspect.getmembers(self)]

    @staticmethod
    def deserialize(s):
        def parse_residence_type(k):
            if k == "Mansion":
                return Mansion
            elif k == "Bungalow":
                return Bungalow
            elif k == "FamilyHome":
                return FamilyHome

        return Groundplan(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11], s[12],
                          [parse_residence_type(r[2])(r[0], r[1], flipped=r[3], minimumClearance=r[4],
                                                      original_min_clearance=r[5]) for r in s[13]],
                          [Waterbody(wb.x, wb.y, wb.width, wb.height) for wb in s[14]],
                          [Playground(pg.x, pg.y, pg.flipped) for pg in s[15]],
                          s[16])

    def serialize(self):
        return [
            self.NUMBER_OF_HOUSES,
            self.PLAYGROUND,
            self.name,
            self.puts,
            self.WIDTH,
            self.HEIGHT,
            self.MINIMUM_WATERBODY_RATIO,
            self.MAXIMUM_PLAYGROUND_DISTANCE,
            self.MINIMUM_MANSION_PERCENTAGE,
            self.MINIMUM_BUNGALOW_PERCENTAGE,
            self.MINIMUM_FAMILYHOMES_PERCENTAGE,
            self.MAXIMUM_WATER_BODIES,
            self.MINIMUM_WATER_PERCENTAGE,
            [[r.x, r.y, r.getType(), r.flipped, r.minimumClearance, float(r.original_min_clearance)] for r in
             self.residences],
            [[wb.x, wb.y, wb.width, wb.height, wb.flipped] for wb in self.waterbodies],
            [[pg.x, pg.y, pg.flipped] for pg in self.playgrounds],
            self.params
        ]

    def deepCopy(self):

        c = Groundplan(self.NUMBER_OF_HOUSES,
                       self.PLAYGROUND,
                       name=self.name,
                       puts=self.puts,
                       width=self.WIDTH,
                       height=self.HEIGHT,
                       min_wb_ratio=self.MINIMUM_WATERBODY_RATIO,
                       max_pg_distance=self.MAXIMUM_PLAYGROUND_DISTANCE,
                       mansion_proportion=self.MINIMUM_MANSION_PERCENTAGE,
                       bungalow_proportion=self.MINIMUM_BUNGALOW_PERCENTAGE,
                       familyhome_proportion=self.MINIMUM_FAMILYHOMES_PERCENTAGE,
                       max_wbs=self.MAXIMUM_WATER_BODIES,
                       min_water_proportion=self.MINIMUM_WATER_PERCENTAGE,
                       residences=self.residences,
                       waterbodies=self.waterbodies,
                       playgrounds=self.playgrounds,
                       params=self.params,
                       )
        return c

    def __init__(self,

                 number_of_houses=10,  #
                 enable_playground=True,  #
                 name="groundplan",  #
                 puts=[],  #
                 width=200,  #
                 height=170,  #
                 min_wb_ratio=4,  #
                 max_pg_distance=50,  #
                 mansion_proportion=0.2,  #
                 bungalow_proportion=0.3,  #
                 familyhome_proportion=0.5,  #
                 max_wbs=4,  #
                 min_water_proportion=0.2,  #
                 residences=[],
                 waterbodies=[],
                 playgrounds=[],
                 params=[]  #
                 ):

        self.NUMBER_OF_HOUSES = number_of_houses
        self.PLAYGROUND = enable_playground
        self.name = name
        self.puts = puts
        self.WIDTH = width
        self.HEIGHT = height
        self.MINIMUM_WATERBODY_RATIO = min_wb_ratio
        self.MAXIMUM_PLAYGROUND_DISTANCE = max_pg_distance
        self.MAXIMUM_WATER_BODIES = max_wbs
        self.MINIMUM_WATER_PERCENTAGE = min_water_proportion
        self.MINIMUM_MANSION_PERCENTAGE = mansion_proportion
        self.MINIMUM_BUNGALOW_PERCENTAGE = bungalow_proportion
        self.MINIMUM_FAMILYHOMES_PERCENTAGE = familyhome_proportion
        self.residences = []
        self.waterbodies = []
        self.playgrounds = []
        self.params = params

        self.AREA = self.WIDTH * self.HEIGHT

        self.ground = Ground(0, 0, self.WIDTH, self.HEIGHT)

        # counters
        self.number_of_familyhomes = 0
        self.number_of_bungalows = 0
        self.number_of_mansions = 0
        self.num_houses = 0

        # avoid accidental shared pointers

        for i in playgrounds:
            pg = Playground(i.getX(), i.getY())
            if i.flipped:
                pg.flip()
            self.addPlayground(pg)
        for i in residences:
            h = self.getResidenceFunc(i.getType())(i.getX(), i.getY())
            if i.flipped:
                h.flip()
            h.original_min_clearance = i.original_min_clearance
            h.minimumClearance = i.minimumClearance
            self.addResidence(h)
        for i in waterbodies:
            wb = Waterbody(i.getX(), i.getY(), i.getWidth(), i.getHeight())
            if i.flipped:
                wb.flip()
            self.addWaterbody(wb)

    @staticmethod
    def getResidenceFunc(t):

        if t == "FamilyHome":
            return FamilyHome
        elif t == "Bungalow":
            return Bungalow
        elif t == "Mansion":
            return Mansion

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
                if self.NUMBER_OF_HOUSES < 1: return False
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
