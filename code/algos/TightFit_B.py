from random import random

import time

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody

# a modified evolver, returns first valid solution it finds
from src.GroundplanFrame import GroundplanFrame



class validstate_tight2(object):

    def getPlan(self):
        return self.plan

    def determine_goal(self,plan, r):

        if isinstance(r,Bungalow):return plan.NUMBER_OF_HOUSES*plan.MINIMUM_BUNGALOW_PERCENTAGE
        elif isinstance(r,Mansion):return plan.NUMBER_OF_HOUSES*plan.MINIMUM_MANSION_PERCENTAGE
        elif isinstance(r,FamilyHome):return plan.NUMBER_OF_HOUSES*plan.MINIMUM_FAMILYHOMES_PERCENTAGE


    def translate(self,plan,clearance,h,w,x,y,k):
        res = [clearance + x*(w+clearance),clearance + y*(h+clearance)]
        if k==1:    res[0]=plan.WIDTH-res[0]
        elif k==2:  res[1]=plan.HEIGHT-res[1]
        return res

    def coords(self,plan,rt,factor,t):
        
        r = rt(0,0)
        c = r.minimumClearance*factor
        h = r.height
        w = r.width
        goal = self.determine_goal(plan, r)
        x_init = 0
        
        placed_houses=0
        
        while placed_houses<goal:
            x_init+=1
            y=-1
            x=x_init
            cur_x = self.translate(plan,c,h,w,x-1,0,t)[0]
            if cur_x > plan.WIDTH or cur_x < 0:
                return plan
            while x>0 and placed_houses<goal:
                x-=1
                y+=1
                res = self.translate(plan,c,h,w,x,y,t)
                house = rt(res[0],res[1])
                if plan.correctlyPlaced(house):
                    plan.addResidence(house)
                    placed_houses+=1

        return plan

    def developGroundplan(self,plan,i,j,k):
        try:
            plan = self.coords(plan,FamilyHome,i,0)
            plan = self.coords(plan,Bungalow,j,1)
            plan = self.coords(plan,Mansion,k,2)
            return plan
        except Exception:
            return plan

    def __init__(self, plan, i, j, k):
        self.plan = self.developGroundplan(plan.deepCopy(),i,j,k)
