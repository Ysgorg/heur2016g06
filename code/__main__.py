import os
import sys
import time
from pprint import pprint

from all import perform_all_experiments
from batch_configs.main_config import main_config
from batch_configs.test_config import test_config
from residence_placers.Other import make_great_plan
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

fname = 'main_results.csv' if len(sys.argv) == 1 or sys.argv[1] != 'test' else 'test_results.csv'


def run_main(frame, test):
    experiment_config = test_config if test else main_config
    pprint(experiment_config)
    res = perform_all_experiments(experiment_config, frame)

    with open(fname, 'w') as fp:
        fields = res[0]
        rows = res[1]

        import csv
        with open(fname, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for r in rows: writer.writerow(r)
        print 'saved results to', fname


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if 'vis' in sys.argv:
    frame = GroundplanFrame(Groundplan())
else:
    frame = None

t = time.time()

if 'other' in sys.argv:
    make_great_plan(frame)
elif 'full' in sys.argv:
    run_main(frame, False)
elif 'test' in sys.argv:
    run_main(frame, True)

print "procedure took", int((time.time() - t)), 'seconds'
