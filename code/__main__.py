import os
import sys
from pprint import pprint

import time

from algos.heur_kno import make_great_plan
from experiments.all import perform_all_experiments
from main_config import main_config
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from test_config import test_config
from test_short_config import test_short_config


def run_main(frame, test):
    experiment_config = test_config if test else main_config
    pprint(experiment_config)
    return perform_all_experiments(experiment_config, frame)


os.chdir(os.path.dirname(os.path.abspath(__file__)))

frame = None#GroundplanFrame(Groundplan())

if len(sys.argv) > 1 and sys.argv[1] == "other":
    make_great_plan(frame)
    exit(0)


import json

t = time.time()

fname = 'main_results.json' if sys.argv == 0 or sys.argv[1]!='test' else 'test_results.json'

with open(fname, 'w') as fp:
    res = run_main(frame, len(sys.argv) > 1 and sys.argv[1] == "test")
    fields = res[0]
    rows = res[1]

    import csv
    with open(fname, 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for r in rows: writer.writerow(r)

print "procedure took" , int((time.time()-t)),'seconds'