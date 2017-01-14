# this thing generates a tree as it traverses it,

"""
def get_valid_water_dimensions(plan, s1, num_bodies):
    # input plan and length of one side and desired number of water bodies
    # output the necessary length of the other side
    return (((plan.HEIGHT * plan.WIDTH) * plan.MINIMUM_WATER_PERCENTAGE) / num_bodies) / s1
"""

from random import random

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from src.GroundplanFrame import GroundplanFrame

from src.DistrictPlanner import DistrictPlanner
from src.OtherDistrict import OtherDistrict

from Queue import Queue


class TreeSearcher(object):

    class Tree(object):
        def __init__(self,depth):
            self.children = []
            self.data = None
            self.depth = depth

    NUMBER_OF_HOUSES = 40
    PLAYGROUND = True

    def __init__(self, visualize=True, beam_width=3):


        # get init plan from other module
        plan = DistrictPlanner().developGroundplan()

        tree = self.Tree(0)
        tree.data = plan
        q = Queue()
        q.put(tree)
        while not q.empty():
            n = q.get()
            for i in range(0,beam_width):
                child = self.Tree(n.depth+1)
                child.data = plan.deepCopy()

                """
                modify child here
                """

                n.children.append(child)
                q.put(n.children[len(n.children)-1])
            if n.depth==10:
                break

        def traverse(n):
            print n.depth, n.data.getPlanValue()
            for i in n.children: traverse(i)

        traverse(tree)

