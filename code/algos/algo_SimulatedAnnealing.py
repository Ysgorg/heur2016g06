import os
from random import random
from math import exp

from src.GroundplanFrame import GroundplanFrame

# A list of JUMP_SAMPLES number of jumps will be stored
JUMP_SAMPLES = 10
MIN_PERCENTAGE_CHANGE = 0.01 # Minimum percentage change (out of 1) between new best and last best, which when reached terminates the search

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

def simulated_annealing(init_state, max_iterations, generateNeighborFunc, visualize):
    state = init_state.deepCopy()
    best_state = state
    jumps_list = [None]*JUMP_SAMPLES
    jump_count = 0 # Number of probabilistic jumps to a lower value state
    sample_number = 0

    if visualize:
        frame = GroundplanFrame(state)
        bframe = GroundplanFrame(state)

    for i in range(max_iterations):
        if visualize:
            frame.repaint(state)
            bframe.repaint(best_state)

        if i >= ((max_iterations / JUMP_SAMPLES) * sample_number):
            jumps_list[sample_number-1] = jump_count
            sample_number += 1
            jump_count = 0

        temperature = get_temperature(i, max_iterations)
        neighbor = generateNeighborFunc(state.deepCopy(), temperature)

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
            prev_best = best_state.deepCopy()
            best_state = state.deepCopy()
            print "T =", temperature, "New best value:", state.getPlanValue()

            if (1.0 - prev_best.getPlanValue() / best_state.getPlanValue()) * 100 <= MIN_PERCENTAGE_CHANGE:
                print "Change between previous best and current best less than", MIN_PERCENTAGE_CHANGE, "% Terminating search."
                break

    jumps_list[sample_number-1] = jump_count
    print "Probabilistic jumps made in each section:", jumps_list
    print "Max value found in", i, "iterations:", best_state.getPlanValue()

    return best_state
