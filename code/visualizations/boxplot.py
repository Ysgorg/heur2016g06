import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
import os
import string

label_rotation = 45
dpi_val = 100
graph_width = 19.2
graph_height = 18

def plot_boxplot(data_sets, fname):
    results = process_results(data_sets)

    #print json.dumps(results, indent=2)

    value_sets = []
    time_sets = []
    labels = []

    for key, obj in results.iteritems():
        if key not in labels:
            labels.append(key)
        value_sets.append(obj['values'])
        time_sets.append(obj['times'])

    plt.figure()

    figure = plt.gcf() # get current figure
    figure.set_size_inches(graph_width, graph_height)

    plt.title("Plan Value"+" ("+str(len(value_sets[0]))+" samples)")
    plt.boxplot(value_sets, labels=labels)
    plt.xticks(rotation=label_rotation)
    plt.xlabel("Experimental Setup")
    plt.ylabel("Plan Value")

    plt.savefig("plan_value_"+fname, dpi=dpi_val)

    plt.figure()

    figure = plt.gcf() # get current figure
    figure.set_size_inches(graph_width, graph_height)

    plt.title("Processing Time"+" ("+str(len(time_sets[0]))+" samples)")
    plt.boxplot(time_sets, labels=labels)
    plt.xticks(rotation=label_rotation)
    plt.xlabel("Experimental Setup")
    plt.ylabel("Time in seconds")

    plt.savefig("processing_time_"+fname, dpi=dpi_val)

    plt.close()

def process_results(all_results):
    results = {}

    for test_set in all_results:
        for test in test_set:
            num_houses =  str(test['Number of residences'])
            plan_value =  test['Plan value']
            playground = test['Enable playground']
            time =  test['Processing time']
            placer =  str(test['Residence placer'])
            base = str(test['Base'])

            if 'Search function' in test:
                search = str(test['Search function'])
            else:
                search = ""

            # Failed at getting string replace to work, hence this...
            if "TightFit_A" in placer:
                placer = "TFA"
            elif "TightFit_B" in placer:
                placer = "TFB"

            if "A" in base:
                base = "bA"
            elif "B" in base:
                base = "bB"
            elif "C" in base:
                base = "bC"
            elif "dynamic" in base:
                base = "bDy"

            if playground == True:
                playground = "PG"
            else:
                playground = ""

            key = num_houses+':'+base+':'+placer+':'+search

            if not key in results:
                results[key] = {}

            if not 'values' in results[key]:
                results[key]['values'] = []
            results[key]['values'].append(plan_value)

            if not 'times' in results[key]:
                results[key]['times'] = []
            results[key]['times'].append(time)

    return results
