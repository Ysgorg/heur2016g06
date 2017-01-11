# Setting absolute path to avoid pathing annoyances
import os
PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# The example solution provided (For testing setup)
from src.Example import Example

# The Class we are expanding on
#from src.DistrictPlanner import DistrictPlanner
