from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Residence import Residence
from src.Groundplan import Groundplan


class NewGrid():

    def build(self,plan,residence_type,num_rows,num_cols,clearance,corner,direction):


        residences = []

        d = residence_type(0, 0)

        x_interval = clearance + d.width
        y_interval = clearance + d.height

        if direction[0] < 0:
            init_x = corner[0] - x_interval
            x_interval *= -1

        else:
            init_x = corner[0] + clearance
        if direction[1] != 1:
            init_y = corner[1] - y_interval
            y_interval *= -1
        else:
            init_y = corner[1] + clearance
        x = init_x
        y = init_y

        assert isinstance(plan,Groundplan)

        if residence_type is FamilyHome: req_residences = plan.MINIMUM_FAMILYHOMES_PERCENTAGE*plan.NUMBER_OF_HOUSES-plan.number_of_familyhomes
        elif residence_type is Bungalow:req_residences = plan.MINIMUM_BUNGALOW_PERCENTAGE*plan.NUMBER_OF_HOUSES-plan.number_of_bungalows
        elif residence_type is Mansion:req_residences = plan.MINIMUM_MANSION_PERCENTAGE*plan.NUMBER_OF_HOUSES-plan.number_of_mansions
        else: raise Exception

        for i in range(num_rows):
            residences.append([])
            for j in range(num_cols):
                if req_residences < 1: break
                r = residence_type(x, y)
                r.minimumClearance = clearance
                assert isinstance(r.minimumClearance, float)
                assert plan.correctlyPlaced(r)

                req_residences-=1
                plan.addResidence(r)
                assert len(plan.residences)>0
                residences[i].append(r)

                x += x_interval
            else:break
            y += y_interval
            x = init_x

        return residences


    def morph(self, v):


        for i in range(len(self.residences)):

            y_change = (v + v * i) * self.direction[1]
            superBreak = False

            for j in range(len(self.residences[i])):
                x_change = (v + v * j) * self.direction[0]


                r = self.residences[i][j]

                r.x1 += x_change
                r.x2 += x_change
                r.y1 += y_change
                r.y2 += y_change



        for j in self.residences:
            for r in j:

                r.minimumClearance = self.plan.getMinimumDistance(r)

                #assert r.x1==self.residences[0][0].x1
                #assert r.x1==self.residences[0][0].x1

    def is_correct(self,verbose=False):
        try:
            for r in self.residences:
                for j in r:
                    assert self.plan.correctlyPlaced(j)
            return True
        except:
            return False

    def get_min_clearance(self):
        m = 999
        for i in self.residences:
            for j in i: m = min(self.plan.getMinimumDistance(j),m)
        return m

    def expand(self):

        assert self.is_correct()
        pre_c = self.get_min_clearance()
        self.morph(1.0)
        post_c = self.get_min_clearance()

        if not self.is_correct() or pre_c > post_c:

            self.shrink()
            assert self.is_correct()
            return False

        return True

    def shrink(self):
        self.morph(-1.0)


    def __init__(self,plan,rows,cols,residence_type,clearance,corner,direction):

        for i in [rows,cols]+direction:assert isinstance(i,int)
        for i in direction: assert i==1 or i==-1
        for i in corner+[clearance]: assert isinstance(i,float)
        assert isinstance(residence_type,type)

        self.corner=corner
        self.direction=direction
        self.clearance=clearance
        self.plan=plan
        self.residence_type=residence_type
        self.num_rows=rows
        self.num_cols=cols

        self.residences = self.build(plan,residence_type,rows,cols,clearance,corner,direction)

        assert self.is_correct()