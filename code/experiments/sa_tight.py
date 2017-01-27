import time
from random import random

from algos.TightFitWB import TightFitWB
from algos.TightFit_A import validstate_tight
from bases.base_dynamic import base_dynamic
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame


def sa_tight(max_iterations,enable_playground,num_houses,visualize):


    visualize = False

    MIN = 10.0
    MAX = 80.0

    base = Groundplan(num_houses,False)

    def state(i,j,k):

        s = TightFitWB(base.deepCopy(),float(i)/10,float(j)/10,float(k/10)).getPlan().deepCopy()
        v = 0 if not s.isValid() else s.getPlanValue()
        return [i,j,k,v,s]

    def gen_neigbor(seed, temperature):

        def factor():

            magnitude = 100

            v = random()*(1 + temperature)
            if random()>0.5:v*=-1.0
            return v * magnitude * temperature

        def set_param(p,f):
            if random()<0.9:
                p += f*(0.5)
                if p > MAX: p = MAX
                elif p < MIN : p = MIN
            return p

        i = set_param(seed[0],factor())
        j = set_param(seed[1],factor())
        k = set_param(seed[2],factor())

        return state(i,j,k)



    current_state = state(10.0,10.0,25.0)

    init_state = current_state


    best_state = init_state

    current_frame = GroundplanFrame(init_state[4])
    best_frame = GroundplanFrame(best_state[4])
    neigbor_frame = GroundplanFrame(best_state[4])

    current_frame.repaint(init_state[4])

    init_time=time.time()

    for i in range(max_iterations-1):
        current_frame.repaint(current_state[4])
        temperature = 1-(float(i + 1) / max_iterations)
        if i % 10 == 0 : print temperature

        neigbor = gen_neigbor(current_state,temperature)

        if neigbor[3] == 0: continue

        #if visualize:neigbor_frame.repaint(neigbor[4])

        if neigbor[3] > current_state[3]:
            current_state = neigbor
            #if visualize: current_frame.repaint(neigbor[4])
            if current_state[3] > best_state[3]:
                #if visualize: best_frame.repaint(best_state[4])
                best_state = current_state
        elif (current_state[3] - neigbor[3]) / temperature > random():
            current_state = neigbor
            #if visualize: current_frame.repaint(neigbor[4])



    print "time",time.time()-init_time
    print ((time.time()-init_time)/ max_iterations )*1000, "ms per iteration"
    print "Max value found in", max_iterations, "iterations:", best_state[3]
    print best_state
    return best_state[4]
