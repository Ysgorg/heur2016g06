import time
from random import random

from src.Groundplan import Groundplan


def sa_tight(max_iterations, enable_playground, num_houses, frame, f):

    MIN = 1.0
    MAX = 10.0

    base = Groundplan(num_houses, enable_playground)

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
                if p > MAX: p = MAX
                elif p < MIN: p = MIN
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

    for i in range(max_iterations - 1):
        frame.repaint(current_state[4])
        temperature = 1 - (float(i + 1) / max_iterations)
        if i % 10 == 0: print "temperature",round(temperature)

        neigbor = gen_neigbor(current_state, temperature, f)

        if neigbor[3] == 0: continue

        if neigbor[3] > current_state[3]:
            current_state = neigbor
            if current_state[3] > best_state[3]:
                best_state = current_state
        elif (current_state[3] - neigbor[3]) / temperature > random():
            current_state = neigbor

    print "time", time.time() - init_time
    print ((time.time() - init_time) / max_iterations) * \
        1000, "ms per iteration"
    print "Max value found in", max_iterations, "iterations:", best_state[3]
    print best_state
    return best_state[4]
