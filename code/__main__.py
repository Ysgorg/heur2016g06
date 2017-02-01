import os
import sys
from pprint import pprint

import time

from algos.cleverer import make_great_plan
from experiments.all import perform_all_experiments
from main_config import main_config
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from test_config import test_config


def run_main(frame, test):
    experiment_config = test_config if test else main_config
    pprint(experiment_config)
    return perform_all_experiments(experiment_config, frame)


os.chdir(os.path.dirname(os.path.abspath(__file__)))

frame = GroundplanFrame(Groundplan())

make_great_plan(frame)


import json

t = time.time()

with open('results.json', 'w') as fp:
    results = run_main(frame, len(sys.argv) > 1 and sys.argv[1] == "test")
    json.dump(results['Results'], fp)

print "procedure took" , int((time.time()-t)),'seconds'