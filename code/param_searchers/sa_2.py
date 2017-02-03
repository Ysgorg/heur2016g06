import time
from pprint import pprint
from random import random

from src.Groundplan import Groundplan


def sa_2(base, experiment, t, frame,slow=False):



    assert 'variables' in experiment
    assert 'constants' in experiment
    assert callable(t)

    constants = experiment['constants']

    def state(i, j, k, f):
        s = f(base.deepCopy(), i, j, k,frame=None,slow=False).getPlan().deepCopy()
        s.params = [i,j,k]
        if frame is not None: frame.repaint(s)
        v = 0 if not s.isValid() else s.getPlanValue()
        return [i, j, k, v, s]

    def gen_neigbor(seed, temperature, f):

        def factor():
            magnitude = 10.0
            v = random() * (1 + temperature)
            if random() > 0.5: v *= -1.0
            return v * magnitude * temperature

        def set_param(p, f):
            if random() < 0.9:
                p += f * 0.5
                if p > constants['max']:
                    p = constants['max']
                elif p < constants['min']:
                    p = constants['min']
            return p

        i = set_param(seed[0], factor())
        j = set_param(seed[1], factor())
        k = set_param(seed[2], factor())

        return state(i, j, k, f)

    current_state = state(1.0, 1.0, 1.0, t)

    init_state = current_state

    best_state = init_state

    init_time = time.time()


    for i in range(constants['max_iterations'] - 1):

        if slow: time.sleep(0.5)
        temperature = 1 - (float(i + 1) / constants['max_iterations'])


        assert isinstance(current_state[0],float)
        assert isinstance(current_state[1],float)
        assert isinstance(current_state[2],float)
        neigbor = gen_neigbor(current_state, temperature, t)

        if neigbor[3] == 0: continue




        if neigbor[3] > current_state[3]:
            current_state = neigbor
            if current_state[3] > best_state[3]:
                best_state = current_state
        elif (current_state[3] - neigbor[3]) / temperature > random():
            current_state = neigbor

    pt = time.time() - init_time

    return {
        'Plan': best_state[4],
        'Value': best_state[3],
        'Processing time': pt,
        'Parameters': {
            'familyhome_min_clearance': best_state[0],
            'bungalow_min_clearance': best_state[1],
            'mansion_min_clearance': best_state[2]
        }
    }
