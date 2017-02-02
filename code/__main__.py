import os
import sys
import time
from pprint import pprint
import datetime

import time

from algos.c2 import make_great_plan
from experiments.all import perform_all_experiments
from main_config import main_config
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from test_config import test_config

RESULTS_FILE = "results.json"
RESULTS_ARCHIVE = "old_results/"

def run_main(frame, test):
    experiment_config = test_config if test else main_config
    pprint(experiment_config)
    return perform_all_experiments(experiment_config, frame)


os.chdir(os.path.dirname(os.path.abspath(__file__)))

frame = GroundplanFrame(Groundplan())

if len(sys.argv) > 1 and sys.argv[1] == "other":
    make_great_plan(frame)
    exit(0)


import json

t = time.time()

# if results.json already exists, archive before writing a new one
if os.path.isfile(RESULTS_FILE):
    print RESULTS_FILE, "already exists. Movign to restults_old/"
    stamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S')
    os.rename(RESULTS_FILE, RESULTS_ARCHIVE + stamp + ".json")

with open(RESULTS_FILE, 'w') as fp:
    results = run_main(frame, len(sys.argv) > 1 and sys.argv[1] == "test")
    json.dump(results['Results'], fp)

print "procedure took" , int((time.time()-t)),'seconds'
