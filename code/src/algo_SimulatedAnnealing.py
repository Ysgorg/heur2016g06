from random import random

import time

from src.GroundplanFrame import GroundplanFrame


def simulated_annealing(init_state, max_iterations, generateNeighborFunc,visualize,timeout):

    #print init_state.isValid()

    state = init_state.deepCopy()
    best_state = state

    if visualize:
        frame = GroundplanFrame(state)
        bframe = GroundplanFrame(state)

    init_time=time.time()

    for i in range(max_iterations):

        run_time = time.time()-init_time

        if run_time >= timeout:
            return best_state

        if visualize:
            frame.repaint(state)
            bframe.repaint(best_state)

        neighbor = generateNeighborFunc(state.deepCopy(),timeout)
        temperature = float(i + 1) / max_iterations

        if neighbor.getPlanValue() > state.getPlanValue():
            state = neighbor.deepCopy()
            if state.getPlanValue() > best_state.getPlanValue():
                best_state = state.deepCopy()
        elif (state.getPlanValue() - neighbor.getPlanValue()) / temperature > random():
            state = neighbor.deepCopy()



    #print ((time.time()-ms) / max_iterations )*1000, "ms per iteration"
    print "Max value found in", max_iterations, "iterations:", best_state.getPlanValue()

    return best_state
