from algos.algo_SimulatedAnnealing import simulated_annealing
from bases import base_a, base_b, base_c, base_dynamic
from src import validstate_tight, validstate_rndm, neighbor_random


def perform_experiment(variables,frame):

    MAX_ITERATIONS = 100

    results = []

    i=0

    for nh in variables[0]:
        for pg in variables[1]:
            for base in variables[2]:
                b = base(num_houses=nh,enable_playground=pg).developGroundplan()
                for init_s in variables[3]:
                    ins = init_s(b.deepCopy()).getPlan().deepCopy()
                    frame.repaint(ins)
                    for ng in variables[4]:
                        r = simulated_annealing(ins.deepCopy(),MAX_ITERATIONS,ng)
                        frame.repaint(r)
                        v = r.getPlanValue() if r.isValid() else -1
                        results.append([nh,pg,base,r,v])
    return results

def construct_report(experiment):

    return experiment

def report(frame):
    experiment_variables = [
        [40, 70, 100],
        [True, False],
        [base_dynamic.base_dynamic, base_a.base_a, base_b.base_b#, base_c.base_c
         ],
        [validstate_tight.validstate_tight,validstate_rndm.validstate_rndm],
        [neighbor_random.neighbor_random]
    ]
    return construct_report(perform_experiment(experiment_variables,frame))

