import time

from algos.Hillclimber_Random import HillClimber
from bases import base_a, base_b, base_c, base_dynamic


def perform_experiments(num_houses,enable_pg, bases, max_iterations, frame):

    results = []

    for base in bases:
        t=time.time()
        b = base(num_houses, enable_pg).deepCopy()
        r = HillClimber(b.deepCopy(),max_iterations).getPlan()
        v = r.getPlanValue() if r.isValid() else 0
        results.append(
            {
                "Parameters":{
                    "base":b.deepCopy()
                },
                "Processing time":time.time()-t,
                "Plan":r,
                "Value":v
            }
        )

    return results

def report(nh, pg, bases, settings, frame):

    return {
        "Constants":settings['constants']["max_iterations"],
        "Results": perform_experiments(nh,pg,bases, settings['constants']["max_iterations"], frame)
    }
