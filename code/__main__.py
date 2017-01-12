# Setting absolute path to avoid pathing annoyances
import os

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# stuped algorithms
from src.Example import Example
# from src.Greedy import Greedy

# cleverer algorithms
from src.DistrictPlanner import DistrictPlanner
from src.Evolver import Evolver

# Evolver()
DistrictPlanner()
