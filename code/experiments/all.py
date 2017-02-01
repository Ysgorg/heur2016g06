import time

from algos.Hillclimber_Random import HillClimber
from param_searchers import zoom
from param_searchers.hc import hc
from param_searchers.sa_2 import sa_2


def perform_all_experiments(experiment_config, frame=None):

    name = "TightFit_A"
    expects = ['Waterbodies', "Playgrounds"]
    puts = ["Residences"]

    def valid_plan(base, algo):
        result = (set(base.puts) == set(algo.expects)) and \
               (not base.PLAYGROUND or "Playgrounds" in algo.puts or "Playgrounds" in base.puts)

        return result

    print "Performing all experiments"

    ec = experiment_config

    report = {"Config": experiment_config, "Results": []}


    counters = [0,0,0,0,0]

    # loops tailored for our experiments
    # todo generify

    for nh in ec['Problem instances']['Number of residences']:
        counters[0]+=1
        for pg in ec['Problem instances']['Enable playgrounds']:
            counters[1]+=1
            for dim in ec['Problem instances']['Area dimensions']:
                for prop in ec['Problem instances']['Building proportions']:
                    for experiment_key in ec['Experiments']:

                        counters[2]+=1

                        experiment = ec['Experiments'][experiment_key]

                        if "Bases" not in experiment['variables']:continue

                        if experiment_key == 'Zoom': f = zoom.zoom
                        elif experiment_key == 'SA': f = sa_2
                        elif experiment_key == 'HC': f = hc

                        for b in experiment['variables']['Bases']:

                            counters[3]+=1

                            base = b(nh, pg, width=dim['width'], height=dim['height']).deepCopy()

                            for wb_ in base.waterbodies: assert base.correctlyPlaced(wb_)
                            for pg_ in base.playgrounds: assert base.correctlyPlaced(pg_)

                            coordinates = {'nh': nh, 'pg': pg, 'dim': dim, 'prop': prop,'algo': experiment_key, 'base': base.name}

                            # todo generify

                            if experiment_key == 'Zoom' or experiment_key == 'SA':
                                variable = experiment['variables']['Tight Fit functions']
                                for v in variable:
                                    if not valid_plan(base,v):
                                        print('[skip]',base.name,v.name)
                                        continue
                                    counters[4]+=1
                                    coordinates['tf'] = v.name
                                    result = f(base.deepCopy(), experiment, v, frame)
                                    print counters, result['Value']
                                    report['Results'].append({'coordinates': coordinates,'result': result})

                            elif experiment_key == 'HillClimber':
                                variable = experiment['variables']["Number of candidate moves"]
                                for v in variable:
                                    counters[4]+=1
                                    coordinates['nc'] = v
                                    result = f(base.deepCopy(), experiment, v, frame)
                                    print counters , result['Value']
                                    report['Results'].append({'coordinates': coordinates,'result': result})

    return report
