import os
import sys
import time
import json
from pprint import pprint

from all import perform_all_experiments
from batch_configs.main_config import main_config
from batch_configs.test_config import test_config
from residence_placers.Other import make_great_plan
from residence_placers.Other_2 import make_other_great_plan
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame

from visualizations.boxplot import plot_boxplot

json_results = 'all_main_results.json' if len(sys.argv) == 1 or sys.argv[1] != 'test' else 'all_test_results.json'
fname = 'main_results.csv' if len(sys.argv) == 1 or sys.argv[1] != 'test' else 'test_results.csv'

def run_main(frame, test):
    experiment_config = test_config if test else main_config
    pprint(experiment_config)
    res = perform_all_experiments(experiment_config, frame)


    fields = res[0]
    rows = res[1]

    import csv
    with open(fname, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for r in rows: writer.writerow(r)
        print 'saved results to', fname

    fname2="value_per_iteration.csv"
    with open(fname2, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(res[2]['lines'])
        print "saved results to",fname2,

    # Store new results with all previous
    # if already exists, read contents to current_results
    current_results = []
    if os.path.exists(json_results):
        with open(json_results, 'r') as old_results:
            current_results = json.load(old_results)
            if current_results == None:
                current_results = []

    current_results.append(res[1])
    with open(json_results, 'w') as json_write:
        json.dump(current_results, json_write, indent=2)

    # Plot all samples on boxplots (Value and time), store in fname.png
    plot_boxplot(current_results, fname+'.png')



os.chdir(os.path.dirname(os.path.abspath(__file__)))

if 'vis' in sys.argv:
    frame = GroundplanFrame(Groundplan())
else:
    frame = None

t = time.time()

if 'other' in sys.argv:
    make_great_plan(frame)
if 'other_2' in sys.argv:
    make_other_great_plan(frame)
elif 'full' in sys.argv:
    run_main(frame, False)
elif 'test' in sys.argv:
    run_main(frame, True)

print "procedure took", int((time.time() - t)), 'seconds'
