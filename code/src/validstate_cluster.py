from random import random

import time

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody

# a modified evolver, returns first valid solution it finds
from src.GroundplanFrame import GroundplanFrame


class validstate_cluster(object):

    # based on main idea of https://prezi.com/od6hubyxv8s0/amstelhaege/


    def getPlan(self):
        return self.plan

    def put_clusters(self,clusters):

        def put_cluster(cluster,x_shift,y_shift,plan):

            x = x_shift+cluster[4]
            for c in range(cluster[2]):
                y = y_shift+cluster[4]
                for r in range(cluster[3]):
                    plan.addResidence(cluster[5](x,y))
                    y += cluster[4]+cluster[5]().height
                x += cluster[4]+cluster[5]().width
            return plan


        """
        x = 0
        y = 0
        for c in clusters:
            self.plan = put_cluster(c,x,y,self.plan)
            y+=c[1]
        """

        self.plan = put_cluster(clusters[0],0,0,self.plan)
        self.plan = put_cluster(clusters[1],self.plan.WIDTH-clusters[1][0],0,self.plan)
        self.plan = put_cluster(clusters[2],0,self.plan.waterbodies[0].getY()-clusters[2][1],self.plan)

        if self.visualize == True:
            frame = GroundplanFrame(self.plan)
            frame.repaint(self.plan)
            #while True: pass

        return self.plan


    def compute_residence_groups(self):

        def define_cluster(cols, rows, housetype, clearance_factor):

            # input number houses per col and row, the residence class, and the clearance factor for this class.

            h = housetype()
            #print h.minimumClearance, clearance_factor
            clearance = h.minimumClearance * clearance_factor
            #print cols, rows, clearance , rows , h.width, h.height
            max_x = (cols+1) * clearance + cols * h.width
            max_y = (rows+1) * clearance + rows * h.height
            return [max_x,max_y,cols,rows,clearance,housetype]

        # MINIMUM_FAMILYHOMES_PERCENTAGE = 0.50
        # MINIMUM_BUNGALOW_PERCENTAGE = 0.30
        # MINIMUM_MANSION_PERCENTAGE = 0.20

        num_fh = int(self.plan.NUMBER_OF_HOUSES*self.plan.MINIMUM_FAMILYHOMES_PERCENTAGE)
        num_b = int(self.plan.NUMBER_OF_HOUSES*self.plan.MINIMUM_BUNGALOW_PERCENTAGE)
        num_m = int(self.plan.NUMBER_OF_HOUSES*self.plan.MINIMUM_MANSION_PERCENTAGE)

        return [
            # todo search for good vals
            define_cluster(5,4,FamilyHome,self.factors[0]),
            define_cluster(3,4,Bungalow,self.factors[1]),
            define_cluster(4,2,Mansion,self.factors[2])
        ]

    def developGroundplan(self,timeout):
        #while True:pass
        pass

    def __init__(self, plan,timeout,visualize=False,clearance_familyhome=3.8, clearance_bungalow=4.5,clearance_mansion=2.5):

        self.timeout = timeout
        self.visualize = visualize
        self.factors = [clearance_familyhome,clearance_bungalow,clearance_mansion]
        self.plan = plan.deepCopy()
        self.put_clusters(self.compute_residence_groups())
