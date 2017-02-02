from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion

# a modified evolver, returns first valid solution it finds
from src.GroundplanFrame import GroundplanFrame


class validstate_cluster(object):
    # based on main idea of https://prezi.com/od6hubyxv8s0/amstelhaege/

    def getPlan(self):
        return self.plan

    def put_clusters(self, clusters):

        def put_cluster(cluster, x_shift, y_shift, plan):

            x = x_shift + cluster[4]
            for c in range(cluster[2]):
                y = y_shift + cluster[4]
                for r in range(cluster[3]):
                    plan.addResidence(cluster[5](x, y))
                    y += cluster[4] + cluster[5]().height
                x += cluster[4] + cluster[5]().width
            return plan

        self.plan = put_cluster(clusters[0], 0, 0, self.plan)
        self.plan = put_cluster(
            clusters[1], self.plan.WIDTH - clusters[1][0], 0, self.plan)
        self.plan = put_cluster(
            clusters[2], 0, self.plan.waterbodies[0].getY() - clusters[2][1], self.plan)

        if self.visualize:
            frame = GroundplanFrame(self.plan)
            frame.repaint(self.plan)
            # while True: pass

        return self.plan

    def compute_residence_groups(self, plan):

        def define_cluster(cols, rows, housetype, clearance_factor):
            # input number houses per col and row, the residence class, and the
            # clearance factor for this class.

            h = housetype()
            clearance = h.minimumClearance * clearance_factor
            max_x = (cols + 1) * clearance + cols * h.width
            max_y = (rows + 1) * clearance + rows * h.height
            return [max_x, max_y, cols, rows, clearance, housetype]

        return [
            # todo search for good vals
            define_cluster(5, 4, FamilyHome, self.factors[0]),
            define_cluster(3, 4, Bungalow, self.factors[1]),
            define_cluster(4, 2, Mansion, self.factors[2])
        ]

    def develop_ground_plan(self):
        # while True:pass
        pass

    def valid_plan(self, in_plan):
        if len(self.expects) != len(in_plan.puts): return False
        for i in in_plan.puts:
            if i not in self.expects:
                return False
        return True

    def __init__(self, plan, i, j, k, frame=None):

        self.name = "TightFit_Cluster"
        self.expects = ['Waterbodies', "Playgrounds"]
        self.places = ["Residences"]
        self.factors = [i, j, k]
        if self.valid_plan(plan):
            self.plan = self.put_clusters(self.compute_residence_groups(plan))
        else:
            self.plan = None
