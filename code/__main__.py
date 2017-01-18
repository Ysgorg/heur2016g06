# Setting absolute path to avoid pathing annoyances
import os
import sys

from src.evaluate_base import evaluate_base
from src.neighbor_random import neighbor_random

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# stuped algorithms
from src.algo_Example import algo_Example

# cleverer algorithms
from src.algo_SimulatedAnnhealing import simulated_annealing
from src.algo_Evolver import algo_Evolver
from src.algo_TreeSearcher import algo_TreeSearcher

# other things
from src.plot_evolver_data import plot_evolver_data

algo = sys.argv[1]

def parseBase(b):
    if b == "dynamic": from src.base_dynamic import base_dynamic as d
    if b == "a":  from src.base_a import base_a as d
    elif b == "b":from src.base_b import base_b as d
    elif b == "c":from src.base_c import base_c as d
    return d().developGroundplan()


if algo == "Evolver":
    base = parseBase(sys.argv[2])
    key = sys.argv[3]
    algo_Evolver(base, key=key)

elif algo == "Base":
    evaluate_base(parseBase(sys.argv[2]))

elif algo == "Example":
    algo_Example()

elif algo == "TreeSearcher":
    base = parseBase(sys.argv[2])
    algo_TreeSearcher(base)

elif algo == "EvoPlot":
    plot_evolver_data('plans/' + sys.argv[2])

elif algo == "SA":
    from src.validstate_a import ValidStateGenerator

    def parseGenNeighborFunction(s):
        if s == "random":
            return neighbor_random

    simulated_annealing(ValidStateGenerator(parseBase(sys.argv[2])).best_plan,int(sys.argv[3]),parseGenNeighborFunction(sys.argv[4]))
