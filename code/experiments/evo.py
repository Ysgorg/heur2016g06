from algos.algo_Evolver import algo_Evolver
from bases import base_a, base_b, base_c, base_dynamic
from src.GroundplanFrame import GroundplanFrame


def perform_experiment(variables,frame):

    print "Performing all evolution experiments"

    MAX_ITERATIONS = 100

    results = []

    def genKey(p1,p2,p3):

        if isinstance(p3,base_a.base_a): p3 = 'a'
        elif isinstance(p3,base_b.base_b): p3  = 'b'
        elif isinstance(p3,base_c.base_c): p3 = 'c'
        elif isinstance(p3,base_dynamic.base_dynamic): p3 = 'D'

        return "evo_"+str(p1)+'_'+str(p2)+'_'+p3+'.json'

    for num_houses in variables[0]:
        for enable_pg in variables[1]:
            for base in variables[2]:
                b = base(num_houses=num_houses,enable_playground=enable_pg)
                k = genKey(num_houses,enable_pg,b)
                #print(k),
                try:
                    r = algo_Evolver(
                        b.developGroundplan().deepCopy(),
                        key=k,
                        max_iterations=MAX_ITERATIONS,
                        frame=frame
                    ).getPlan().deepCopy()
                    v =  r.getPlanValue()
                    #print "  " + str(v)
                except Exception:
                    #print " timeout"
                    r = None
                    v = 0
                #print r
                results.append([num_houses,enable_pg,base, r, v])

    return results

def construct_report(experiment):
    return experiment

def report(frame):
    experiment_variables = [
        [40#, 70, 100
         ],
        [#True,
         False],
        [base_dynamic.base_dynamic, base_a.base_a, base_b.base_b
         #   , base_c.base_c
         ]
    ]
    return construct_report(perform_experiment(experiment_variables,frame))

