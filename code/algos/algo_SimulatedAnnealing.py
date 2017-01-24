import os
from random import random
from math import exp

import time

import errno

import signal
from six import wraps

from src.GroundplanFrame import GroundplanFrame

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:result = func(*args, **kwargs)
            finally:signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


@timeout(50)

def get_acceptance_probability(current_value, new_value, temperature, max_temperature):
    if temperature == 0:
        return 0.0
    else:
        difference = new_value - current_value
        threshold = exp(difference / (temperature * float(max_temperature)))

        return threshold

def get_temperature(i, max_i):
    #return float(max_i - i)
    return (1.0 - (float(i + 1) / float(max_i)))

def simulated_annealing(init_state, max_iterations, generateNeighborFunc, visualize, timeout):
    state = init_state.deepCopy()
    best_state = state

    jump_count = 0 # Number of probabilistic jumps to a lower value state
    quartile = 1

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

        if i >= ((max_iterations / 4) * quartile):
            print "Jumps in quartile", quartile, ":", jump_count
            quartile += 1
            jump_count = 0

        neighbor = generateNeighborFunc(state.deepCopy(),timeout)
        temperature = get_temperature(i, max_iterations)

        # If the new plan has a lower value, calculate the acceptance threshold of still accepting this state (probability decreases as temperature does)
        if neighbor.getPlanValue() < state.getPlanValue():
            accept_probability = get_acceptance_probability(state.getPlanValue(), neighbor.getPlanValue(), temperature, max_iterations)
            random_val = random()

            if accept_probability > random_val:
                state = neighbor.deepCopy()
                jump_count += 1
                #print "Accepted new state with probability: ", accept_probability, ">", random_val

        else:
            state = neighbor.deepCopy()
            #print "Better state found"

        if state.getPlanValue() > best_state.getPlanValue():
            best_state = state.deepCopy()
            print "T =", temperature, "New best value:", state.getPlanValue()

    print "Jumps in quartile", quartile, ":", jump_count
    print "Max value found in", max_iterations, "iterations:", best_state.getPlanValue()

    return best_state
