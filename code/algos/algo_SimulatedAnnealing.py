import os
from random import random

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
def simulated_annealing(init_state, max_iterations, generateNeighborFunc):

    print type(init_state)

    state = init_state.deepCopy()
    best_state = state.deepCopy()

    for i in range(max_iterations):
        neighbor = generateNeighborFunc(state.deepCopy())
        temperature = float(i + 1) / max_iterations
        if neighbor.getPlanValue() > state.getPlanValue():                              state = neighbor.deepCopy()
        if state.getPlanValue() > best_state.getPlanValue():                            best_state = state.deepCopy()
        elif (state.getPlanValue() - neighbor.getPlanValue()) / temperature > random(): state = neighbor.deepCopy()

    return best_state
