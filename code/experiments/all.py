
import zoom_tight
from experiments import hc
from experiments import sa_1
from experiments import sa_2
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame


def perform_all_experiments(nh, pg, bases, algo_specific_params, frame=None):

    if frame is None: frame = GroundplanFrame(Groundplan(0,False))

    print "Performing all experiments"

    report = {}
    for n in nh:
        report[n] = {}
        for p in pg:
            report[n][p] = {
                "HillClimberRandom": hc.report(n, p, bases, algo_specific_params["HillClimberRandom"], frame),
                "SimulatedAnnealing_2": sa_2.report(n, p, bases, algo_specific_params["SimulatedAnnealing_2"], frame),
                "Zoom": zoom_tight.report(n, p, bases, algo_specific_params["Zoom"], frame)

                # sa_1 requires an init_state, which screws up the structure of the batch experiments
                #
                #"SimulatedAnnealing_1": sa_1.report(n, p, bases, algo_specific_params["SimulatedAnnealing_1"], frame),

            }

    return report