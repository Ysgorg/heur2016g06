import os
import sys

from algos.BFS import algo_TreeSearcher
from algos.Hillclimber_Random import HillClimber
from algos.SimulatedAnnealing import simulated_annealing
from algos.TightFitWB import TightFitWB
from algos.TightFit_A import validstate_tight
from bases.evaluate_base import evaluate_base
from experiments.sa_tight import sa_tight
from neighborfunctions.neighbor_random import neighbor_random
from neighborfunctions.neighbor_tight import neighbor_tight
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

"""
# example commands

python . sat
python . full # runs all single_experiments
python . fullclean # runs all experiments, in more structured in way

# single runs
python . single algo=ts w=3 d=5 base=b vis=True pg=True nh=40
python . single algo=sa max_i=1000 ng=rndm base=b inits=rndm vis=True pg=True nh=40
python . single algo=evo base=b f=somekey vis=True pg=True nh=40
python . single algo=base base=b pg=True nh=40 vis=True
python . single algo=ex pg=True nh=40 vis=True
python . single other=evoplot f=somekey
"""

def sat(frame):
    s = sa_tight(1000, True, 100,frame, TightFitWB)
    s = HillClimber(s, 10000).getPlan()
    frame.repaint(s)

def full_clean(frame):
    from experiments.all import perform_all_experiments
    perform_all_experiments(frame)

def parse_boolean(s): return s == "True"

def parse_base(b, enable_playground, num_houses):
    if b == "dynamic": from bases.base_dynamic import base_dynamic as d
    elif b == "a": from bases.base_a import base_a as d
    elif b == "b": from bases.base_b import base_b as d
    elif b == "c": from bases.base_c import base_c as d
    else: raise Exception("unknown base:", b)
    return d(enable_playground, num_houses).develop_ground_plan()

def parse_generate_neigbor_function(s):
    if s == "rndm": return neighbor_random
    elif s == "tight": return neighbor_tight

def parse_init_state(s, base):
    if s == "rndm": return HillClimber(base,num_iterations=1000).getPlan()
    elif s == "tight": return validstate_tight(base, 1.0, 1.0, 1.0).getPlan()

def single_experiment(args,frame):

    if not args['algo'] in ['evo', 'sa', 'ts', 'base']: return None

    base = parse_base(args['base'], parse_boolean(args['pg']), int(args['nh']))
    if not base.isValid(stage="base"): return False

    if args['algo'] == 'ts':  return algo_TreeSearcher(base=base, beam_width=int(args['w']), height=int(args['d'])).getPlan().deepCopy()
    elif args['algo'] == "evo": return HillClimber(base, num_iterations=int(args['num_iterations'])).getPlan().deepCopy()
    elif args['algo'] == "base": return evaluate_base(base,frame).getPlan().deepCopy()
    elif args['algo'] == 'sa':
        if not 'ng' in args or not 'max_i' in args or not 'inits' in args: raise Exception("Invalid args for SA :(")
        ng = parse_generate_neigbor_function(args['ng'])
        max_iter = int(args['max_i'])
        init_state = parse_init_state(args['inits'], base)
        return simulated_annealing(init_state=init_state, max_iterations=max_iter, gen_neigbor_func=ng).getPlan().deepCopy()

def all_experiments(frame):
    NUM_HOUSES = [40, 60, 100]
    ENABLE_PG = [True, False]
    INIT_STATE = ["rndm", "tight", "cluster"]
    NEIGBOR_GEN = ["rndm"]
    BASES = ["dynamic", 'a', 'b']

    num_experiments = float(len(NUM_HOUSES) * len(
        ENABLE_PG) * len(INIT_STATE) * len(NEIGBOR_GEN) * len(BASES))

    print "running", num_experiments, " experiments, systematically changing 5 variables"

    params = {"vis": "False", "algo": "sa", "max_i": 500,"timeout": 60}

    results = [None] * len(NUM_HOUSES)

    for nh in NUM_HOUSES:
        i1 = NUM_HOUSES.index(nh)

        results[i1] = [None] * len(ENABLE_PG)
        params["nh"] = nh
        for pg in ENABLE_PG:
            i2 = ENABLE_PG.index(pg)
            results[i1][i2] = [None] * len(INIT_STATE)
            params["pg"] = pg
            for inits in INIT_STATE:
                i3 = INIT_STATE.index(inits)
                results[i1][i2][i3] = [None] * len(NEIGBOR_GEN)
                params["inits"] = inits
                for ng in NEIGBOR_GEN:
                    i4 = NEIGBOR_GEN.index(ng)
                    results[i1][i2][i3][i4] = [None] * len(BASES)
                    params['ng'] = ng
                    for base in BASES:
                        params["base"] = base
                        i5 = BASES.index(base)
                        r = single_experiment(params,frame)
                        frame.repaint(r)
                        if r == False or not r.isValid():results[i1][i2][i3][i4][i5] = [0, 0]
                        else:results[i1][i2][i3][i4][i5] = [r.isValid(), r.getPlanValue()]

def parseArgs(strs):
    args = {}

    for i in strs[1:]:
        if i == "full": args["full"] = True
        elif i == "single": args["single"] = True
        elif i == "cluster": args["cluster"] = True
        elif i == "sat": args["sat"] = True
        elif i == "fullclean": args["fullclean"] = True
        else:
            parts = i.split("=")
            args[parts[0]] = parts[1]
    return args


def reactToInput(args):

    frame = GroundplanFrame(Groundplan(40,True))

    if "sat" in args: sat(frame)
    if "fullclean" in args: full_clean(frame)
    elif "full" in args: all_experiments(frame)
    else: frame.repaint(single_experiment(args,frame))

# set working dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# run program
reactToInput(parseArgs(sys.argv))

while True: pass