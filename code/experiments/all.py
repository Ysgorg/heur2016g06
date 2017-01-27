import best
import zoom_tight
from experiments import hc
from experiments import sa


def clean_out_data():
    import os
    filelist = [f for f in os.listdir("plans")]
    for f in filelist:
        os.remove("plans/" + f)


def perform_all_experiments(frame):
    clean_out_data()

    print "Performing all experiments"

    report = {
        #"GreedyRandom": hc.report(frame),
        #"simulated_annealing": sa.report(frame),
        "tight": zoom_tight.report(frame)
    }
    report['best'] = best.report(report)
    frame.repaint(report['best'][6])
    print "Best: ", report
    while True:
        pass
    """
    from algos.Hillclimber_Random import HillClimber
    overall_best = HillClimber(report['best'][6].deepCopy(),frame=frame).getPlan()
    print "best:",overall_best
    frame.repaint(overall_best)
    """
