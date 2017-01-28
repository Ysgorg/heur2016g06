import time

from algos.TightFitWB import TightFitWB
from algos.TightFit_A import TightFit_A
from algos.TightFit_B import TightFit_B
from bases import base_a
from bases import base_b
from bases import base_c
from bases import base_dynamic
from src.Groundplan import Groundplan



def doit(num_houses, enable_pg, base, f, frame,p):

    def best_res(res):
        bestone = None
        for r in res:
            if bestone is None or r[5] > bestone[5]: bestone = r
        return bestone

    def getmin(v): return max(p['min'],v-interval*2)
    def getmax(v): return min(p['max'],v+interval*2)

    t = time.time()
    bas = base(num_houses, enable_pg).deepCopy()

    i_min = p['min']
    i_max = p['max']
    j_min = p['min']
    j_max = p['max']
    k_min = p['min']
    k_max = p['max']

    interval = p['interval']

    results = []

    while interval > p['min_interval']:
        i = i_min
        while i_min <= i < i_max:
            j = j_min
            while j_min <= j < j_max:
                k = k_min
                while k_min <= k < k_max:
                    r = f(bas.deepCopy(), i, j, k, frame).getPlan().deepCopy()
                    frame.repaint(r)
                    v = r.getPlanValue() if r.isValid() else 0
                    results.append(
                        [
                            bas,
                            i,
                            j,
                            k,
                            r,
                            v
                        ]
                    )
                    k += interval
                j += interval
            i += interval

        best = best_res(results)

        i_min = getmin(best[1])
        i_max = getmax(best[1])
        j_min = getmin(best[2])
        j_max = getmax(best[2])
        k_min = getmin(best[3])
        k_max = getmax(best[3])

        interval *= p['interval_shrink_factor']

    best = best_res(results)
    pt = time.time()-t

    if best is None: return {'Plan':None,'Value':0,'Processing time':pt,'Params':{'base':base, 'algorithm':f}}
    else: return {
        'Plan':best[4],
        'Value': best[5],
        'Processing time': pt,
        'Parameters':{
            'base':best[0],
            'algorithm':f,
            'familyhome_min_clearance':best[1],
            'bungalow_min_clearance':best[2],
            'mansion_min_clearance':best[3]
        }
    }

def perform_experiments(num_houses, enable_pg, bases, algorithms, params, frame):


    results = []
    for base in bases:
        for f in algorithms:
            if (f is not TightFitWB and base != "gp") or (f is TightFitWB and base == "gp"):
                results.append(
                    doit(
                        num_houses,
                        enable_pg,
                        base,
                        f,
                        frame,
                        params
                    )
                )

    return {'Constants':params,'Results':results}


def report(nh, pg, bases, settings, frame=None):
    return perform_experiments(nh, pg, bases, settings['algorithms'], settings['constants'], frame)
