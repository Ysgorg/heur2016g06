from algos.algo_Evolver import algo_Evolver
from bases import base_a, base_b, base_c, base_dynamic
from src.validstate_tight import validstate_tight


def perform_experiment(variables,frame):


    MIN = 10
    MAX = 60
    INTERVAL = 5

    results = []

    for num_houses in variables[0]:
        for enable_pg in variables[1]:
            for base in variables[2]:
                bas = base(num_houses=num_houses,enable_playground=enable_pg).developGroundplan()
                for i in range(MIN,MAX,INTERVAL):
                    a = float(i)/10
                    for j in range(MIN,MAX,INTERVAL):
                        b = float(j)/10
                        for k in range(MIN,MAX,INTERVAL):
                            c = float(k)/10
                            r = validstate_tight(bas.deepCopy(), a, b, c,visualize=False).getPlan().deepCopy()
                            frame.repaint(r)
                            v = r.getPlanValue() if r.isValid() else -1
                            results.append([num_houses,enable_pg,base, r, v])


    for num_houses in variables[0]:
        for enable_pg in variables[1]:
            for base in variables[2]:
                r = algo_Evolver(base(num_houses,enable_pg).developGroundplan()).getPlan()
                results.append([num_houses,enable_pg,base, r, r.getPlanValue()])
    return results

def construct_report(experiment):
    return experiment

def report(frame):
    experiment_variables = [
        [40, 70, 100],
        [True, False],
        [base_dynamic.base_dynamic, base_a.base_a, base_b.base_b]
    ]
    return construct_report(perform_experiment(experiment_variables,frame))

