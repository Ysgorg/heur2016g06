# Setting absolute path to avoid pathing annoyances
import os
import sys

from docopt import docopt

from src.evaluate_base import evaluate_base
from src.neighbor_random import neighbor_random
from src.validstate_a import ValidStateGenerator

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)

print "Current directory:", PATH

# stuped algorithms
from src.algo_Example import algo_Example

# cleverer algorithms
from src.algo_SimulatedAnnealing import simulated_annealing
from src.algo_Evolver import algo_Evolver
from src.algo_TreeSearcher import algo_TreeSearcher

# other things
from src.plot_evolver_data import plot_evolver_data






algo = sys.argv[1]



"""
# example commands
python . algo=ts w=3 d=5 base=b vis=True pg=True nh=40
python . algo=sa max_i=1000 ng=rndm base=b inits=rndm vis=True pg=True nh=40
python . algo=evo base=b f=somekey vis=True pg=True nh=40
python . algo=base base=b pg=True nh=40 vis=True
python . algo=ex pg=True nh=40 vis=True
python . other=evoplot f=somekey
"""

def parseArgs(strs):
    args = {}
    for i in strs[1:]:
        parts = i.split("=")
        args[parts[0]]=parts[1]
    return args


def parseBool(s): return s=="True"

args = parseArgs(sys.argv)

algos = ['evo','sa','ts','base','ex']
bases = ['dynamic','a','b','c']
other = ['evoplot']
neigens = ['rndm']


if 'other' in args:
    if args['other'] == "evoplot":
        plot_evolver_data('plans/' + args['f'])

elif args['algo'] in algos:
    visualize = parseBool(args['vis'])

if args['algo'] in algos and args['algo'] != 'ex':

    def parseBase(b,enable_playground,num_houses):
        if b == "dynamic": from src.base_dynamic import base_dynamic as d
        elif b == "a":  from src.base_a import base_a as d
        elif b == "b":from src.base_b import base_b as d
        elif b == "c":from src.base_c import base_c as d
        return d(enable_playground,num_houses).developGroundplan()

    base = parseBase(args['base'],parseBool(args['pg']),int(args['nh']))

if args['algo'] == 'ts':

    # ts is bugged it seems
    search_width = int(args['w'])
    max_depth = int(args['d'])
    algo_TreeSearcher(base=base,beam_width=search_width,height=max_depth,visualize=visualize)

elif args['algo'] == 'sa':


    def parseGenNeighborFunction(s):
        if s == "rndm": return neighbor_random

    if args['ng'] in neigens: ng = parseGenNeighborFunction(args['ng'])
    max_iter = int(args['max_i'])

    def parse_initState(s,base):
        if s=="rndm": return ValidStateGenerator(base).plan
    init_state = parse_initState(args['inits'], base)

    simulated_annealing(init_state=init_state,max_iterations=max_iter,generateNeighborFunc=ng,visualize=visualize)

elif args['algo'] == "evo":

    algo_Evolver(base=base, key=args['f'], visualize=visualize)

elif args['algo'] == "base":

    evaluate_base(base,visualize=visualize)
    while True: pass # to avoid instant closing of visualization

elif args['algo'] == "ex":
    algo_Example(enable_playground=parseBool(args['pg']),num_houses=int(args['nh']), visualize=visualize)
