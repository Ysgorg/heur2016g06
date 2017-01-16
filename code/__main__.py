# Setting absolute path to avoid pathing annoyances
import os
import sys

from src.evo_meta_get import plot_evo_meta

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# stuped algorithms
from src.Example import Example

# cleverer algorithms
from src.Evolver import Evolver
from src.TreeSearcher import TreeSearcher

algo = sys.argv[1]


# interpretation of arguments depend on first argument

def parseBase(b):
    if b == "DistrictPlanner": from src.DistrictPlanner import DistrictPlanner as d
    if b == "OtherDistrict":
        from src.OtherDistrict import OtherDistrict as d
    elif b == "AnotherDistrict":
        from src.AnotherDistrict import AnotherDistrict as d
    elif b == "TestDistrict":
        from src.TestDistrict import TestDistrict as d
    return d().developGroundplan()


if algo == "Evolver":
    base = parseBase(sys.argv[2])
    key = sys.argv[3]
    Evolver(base, key=key)

elif algo == "Example":
    Example()

elif algo == "TreeSearcher":
    base = parseBase(sys.argv[2])
    TreeSearcher(base)

elif algo == "EvoPlot":
    plot_evo_meta(sys.argv[2])
