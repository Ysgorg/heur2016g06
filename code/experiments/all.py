
import evo, tight, sa, best, printer
from bases.base_b import base_b
from src.GroundplanFrame import GroundplanFrame


def clean_out_data():
    import os
    filelist = [ f for f in os.listdir("plans") ]
    for f in filelist:
        os.remove("plans/"+f)

def perform_all_experiments():


    clean_out_data()

    frame = GroundplanFrame(base_b(num_houses=40,enable_playground=True).developGroundplan())

    report = {
        #"evolution": evo.report(frame),
        #"simulated_annealing": sa.report(frame),
        "tight": tight.report(frame)
    }

    #report['best'] = best.report(report,frame)

    #for r in report:
     #   printer.print_report(report,frame)

