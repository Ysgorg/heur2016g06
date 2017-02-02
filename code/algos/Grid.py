
class Grid:

    def build(self):

        d = self.residence_type(0, 0)

        x_interval = self.clearance + d.width
        y_interval = self.clearance + d.height

        init_x = 0

        if self.anchor_corner[0] != 1:
            init_x = self.anchor_coordinates[0]-x_interval
            x_interval*=-1
        else:
            init_x = self.anchor_coordinates[0]+self.clearance
        if self.anchor_corner[1] != 1:
            init_y = self.anchor_coordinates[1]-y_interval
            y_interval*=-1
        else:
            init_y = self.anchor_coordinates[1]+self.clearance
        x=init_x
        y=init_y

        for i in range(self.num_rows):
            for j in range(self.num_cols):


                r = self.residence_type(x, y)
                r.minimumClearance = self.clearance

                assert isinstance(r.minimumClearance,float)
                if self.plan.correctlyPlaced(r,verbose=False):

                    self.plan.residences.append(r)
                    self.residences.append(r)

                x += x_interval
            y += y_interval
            x = init_x

    def __init__(self, num_rows, num_cols, residence_type, clearance, anchor_corner, anchor_coordinates,plan):


        assert isinstance(plan.name,str)
        assert isinstance(num_rows,int)
        assert isinstance(num_cols,int)

        self.plan = plan
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.residence_type = residence_type
        self.clearance = clearance
        self.anchor_corner = anchor_corner
        self.anchor_coordinates = anchor_coordinates
        self.x_dir = -0.1 if self.anchor_corner[0] > 0 else 0.1
        self.y_dir = -0.1 if self.anchor_corner[1] > 0 else 0.1
        self.residences = []

        self.build()

    def morph(self,v):

        for i in range(len(self.residences)):
            r = self.residences[i]
            if self.anchor_corner[0] == 1:
                r.x1 += v+v*i
                r.x2 += v+v*i
            else:
                r.x1 -= v+v*i
                r.x2 -= v+v*i
            if self.anchor_corner[1] == 1:
                r.y1 += v
                r.y2 += v
            else:
                r.y1 -= v
                r.y2 -= v
            r.minimumClearance = self.plan.compute_clearance(r)

    def is_correct(self):
        for r in self.residences:
            if not self.plan.correctlyPlaced(r): return False
        return True

    def expand(self,f=1.0):
        self.is_correct()
        self.morph(0.1*f)
        if not self.is_correct():
            self.shrink(f)
            assert self.is_correct()
            return False
        return True

    def shrink(self,f=1.0):
        self.morph(-0.1*f)

    def f(self):
        return 'hello world'

