from random import random

import time

from src.GroundplanFrame import GroundplanFrame


def simulated_annealing(init_state, max_iterations, generateNeighborFunc,visualize):

    state = init_state.deepCopy()
    best_state = state

    if visualize:
        frame = GroundplanFrame(state)
        bframe = GroundplanFrame(state)

    ms=time.time()

    for i in range(max_iterations):

        if visualize:
            frame.repaint(state)
            bframe.repaint(best_state)

        neighbor = generateNeighborFunc(state.deepCopy())
        temperature = float(i + 1) / max_iterations

        if neighbor.getPlanValue() > state.getPlanValue():
            state = neighbor.deepCopy()
            if state.getPlanValue() > best_state.getPlanValue():
                best_state = state.deepCopy()
        elif (state.getPlanValue() - neighbor.getPlanValue()) / temperature > random():
            state = neighbor.deepCopy()

    print ((time.time()-ms) / max_iterations )*1000, "ms per iteration"