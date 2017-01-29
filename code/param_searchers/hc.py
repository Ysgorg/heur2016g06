import time

from algos.Hillclimber_Random import HillClimber


def hc(base, experiment, num_candidates, frame=None):
    def best_res(res):
        bestone = None
        for r in res:
            if bestone is None or r[5] > bestone[5]: bestone = r
        return bestone

    t = time.time()
    try:
        best = HillClimber(base, experiment['constants'], num_candidates, frame).getPlan().deepCopy()
    except Exception:
        best = None
    pt = time.time() - t
    if best is None:
        o = {'Plan': None, 'Value': 0, 'Processing time': pt, 'Params': {}}
    else:
        o = {
            'Plan': best.serialize() if best.isValid() else None,
            'Value': best.getPlanValue() if best.isValid() else 0,
            'Processing time': pt,
            'Parameters': {}
        }

    return o
