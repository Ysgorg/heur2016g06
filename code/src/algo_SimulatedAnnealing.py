from random import random
from math import exp

import time

from src.GroundplanFrame import GroundplanFrame

def get_acceptance_threshold(current_value, new_value, temperature, max_temperature):
    difference = int(new_value - current_value)

    print temperature, new_value, current_value, new_value - current_value

    threshold = exp(difference / temperature)

    print "Threshold:", threshold, "\n"

    return threshold
    #return current_value - new_value / temperature # old function

def get_temperature(i, max_i):
    return max_i - i
    #return max_i - (i + 1 / max_i)

def simulated_annealing(init_state, max_iterations, generateNeighborFunc, visualize, timeout):

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
        temperature = get_temperature(i, max_iterations)

        accept_threshold = get_acceptance_threshold(int(state.getPlanValue()), int(neighbor.getPlanValue()), temperature, max_iterations)
        random_val = random()

        if neighbor.getPlanValue() >= state.getPlanValue():
            state = neighbor.deepCopy()
            if state.getPlanValue() > best_state.getPlanValue():
                best_state = state.deepCopy()
        elif accept_threshold > random_val:
            state = neighbor.deepCopy()

    #print ((time.time()-ms) / max_iterations )*1000, "ms per iteration"
    print "Max value found in", max_iterations, "iterations:", best_state.getPlanValue()

    return best_state
