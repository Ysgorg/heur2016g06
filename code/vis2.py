import json
from visualizations.multiline_double_plot import multiline_double_plot, test_mdp
from visualizations.boxplot import plot_boxplot
import matplotlib.pyplot as plt

import glob

RESULTS_ARCHIVE = "old_results/"
VALUE_FILE = "values.json"

def series_metadata(param,variable):

    assert isinstance(variable,str)
    assert isinstance(param,dict)
    assert "base" in param
    assert "algo" in param
    assert "nh" in param
    assert 'pg' in param

    o = {
        "base":param['base'],
        "algo":param['algo'],
        "pg":param['pg'],
        "nh":param['nh']
    }

    if 'nc' in param: o['nc'] = param['nc']
    elif 'tf' in param: o['tf'] = param['tf']

    o['variant'] = variable

    o[variable] = '**variant**'

    return o

def compute_dataseries(data, variable):

    # todo generify

    def genkey(pretty_coords):
        t = pretty_coords[variable]
        pretty_coords[variable] = '**variant**'
        s = json.dumps(pretty_coords)
        pretty_coords[variable] = t
        return s

    rs = {}

    for i in data:

        meta = series_metadata(i['coordinates'],variable)
        assert variable in meta
        key = genkey(i['coordinates'])
        if not key in rs: rs[key] = [meta,[]]
        rs[key][1].append([i['coordinates'][variable], i['result']['Value'],i['result']['Processing time']])

    return [ v for v in rs.values() ]

def compute_spread(all_results, save_output=True):
    tests = []

    for test_num in dataset:
        value_row = []
        for dataset in all_results:
            value = test_num['result']['Value']
            value_row.append(value)
        tests.append(value_row)

    # save the output
    if save_output:
        with open(VALUE_FILE, 'w') as vf:
            json.dump(tests, vf)

    return tests


def load_old_results():
    old_results = []

    for filename in glob.iglob(RESULTS_ARCHIVE):
        print filename
        with open(filename) as data_file:
            data = json.load(data_file)
            old_results.append(data)

    return old_results

#test_mdp()

# load latest results file
with open('results.json') as data_file: data = json.load(data_file)
multiline_double_plot(plt, compute_dataseries(data, variable='nh'), separate_legend=True)

all_results = load_old_results().append(data) # load old results and append latest
plot_boxplot(plt, compute_spread(all_results, save_output=True))
plt.show()
