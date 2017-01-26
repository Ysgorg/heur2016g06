# Setting absolute path to avoid pathing annoyances
import os
import sys
import time

from algos.BFS import algo_TreeSearcher
from algos.SimulatedAnnealing import simulated_annealing
from algos.TightFit_A import validstate_tight
from algos.TightFit_B import validstate_tight2
from algos.Hillclimber_Random import HillClimber
from bases.base_dynamic import base_dynamic
from bases.evaluate_base import evaluate_base
from experiments.sa_tight import sa_tight
from neighborfunctions.neighbor_random import neighbor_random
from neighborfunctions.neighbor_tight import neighbor_tight
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from src.plot_evolver_data import plot_evolver_data

"""
# example commands

python . sat # bugged or poorly designed
python . cluster # brute forces best params for validstate_tight
python . full # runs all experiments

# single runs
python . single algo=ts w=3 d=5 base=b vis=True pg=True nh=40
python . single algo=sa max_i=1000 ng=rndm base=b inits=rndm vis=True pg=True nh=40
python . single algo=evo base=b f=somekey vis=True pg=True nh=40
python . single algo=base base=b pg=True nh=40 vis=True
python . single algo=ex pg=True nh=40 vis=True
python . single other=evoplot f=somekey
"""

def other():
    thing = Groundplan(40,False)
    f = GroundplanFrame(thing)
    r = validstate_tight2(thing,1.0,1.0,1.0).getPlan()
    f.repaint(r)
    while True:pass

if sys.argv[1]=="other":other()

def sat():
    ## fail

    s = sa_tight(100,True,100,True)
    s = HillClimber(s,1000).getPlan()
    GroundplanFrame(s).repaint(s)
    while True:pass

if sys.argv[1]=="sat":sat()


def full_clean():
    ## fail

    from experiments.all import perform_all_experiments
    perform_all_experiments()
    while True:pass

if sys.argv[1]=="fullclean":full_clean()


def cluster_experiment():

    best_plan = None
    best_val = None

    base = base_dynamic(True,100).developGroundplan(1000)
    frame = GroundplanFrame(base)
    bframe = GroundplanFrame(base)
    best_vals=[]
    MIN = 10
    MAX = 60
    INTERVAL = 5
    num_iterations = 0
    t=time.time()

    results = []

    counter = 0



    for i in range(MIN,MAX,INTERVAL):
        a = float(i)/10
        if num_iterations>0:
            print round(float(num_iterations)/(time.time()-t)) , "iterations per second", num_iterations,"of",((MAX-MIN)/INTERVAL)**3,"done (",round(100*(float(num_iterations)/((MAX-MIN)/INTERVAL)**3)),"%)"
        for j in range(MIN,MAX,INTERVAL):
            b = float(j)/10
            upperupperbreak = 0
            for k in range(MIN,MAX,INTERVAL):
                c = float(k)/10
               # print i,j,k
                num_iterations+=1
                upperbreak=0
                #print i,j,k
                plan = validstate_tight(base.deepCopy(), a, b, c,visualize=False).getPlan().deepCopy()

                #print plan.getPlanValue()

                #plan = validstate_cluster(base.deepCopy(),1000,False,float(i)/10,float(j)/10,float(k)/10).getPlan()

                if plan.isValid():


                    v = plan.getPlanValue()
                    frame.repaint(plan)
                    if best_plan is None or v > best_val:
                        best_plan = plan.deepCopy()
                        best_val = best_plan.getPlanValue()
                        best_vals = [i,j,k]
                        bframe.repaint(best_plan)
                        print "best:",best_vals,best_val

                else:
                    #print "invalid"
                    if k==MIN:upperbreak+=1
                    break
                if upperbreak>0:
                    upperupperbreak=1
                    break

            if upperupperbreak>0:
                break


    #bframe.repaint(best_plan)
    print "best found: ", best_vals , best_val
    # simulated_annealing(best_plan,1000,neighbor_random,True,10000) # doesn't help much
    HillClimber(best_plan)
    while True: pass


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
            if b == "dynamic": from bases.base_dynamic import base_dynamic as d
            elif b == "a":  from bases.base_a import base_a as d
            elif b == "b":from bases.base_b import base_b as d
            elif b == "c":from bases.base_c import base_c as d

            return d(enable_playground,num_houses).developGroundplan()

        base = parseBase(args['base'],parseBool(args['pg']),int(args['nh']))
        if not base.isValid(stage="base"):
            return False


    if args['algo'] == 'ts':

        # ts is bugged it seems
        search_width = int(args['w'])
        max_depth = int(args['d'])
        algo_TreeSearcher(base=base,beam_width=search_width,height=max_depth,visualize=visualize)

    elif args['algo'] == 'sa':
        if 'ng' in args:
            if 'max_i' in args:
                if 'inits' in args:
                    def parseGenNeighborFunction(s):
                        if s == "rndm":
                            return neighbor_random
                        elif s == "tight":
                            return neighbor_tight

                    #if args['ng'] in args:
                    ng = parseGenNeighborFunction(args['ng'])
                    max_iter = int(args['max_i'])

                    def parse_initState(s,base):
                        if s=="rndm":
                            return HillClimber(base, args['vis']).getPlan()
                        elif s=="tight":
                            return validstate_tight(base, 1.0,1.0,1.0).getPlan()
                        #elif s=="cluster":return validstate_cluster(base, int(timeout)).getPlan()

                    # Keep trying until we find a valid starting state
                    init_state = parse_initState(args['inits'], base)
                    frame = GroundplanFrame(init_state)

                    print "Searching for valid init state"
                    while init_state.isValid() == False:
                        frame.repaint(init_state)
                        parse_initState(args['inits'], base)
                    print "init sa"
                    return simulated_annealing(init_state=init_state,max_iterations=max_iter,generateNeighborFunc=ng,visualize=visualize)
                else:
                    print 'inits arg missing!'
            else:
                print 'max_i arg missing!'

        else:
            print 'ng arg missing!'

    elif args['algo'] == "evo":

        HillClimber(base=base, key=args['f'], visualize=visualize)

    elif args['algo'] == "base":

        evaluate_base(base,visualize=visualize)
        while True: pass # to avoid instant closing of visualization




def all_experiments():

    NUM_HOUSES = [40,60,100]
    ENABLE_PG = [True, False]
    INIT_STATE = ["rndm", "tight","cluster"]
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
            #results[i1][i2]
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
        elif i=="cluster":
            args["cluster"] = True
        else:
            parts = i.split("=")
            args[parts[0]]=parts[1]
    return args


def reactToInput(args):
    global timeout
    if 'timeout' in args:
        timeout = args['timeout']
    else:
        timeout = 60
        print 'timeout arg missing! Defaulting to 60 seconds'

    if "cluster" in args: cluster_experiment()
    elif "full" in args: all_experiments()
    else:
        result = single_experiment(args)
        #frame = GroundplanFrame(result)
        #frame.repaint(result)
        #while True:
        #    pass


# set working dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# run program
reactToInput(parseArgs(sys.argv))
