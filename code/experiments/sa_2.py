import time
from random import random

from src.Groundplan import Groundplan


def sa_tight(constants, enable_playground, num_houses, frame, f, base):

    def state(i, j, k, f):
        s = f(base.deepCopy(), i, j, k).getPlan().deepCopy()
        v = 0 if not s.isValid() else s.getPlanValue()
        return [i, j, k, v, s]

    def gen_neigbor(seed, temperature, f):

        def factor():
            magnitude = 10
            v = random() * (1 + temperature)
            if random() > 0.5: v *= -1.0
            return v * magnitude * temperature

        def set_param(p, f):
            if random() < 0.9:
                p += f * (0.5)
                if p > constants['max']: p = constants['max']
                elif p < constants['min']: p = constants['min']
            return p

        i = set_param(seed[0], factor())
        j = set_param(seed[1], factor())
        k = set_param(seed[2], factor())

        return state(i, j, k, f)

    current_state = state(1.1, 1.1, 1.1,f)

    init_state = current_state

    best_state = init_state

    frame.repaint(init_state[4])

    init_time = time.time()

    for i in range(constants['max_iterations'] - 1):
        frame.repaint(current_state[4])
        temperature = 1 - (float(i + 1) / constants['max_iterations'])

        neigbor = gen_neigbor(current_state, temperature, f)

        if neigbor[3] == 0: continue

        if neigbor[3] > current_state[3]:
            current_state = neigbor
            if current_state[3] > best_state[3]:
                best_state = current_state
        elif (current_state[3] - neigbor[3]) / temperature > random():
            current_state = neigbor

    pt = time.time() - init_time

    return {
        'Plan':best_state[4],
        'Value': best_state[3],
        'Processing time': pt,
        'Parameters':{
            'base':base.deepCopy(),
            'algorithm':f,
            'familyhome_min_clearance':best_state[0],
            'bungalow_min_clearance':best_state[1],
            'mansion_min_clearance':best_state[2]
        }
    }

def perform_experiments(nh,pg,bases,algorithms,constants,frame):
    results = []
    for b in bases:
        for f in algorithms:
            results.append(sa_tight(constants,pg,nh,frame,f,b(nh,pg).deepCopy()))
    return {"Constants":constants,"Results":results}

def report(nh, pg, bases, settings, frame=None):
    return perform_experiments(nh, pg, bases, settings['algorithms'], settings['constants'], frame)