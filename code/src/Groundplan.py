import inspect

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Ground import Ground
from districtobjects.Mansion import Mansion
from districtobjects.Playground import Playground
from districtobjects.Residence import Residence
from districtobjects.Waterbody import Waterbody


class Groundplan(object):

    def __init__(self,

                 number_of_houses=10,  #
                 enable_playground=True,  #
                 name="groundplan",  #
                 puts=[],  #
                 width=200,  #
                 height=170,  #
                 min_wb_ratio=4,  #
                 max_pg_distance=50.0,  #
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
        self.width = width
        self.height = height
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

        self.AREA = self.width * self.height

        self.ground = Ground(0, 0, self.width, self.height)

        # counters
        self.number_of_familyhomes = 0
        self.number_of_bungalows = 0
        self.number_of_mansions = 0
        self.num_houses = 0

        # avoid accidental shared pointers

        for i in playgrounds:
            pg = Playground(i.x1, i.y1)
            if i.flipped:
                pg.flip()
            self.playgrounds.append(pg)
        for i in residences:
            h = self.getResidenceFunc(i.getType())(i.x1, i.y1)
            if i.flipped:
                h.flip()
            h.original_min_clearance = i.original_min_clearance
            h.minimumClearance = i.minimumClearance
            self.addResidence(h)
        for i in waterbodies:
            wb = Waterbody(i.x1, i.y1, i.width, i.height)
            if i.flipped:
                wb.flip()
            self.waterbodies.append(wb)

    @staticmethod
    def getResidenceFunc(t):
        if t == "FamilyHome": return FamilyHome
        elif t == "Bungalow": return Bungalow
        elif t == "Mansion": return Mansion

    def getNumberOfHouses(self):
        return self.num_houses

    def __copy__(self):
        return type(self)

    def addResidence(self, residence):
        assert isinstance(residence, Residence)
        if isinstance(residence,FamilyHome): self.number_of_familyhomes += 1
        elif isinstance(residence,Bungalow): self.number_of_bungalows += 1
        elif isinstance(residence,Mansion): self.number_of_mansions += 1
        self.num_houses += 1
        self.residences.append(residence)

    def removeResidence(self, residence):
        assert isinstance(residence, Residence)
        if isinstance(residence,FamilyHome): self.number_of_familyhomes -= 1
        elif isinstance(residence,Bungalow): self.number_of_bungalows -= 1
        elif isinstance(residence,Mansion): self.number_of_mansions -= 1
        self.num_houses -= 1
        self.residences.remove(residence)

    def isValid(self):

        def correctProportion(num_elements, threshold):

            return float(num_elements) / self.NUMBER_OF_HOUSES == threshold

        try:

            total_wb_area = 0
            for wb in self.waterbodies:

                assert self.correctlyPlaced(wb)
                total_wb_area += wb.width*wb.height

            assert (float(total_wb_area) / self.AREA) >= self.MINIMUM_WATER_PERCENTAGE
            assert len(self.waterbodies) <= self.MAXIMUM_WATER_BODIES
            assert correctProportion(self.number_of_familyhomes, self.MINIMUM_FAMILYHOMES_PERCENTAGE)
            assert correctProportion(self.number_of_bungalows, self.MINIMUM_BUNGALOW_PERCENTAGE)
            assert correctProportion(self.number_of_mansions, self.MINIMUM_MANSION_PERCENTAGE)
            assert self.num_houses == self.NUMBER_OF_HOUSES
            for r in self.residences: assert self.correctlyPlaced(r)
            return True
        except:
            return False

    @staticmethod
    def overlap(o1, o2): return o1 is not o2 and o1.x1 <= o2.x2 and o1.x2 >= o2.x1 and o1.y1 <= o2.y2 and o1.y2 >= o2.y1

    def correctlyPlaced(self, o,verbose=False):

        def within_area(o,verbose):
            assert o.y1 >= self.ground.y1
            assert o.x2 <= self.ground.x2
            assert o.y2 <= self.ground.y2
            assert o.x1 >= self.ground.x1
            if verbose: print 'within area limits'
            return True

        def no_overlap(o,verbose):
            for r in self.residences: assert not self.overlap(r, o)
            for r in self.playgrounds: assert not self.overlap(r, o)
            for r in self.waterbodies: assert not self.overlap(r, o)
            if verbose: print 'not overlapping anything'
            return True

        def water_is_ok(o,verbose):
            r = max(o.width, o.height) / min(o.width, o.height) <= self.MINIMUM_WATERBODY_RATIO
            if verbose: print 'is ok water'
            return r

        def residence_is_ok(o,verbose=False):

            def is_within_reach_of_pg(pgs,o):
                assert self.PLAYGROUND
                assert len(pgs) > 0
                for pg in pgs:
                    if self.getDistance(pg, o) <= self.MAXIMUM_PLAYGROUND_DISTANCE: return True
                if verbose: print 'not within pg reach'
                return False

            assert isinstance(o,Residence)
            assert o.y1 >= o.minimumClearance
            assert o.x1 >= o.minimumClearance
            assert o.x2 <= self.ground.x2 - o.minimumClearance
            assert o.y2 <= self.ground.y2 - o.minimumClearance
            if verbose: print 'has ok clearance from area edges'
            for r in self.residences: assert r is o or self.getDistance(r, o) >= max(r.minimumClearance,o.minimumClearance)
            if verbose: print 'no clearance conflict with other residences'
            assert not self.PLAYGROUND or is_within_reach_of_pg(self.playgrounds,o)
            return True

        try:
            assert within_area(o,verbose)
            assert no_overlap(o,verbose)
            if isinstance(o,Waterbody): assert water_is_ok(o,verbose)
            if isinstance(o,Residence): assert residence_is_ok(o)
            return True
        except: return False

    def getDistance(self, o1, o2):

        def dist(p1, p2): return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

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

        bm = [[0 for y in range(self.height)] for x in range(self.width)]

        for x in range(0, self.width):
            for y in range(0, self.height):
                m = Mansion(x, y)
                b = Bungalow(x, y)
                h = FamilyHome(x, y)

                if self.correctlyPlaced(m):
                    bm[x][y] = 1
                if self.correctlyPlaced(h):
                    bm[x][y] = 1
                if self.correctlyPlaced(b):
                    bm[x][y] = 1

        for x in range(self.width):
            for y in range(self.height):
                if bm[x][y]:
                    usableArea += 1

        return usableArea

    def getResidenceValue(self, residence):

        residence.original_min_clearance = type(residence)(0,0).minimumClearance
        value_residence = residence.getValue()
        distance = self.getMinimumDistance(residence)
        value_increase = residence.getAddedValuePercentage() * value_residence
        return value_residence + (max(distance - residence.original_min_clearance, 0)) * value_increase

    def getMinimumDistance(self, residence):
        return min([residence.x1,residence.y1,self.ground.x2 - residence.x2,self.ground.y2 - residence.y2,] 
                   + [self.getDistance(residence,other) for other in self.residences if other is not residence])

    def toString(self):
        return [[name, thing] for name, thing in inspect.getmembers(self)]

    def deepCopy(self):

        c = Groundplan(self.NUMBER_OF_HOUSES, self.PLAYGROUND,name=self.name,puts=self.puts,width=self.width,height=self.height,min_wb_ratio=self.MINIMUM_WATERBODY_RATIO,max_pg_distance=self.MAXIMUM_PLAYGROUND_DISTANCE,mansion_proportion=self.MINIMUM_MANSION_PERCENTAGE,bungalow_proportion=self.MINIMUM_BUNGALOW_PERCENTAGE,familyhome_proportion=self.MINIMUM_FAMILYHOMES_PERCENTAGE,max_wbs=self.MAXIMUM_WATER_BODIES,min_water_proportion=self.MINIMUM_WATER_PERCENTAGE,residences=self.residences,waterbodies=self.waterbodies,playgrounds=self.playgrounds,params=self.params,)
        return c

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
                          [Waterbody(wb.x1, wb.y1, wb.width, wb.height) for wb in s[14]],
                          [Playground(pg.x1, pg.y1, pg.flipped) for pg in s[15]],
                          s[16])

    def serialize(self):
        return [
            self.NUMBER_OF_HOUSES,
            self.PLAYGROUND,
            self.name,
            self.puts,
            self.width,
            self.height,
            self.MINIMUM_WATERBODY_RATIO,
            self.MAXIMUM_PLAYGROUND_DISTANCE,
            self.MINIMUM_MANSION_PERCENTAGE,
            self.MINIMUM_BUNGALOW_PERCENTAGE,
            self.MINIMUM_FAMILYHOMES_PERCENTAGE,
            self.MAXIMUM_WATER_BODIES,
            self.MINIMUM_WATER_PERCENTAGE,
            [[r.x1, r.y1, r.getType(), r.flipped, r.minimumClearance, float(r.original_min_clearance)] for r in
             self.residences],
            [[wb.x1, wb.y1, wb.width, wb.height, wb.flipped] for wb in self.waterbodies],
            [[pg.x1, pg.y1, pg.flipped] for pg in self.playgrounds],
            self.params
        ]
