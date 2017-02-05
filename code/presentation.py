import os

from bases.base_a import base_a
from bases.base_b import base_b
from param_searchers.simulated_annealing import sa_2
from param_searchers.zoom import zoom
from residence_placers.HillClimber import HillClimber
from residence_placers.Other import make_great_plan
from residence_placers.TightFit_B import TightFit_B
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from residence_placers.TightFit_A import TightFit_A

f = GroundplanFrame(Groundplan())
f.repaint(Groundplan())

print "##########" , 'Incomplete algorithm'
make_great_plan(f,slow=True)

a = base_a(40, True, 200, 170).deepCopy()
b = base_a(40, True, 200, 170).deepCopy()

print "##########" , 'Running Tight Fit A'
TightFit_A(a.deepCopy(), 1.0, 2.0, 3.0, frame=f, slow=True)
print "##########" , 'Running Tight Fit B'
TightFit_B(b.deepCopy(), 1.0, 2.0, 3.0, frame=f, slow=True)
print "##########" , 'Running Hill Climber'
HillClimber(a.deepCopy(),{'max_iterations': 60,'number_of_candidate_moves':4},frame=f,slow=True)


print "##########" , 'Running Simulated Annealing'
sa_2(a, {"max_iterations": 25, 'min': 1.0, 'max': 15.0}, TightFit_A, frame=f, slow=True)
print "##########" , 'Running zoom'
zoom(b, {'min': 1.0, 'max': 15.0, 'interval':2, 'min_interval':0.2, 'interval_shrink_factor':0.75}, TightFit_B, frame=f, slow=True)

print "##########" , 'Running test batch test'
os.system("python . vis test")