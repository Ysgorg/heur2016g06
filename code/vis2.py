import json
from visualizations.multiline_double_plot import multiline_double_plot, test_mdp


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

test_mdp()

with open('results.json') as data_file: data = json.load(data_file)
multiline_double_plot(compute_dataseries(data, variable='nh'))
