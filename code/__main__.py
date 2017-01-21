# Setting absolute path to avoid pathing annoyances
import os
import sys
from pprint import pprint

from docopt import docopt

# for getting the proportion of a run
from src.evaluate_base import evaluate_base

# gen_neighbor functions for simulated annealing
from src.neighbor_random import neighbor_random

# residence placers
from src.validstate_rndm import validstate_rndm
from src.validstate_tight import validstate_tight

# water and playground placers
from src.base_dynamic import base_dynamic
from src.base_a import base_a
from src.base_b import base_b
from src.base_c import base_c

# plan optimizers
from src.algo_SimulatedAnnealing import simulated_annealing
from src.algo_Evolver import algo_Evolver
from src.algo_TreeSearcher import algo_TreeSearcher

# data analysis
from src.plot_evolver_data import plot_evolver_data

"""
# example commands
python . full
python . single algo=ts w=3 d=5 base=b vis=True pg=True nh=40
python . single algo=sa max_i=1000 ng=rndm base=b inits=rndm vis=True pg=True nh=40
python . single algo=evo base=b f=somekey vis=True pg=True nh=40
python . single algo=base base=b pg=True nh=40 vis=True
python . single algo=ex pg=True nh=40 vis=True
python . single other=evoplot f=somekey
"""


def single_experiment(args):


    def parseBool(s):
        return s=="True"


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
            return d(enable_playground,num_houses).developGroundplan(float(args['timeout'])/10)

        base = parseBase(args['base'],parseBool(args['pg']),int(args['nh']))
        if not base.isValid(stage="base"):
            return False


    if args['algo'] == 'ts':

        # ts is bugged it seems
        search_width = int(args['w'])
        max_depth = int(args['d'])
        algo_TreeSearcher(base=base,beam_width=search_width,height=max_depth,visualize=visualize)

    elif args['algo'] == 'sa':

        if not 'timeout' in args:
            print "timeout arg missing!"
            return
        else: timeout = 1

        if 'ng' in args:
            if 'max_i' in args:
                if 'inits' in args:
                    def parseGenNeighborFunction(s):
                        if s == "rndm": return neighbor_random

                    if args['ng'] in neigens: ng = parseGenNeighborFunction(args['ng'])
                    max_iter = int(args['max_i'])

                    def parse_initState(s,base):
                        if s=="rndm": return validstate_rndm(base,args['timeout']/10).getPlan()
                        if s=="tight": return validstate_tight(base,args['timeout']/10).getPlan()

                    init_state = parse_initState(args['inits'], base)

                    if not init_state.isValid(): return init_state

                    #print "Initial state found"

                    return simulated_annealing(init_state=init_state,max_iterations=max_iter,generateNeighborFunc=ng,visualize=visualize,timeout=timeout)
                else:
                    print 'inits arg missing!'
            else:
                print 'max_i arg missing!'

        else:
            print 'ng arg missing!'

    elif args['algo'] == "evo":

        algo_Evolver(base=base, key=args['f'], visualize=visualize)

    elif args['algo'] == "base":

        evaluate_base(base,visualize=visualize)
        while True: pass # to avoid instant closing of visualization




def all_experiments():

    NUM_HOUSES = [40,60,100]
    ENABLE_PG = [True, False]
    INIT_STATE = ["rndm", "tight"]
    NEIGBOR_GEN = ["rndm"]
    BASES = ["dynamic", 'a', 'b']

    num_experiments = float(len(NUM_HOUSES) * len(ENABLE_PG) * len(INIT_STATE) * len(NEIGBOR_GEN) * len(BASES))

    print "running",num_experiments, " experiments, systematically changing 5 variables"

    params = {
                "vis":"False", # increases performance
                "algo":"sa",
                "max_i":500,
                "timeout":60
              }

    results = [None]*len(NUM_HOUSES)

    i=0

    def logString(i1,i2,i3,i4,i5,i):
        print(str(NUM_HOUSES[i1])+"\t"+str(ENABLE_PG[i2])+"\t"+INIT_STATE[i3]+"\t"+NEIGBOR_GEN[i4]+\
               "\t"+BASES[i5]+"\t"+str(i)+"\t"),

    for nh in NUM_HOUSES:
        i1 = NUM_HOUSES.index(nh)

        results[i1] = [None]*len(ENABLE_PG)
        params["nh"] = nh
        for pg in ENABLE_PG:
            i2 = ENABLE_PG.index(pg)
            results[i1][i2] = [None]*len(INIT_STATE)
            params["pg"] = pg
            for inits in INIT_STATE:
                i3 = INIT_STATE.index(inits)
                results[i1][i2][i3] = [None]*len(NEIGBOR_GEN)
                params["inits"] = inits
                for ng in NEIGBOR_GEN:
                    i4 = NEIGBOR_GEN.index(ng)
                    results[i1][i2][i3][i4] = [None]*len(BASES)
                    params['ng'] = ng
                    for base in BASES:
                        params["base"] = base
                        i5 = BASES.index(base)
                        # print i1,i2,i3,i4,i5

                        i+=1
                        logString(i1,i2,i3,i4,i5 , i)

                        r = single_experiment(params)
                        if r == False or not r.isValid(): results[i1][i2][i3][i4][i5] = [0, 0]
                        else: results[i1][i2][i3][i4][i5] = [r.isValid(),r.getPlanValue()]
                        print str(results[i1][i2][i3][i4][i5][0]) + "\t" + str(results[i1][i2][i3][i4][i5][1])





def parseArgs(strs):
    args = {}
    for i in strs[1:]:
        if i=="full":
            args["full"] = True
        elif i=="single":
            args["single"] = True
        else:
            parts = i.split("=")
            args[parts[0]]=parts[1]
    return args


def reactToInput(args):
    if "full" in args: all_experiments()
    else: single_experiment(args)

# set working dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# run program
reactToInput(parseArgs(sys.argv))

