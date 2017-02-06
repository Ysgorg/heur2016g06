def simulated_annealing(init_state, max_iterations):
    state = init_state
    best_state = state
    for i in range(max_iterations):
        neighbor = generateNeighbor(state)
        if value(neighbor) > value(state):
            # the generated neighbor state is better than current state
            # so we make it our new current state
            state = neighbor
            if value(state) > value(best_state):
                # the state is the best found so far
                # so update best_state
                best_state = state
        elif (value(neighbor) - value(state)) / temperature > random():
            # the generated was not better than our current state
            # , but since the temperature (times random factor) is high
            # , we make it our new current state anyway
            state = neighbor
