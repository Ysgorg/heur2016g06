from random import random

import time

import math

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.GroundplanFrame import GroundplanFrame


class TightFitWB(object):

    def compute_clearance(self,r):
        if isinstance(r, Mansion ): return Mansion(0,0).minimumClearance*self.m_clearance
        elif isinstance(r, Bungalow ): return Bungalow(0,0).minimumClearance*self.b_clearance
        elif isinstance(r, FamilyHome) : return FamilyHome(0,0).minimumClearance*self.f_clearance

    def next_to_place(self,i):

        if i < self.mansion_tresh: return None
        elif i < self.bungalow_tresh: return Bungalow
        else: return FamilyHome

    def place_residences(self,plan,frame=None):

        def placeWbs(plan,mc,frame):

            num_waterbodies = 4


            mansions_to_place = int(plan.NUMBER_OF_HOUSES * plan.MINIMUM_MANSION_PERCENTAGE)
            mansions_per_col = int(math.ceil(mansions_to_place*1.0/4))
            t = Mansion(0,0)
            t.minimumClearance = self.compute_clearance(t)

            for i in range(num_waterbodies):
                x = i * (self.wb_width+t.width+1)
                plan.addWaterbody(Waterbody(x,0,self.wb_width,self.wb_width*num_waterbodies))
                for j in range(mansions_per_col):
                    m = Mansion(x+self.wb_width+0.5,
                                t.minimumClearance + j * ( t.minimumClearance + t.width ))
                    m.minimumClearance = t.minimumClearance
                    print m.x,m.y,self.wb_width
                    if plan.correctlyPlaced(m): plan.addResidence(m)
                    else:
                        print "noo",m.x,m.y
                        #raise Exception

            return plan.deepCopy()

        visualize=frame is not None

        i = self.mansion_tresh
        r = self.next_to_place(i)
        r1 = r(0,0)
        r1.minimumClearance = self.compute_clearance(r1)
        x = r1.minimumClearance

        plan = placeWbs(plan,x,frame).deepCopy()

        while x < plan.WIDTH:
            y = r1.minimumClearance

            while y+r1.width+r1.minimumClearance < plan.HEIGHT:

                r1 = r(x,y)

                r1.minimumClearance = self.compute_clearance(r1)

                if plan.correctlyPlaced(r1):



                    plan.addResidence(r1)
                    if plan.NUMBER_OF_HOUSES == plan.getNumberOfHouses(): return plan
                    y+=r1.height+r1.minimumClearance
                    i+=1
                    r = self.next_to_place(i)
                else:
                    y += 1
            x+=r1.width+max(self.compute_clearance(r(0,0)),r1.minimumClearance)
        return plan.deepCopy()


    def compute_wb_min_side_length(self,plan,num_bodies):
        return math.sqrt(((plan.HEIGHT * plan.WIDTH * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies) / plan.MINIMUM_WATERBODY_RATIO)

    def compute_other_wb_side(self,plan,num_bodies,side_1):
        side_2 = ((plan.HEIGHT * plan.WIDTH * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies)/side_1
        if max(side_1,side_2) / min(side_1,side_2) > plan.MINIMUM_WATERBODY_RATIO:
            print "Too high wb proportion:" , max(side_1,side_2) / min(side_1,side_2)
            raise Exception
        else:
            return side_2

    def getPlan(self):
        return self.plan

    def __init__(self, plan, i,j,k,frame=None):

        self.f_clearance = i
        self.b_clearance = j
        self.m_clearance = k

        self.wb_width = self.compute_wb_min_side_length(plan,4)

        self.mansion_tresh = plan.NUMBER_OF_HOUSES * plan.MINIMUM_MANSION_PERCENTAGE
        self.bungalow_tresh = plan.NUMBER_OF_HOUSES * (plan.MINIMUM_MANSION_PERCENTAGE+
                                                   plan.MINIMUM_BUNGALOW_PERCENTAGE)


        self.plan = self.place_residences(plan.deepCopy(),frame=frame).deepCopy()
        self.plan.params = [i,j,k]

