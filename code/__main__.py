# Setting absolute path to avoid pathing annoyances
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# stuped algorithms
from src.Example import Example

# cleverer algorithms
from src.Evolver import Evolver

algo = sys.argv[1]

if algo == "Evolver":
    seed = sys.argv[2]
    Evolver(seed)

elif algo == "Example":
    Example()

