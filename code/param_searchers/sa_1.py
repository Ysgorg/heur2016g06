from algos import TightFit_A
from algos.SimulatedAnnealing import simulated_annealing
from neighborfunctions import neighbor_tight


def perform_experiments(nh, pg, bases, init_states, neigbor_functions, max_iterations, frame):
    results = []

    for base in bases:

        b = base(nh, pg).deepCopy()
        for init_s in init_states:
            if init_s == TightFit_A.TightFit_A:
                ins = init_s(b.deepCopy(), 1.0, 1.0, 1.0).getPlan().deepCopy()
            else:
                try:
                    ins = init_s(b.deepCopy()).getPlan().deepCopy()
                except Exception:
                    continue
            if frame is not None: frame.repaint(ins)
            for ng in neigbor_functions:
                if ng == neighbor_tight.neighbor_tight and not init_s == TightFit_A.TightFit_A: continue
                r = simulated_annealing(ins.deepCopy(), max_iterations, ng)
                v = r.getPlanValue() if r.isValid() else 0
                results.append([nh, pg, base, r, v])

    return results


def construct_report(experiment):
    return experiment


def sa_1(num_houses, enable_pg, settings, frame=None):
    return construct_report(perform_experiments(num_houses, enable_pg, settings['init_state_functions'],
                                                settings['neigbor_functions'], settings['max_iterations'], frame))
