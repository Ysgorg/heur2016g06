from random import random

from algos.TightFit_A import validstate_tight


def neighbor_tight(state, temperature):
    MIN = 1.0
    MAX = 8.0

    # print temperature, state.params

    temperature = 1 - temperature

    seed = state.deepCopy()

    while len(seed.residences) > 0:
        seed.removeResidence(seed.getResidence(0))

    def generate_state(i, j, k):
        return validstate_tight(seed.deepCopy(), i, j, k).getPlan().deepCopy()

    def factor():
        v = random() * (1 + temperature)
        if random() > 0.5:
            v *= -1.0
        return v * 500 * temperature

    def set_param(p, f):
        if random() < 0.9:
            p += f * (0.5)
            if p > MAX:
                p = MAX
            elif p < MIN:
                p = MIN
        return p

    a = state.params[0]
    b = state.params[1]
    c = state.params[2]

    i = set_param(a, factor())
    j = set_param(b, factor())
    k = set_param(c, factor())

    return generate_state(i, j, k).deepCopy()
