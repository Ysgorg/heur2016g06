import json
from pprint import pprint

from matplotlib.pyplot import savefig

from test_config import test_config

with open('results.json') as data_file:
    data = json.load(data_file)

config = test_config

res = {}

x_vals = test_config['Problem instances']['Number of residences']
for pg in test_config['Problem instances']['Enable playgrounds']:
    res[pg] = {}
    for exp in config['Experiments']:
        res[pg][exp] = {}
        for i in data:

            if i['coordinates']['experiment key'] == exp and i['coordinates']['pg'] == pg:

                o = {'value': i['result']['Value'],'time': i['result']['Processing time']}
                if 'Parameters' in i['result']: o['params'] = i['result']['Parameters']

                t = i['coordinates']['tf'] if 'tf' in i['coordinates'] else i['coordinates']['nc']
                b = i['coordinates']['base']
                nh = i['coordinates']['nh']

                if t not in res[pg][exp]:           res[pg][exp][t] = {}
                if b not in res[pg][exp][t]:        res[pg][exp][t][b] = {}
                res[pg][exp][t][b][nh] = o

def doit2(k1,k2,r):

    line = []

    for k in config['Problem instances']['Number of residences']:
        result = r[k]
        line.append(result[k2])

    import matplotlib.pyplot as plt
    plt.plot(config['Problem instances']['Number of residences'],line,marker='o',linestyle='--')
    plt.xlabel('Number of Residences')
    plt.ylabel(k2.upper())
    plt.savefig(k1+k2+'.png')
    plt.xticks(
        range(len(config['Problem instances']['Number of residences'])),
        config['Problem instances']['Number of residences'],
               rotation='vertical')
    plt.gcf().clear()

def doit(r,r1,r2,r3,j):
    key = 'imgs/'+str(r1)+str(r2)+str(r3)+str(j)
    doit2(key,'time',r[r1][r2][r3][j])
    doit2(key,'value',r[r1][r2][r3][j])

def plot_1(r):
    for r1 in r:
        for r2 in r[r1]:
            for r3 in r[r1][r2]:
                for j in r[r1][r2][r3]:
                    doit(r,r1,r2,r3,j)



plot_1(res)
"""
import matplotlib.pyplot as plt
#plt.plot(values)
plt.ylabel('some numbers')
plt.show()
"""
