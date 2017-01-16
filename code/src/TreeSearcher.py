# this thing generates a tree as it traverses it,

"""
def get_valid_water_dimensions(plan, s1, num_bodies):
    # input plan and length of one side and desired number of water bodies
    # output the necessary length of the other side
    return (((plan.HEIGHT * plan.WIDTH) * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies) / s1
"""

from random import random

import time
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.GroundplanFrame import GroundplanFrame

from src.DistrictPlanner import DistrictPlanner
from src.OtherDistrict import OtherDistrict
from src.TestDistrict import TestDistrict

from Queue import Queue


def determine_type_to_place(i):
    tot = i.getNumberOfHouses()
    if tot % 10 == 0: return FamilyHome
    if float(i.number_of_familyhomes) / tot < 0.5: return FamilyHome
    elif float(i.number_of_bungalows) / tot < 0.3: return Bungalow
    elif float(i.number_of_mansions) / tot < 0.2: return Mansion


def determine_coordinates(plan, f):

    while True:
        x = int(random()*plan.WIDTH)
        y = int(random()*plan.HEIGHT)
        if plan.correctlyPlaced(f(x,y)):
            return [x,y]
    """

    for x in range(1,plan.WIDTH,1+int(25*random())):
        for y in range(1,plan.HEIGHT,1+int(25*random())):
            if plan.correctlyPlaced(f(x,y)):
                return [x,y]
    return None
    pass
    """



class TreeSearcher(object):

    class Tree(object):
        def __init__(self,depth):
            self.children = []
            self.data = None
            self.depth = depth

    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True

    def __init__(self, base, visualize=True, beam_width=3,height=4):



        # get init plan from other module
        self.best_plan = base
        self.thetree = self.Tree(0)

        frame = GroundplanFrame(self.best_plan)


        while not self.best_plan.getNumberOfHouses() == 40:
            print 'at ========================== ',self.best_plan.getNumberOfHouses()

            frame.repaint(self.best_plan)
            tree = self.Tree(self.thetree.depth)
            print tree.depth
            tree.data = self.best_plan
            q = Queue()
            q.put(tree)
            ms = time.time()
            while not q.empty():
                n = q.get()
          #      print 'depth: ',n.depth
                for i in range(0,beam_width):
                    child = self.Tree(n.depth+1)
                    child.data = n.data.deepCopy()

                    ####
                    """
                    modify child here
                    """
                    f = determine_type_to_place(child.data)
                    if f is None:
                        print
                    coords = determine_coordinates(n.data,f)
                    if coords is not None:
                        n.data.addResidence(f(coords[0],coords[1]))
                        n.children.append(child)
                        q.put(n.children[len(n.children)-1])


                    ####



                if n.depth==height:
                    break

            buildt = time.time()-ms
            self.c = 0

            self.best_plan = None
            self.best_plan_val = -999999999999

            def traverse(n):
                self.c+=1
                #print self.c , n.depth
                val = n.data.getPlanValue()
                if val>self.best_plan_val and not n.data.getNumberOfHouses() > 40:
                    self.best_plan = n.data.deepCopy()
                    self.best_plan_val = val
                    self.thetree = self.Tree(n.depth)
                    self.thetree.data = self.best_plan.deepCopy()

                    if n.data.getNumberOfHouses() == 40:
                        return "yes"
                print self.c, n.depth, n.data.getPlanValue()
                for i in n.children: traverse(i)

            ms = time.time()
            if traverse(tree) == "yes":
                print "yes"
            end = time.time()
            print "built tree of ", self.c,"nodes in ",buildt,"sec, then traversed it in",(end-ms),"sec"

        frame.repaint(self.best_plan)
        while True: pass