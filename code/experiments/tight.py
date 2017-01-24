from algos.algo_Evolver import algo_Evolver
from bases import base_a, base_b, base_c, base_dynamic
from src.validstate_tight2 import validstate_tight2
from src.validstate_tight import validstate_tight


def best_res(res):
    bestone = None
    for r in res:
        if bestone is None or r[7]>bestone[7]:
            bestone = r
    return bestone

def perform_experiment(variables,frame):

    print "Performing all tight experiments"

    MIN = 10
    MAX = 80
    INTERVAL = 10



    def find_best_params(num_houses,enable_playground,base,f,frame):

        bas = base(num_houses=num_houses,enable_playground=enable_playground).developGroundplan().deepCopy()

        interval = INTERVAL
        i_min = MIN
        i_max = MAX
        j_min = MIN
        j_max = MAX
        k_min = MIN
        k_max = MAX
        res=[]
        while True:
            results = []
            for i in range(i_min,i_max,interval):
                a = float(i)/10
                for j in range(j_min,j_max,interval):
                    b = float(j)/10
                    for k in range(k_min,k_max,interval):
                        c = float(k)/10
                        r = f(bas.deepCopy(),a,b,c).getPlan().deepCopy()
                        #r = validstate_tight(bas.deepCopy(), a, b, c).getPlan().deepCopy()
                        v = r.getPlanValue() if r.isValid() else -1
                        if v < 0: break
                        frame.repaint(r)
                        results.append([num_houses,enable_pg,base, i, j, k, r, v])

            best = best_res(results)
            res.append(best)

            i_ = best[3]
            j_ = best[4]
            k_ = best[5]

            i_min = max(MIN, i_ - interval*2)
            i_max = min(MAX, i_ + interval*2)
            j_min = max(MIN, j_ - interval*2)
            j_max = min(MAX, j_ + interval*2)
            k_min = max(MIN, k_ - interval*2)
            k_max = min(MAX, k_ + interval*2)
            interval=int(interval/2)
            if interval==0:
                break

        overall_best = best_res(res)
        frame.repaint(overall_best[6])
        return overall_best

    allresults = []
    for num_houses in variables[0]:
        for enable_pg in variables[1]:
            for base in variables[2]:
                for f in variables[3]:
                    allresults.append(find_best_params(num_houses,enable_pg,base,f,frame))

    best = best_res(allresults)

    frame.repaint(best[6])
    return allresults

def construct_report(experiment):
    return experiment

def report(frame):
    experiment_variables = [
        [#40, 70,
         100],
        [False],
        [base_dynamic.base_dynamic, base_a.base_a, base_b.base_b, base_c.base_c
         ],
        [#validstate_tight,
         validstate_tight2
         ]
    ]
    return construct_report(perform_experiment(experiment_variables,frame))

