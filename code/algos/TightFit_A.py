from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion


class TightFit_A(object):
    name = "TightFit_A"
    expects = ['Waterbodies', "Playgrounds"]
    puts = ["Residences"]

    def compute_clearance(self, r):
        if isinstance(r, Mansion):
            return Mansion(0, 0).minimumClearance * self.m_clearance
        elif isinstance(r, Bungalow):
            return Bungalow(0, 0).minimumClearance * self.b_clearance
        elif isinstance(r, FamilyHome):
            return FamilyHome(0, 0).minimumClearance * self.f_clearance
        else:
            print "nooo"

    def getPlan(self):
        return self.plan

    def place_residences(self, plan, frame=None):

        i = 0
        r = self.next_to_place(i)
        r1 = r(0, 0)
        r1.original_min_clearance = r1.minimumClearance
        r1.minimumClearance = self.compute_clearance(r1)
        x = r1.minimumClearance

        while x < plan.WIDTH:

            y = r1.minimumClearance

            while y + r(0, 0).width + r(0, 0).minimumClearance < plan.HEIGHT:
                r1 = r(x, y)
                r1.original_min_clearance = r1.minimumClearance
                r1.minimumClearance = self.compute_clearance(r1)

                #print plan.PLAYGROUND

                if plan.correctlyPlaced(r1):


                    plan.addResidence(r1)
                    if plan.NUMBER_OF_HOUSES == plan.getNumberOfHouses():
                        return plan
                    #if frame is not None: frame.repaint(plan)
                    y += r1.height + r1.minimumClearance
                    i += 1
                    r = self.next_to_place(i)
                else:
                    y += 1
            x += r1.width + \
                 max(self.compute_clearance(r(0, 0)), r1.minimumClearance)
        return plan.deepCopy()

    def next_to_place(self, i):
        if i < self.fam_tresh:
            return FamilyHome
        elif i < self.bungalow_tresh:
            return Bungalow
        else:
            return Mansion

    def __init__(self, plan, i, j, k, frame=None):

        self.factors = [i, j, k]

        # print "satight",i,j,k
        self.f_clearance = i
        self.b_clearance = j
        self.m_clearance = k

        self.fam_tresh = plan.NUMBER_OF_HOUSES * plan.MINIMUM_FAMILYHOMES_PERCENTAGE
        self.bungalow_tresh = plan.NUMBER_OF_HOUSES * (
            plan.MINIMUM_FAMILYHOMES_PERCENTAGE + plan.MINIMUM_BUNGALOW_PERCENTAGE)

        self.plan = self.place_residences(plan, frame=frame).deepCopy()
        if frame is not None: frame.repaint(self.plan)
        # frame.repaint(self.plan)
        self.plan.params = [i, j, k]
