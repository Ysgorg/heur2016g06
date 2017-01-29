from algos.Hillclimber_Random import HillClimber
from param_searchers import zoom
from param_searchers.hc import hc
from param_searchers.sa_2 import sa_2


def perform_all_experiments(experiment_config, frame=None):
    def valid_plan(base, algo):
        ok = (set(base.puts) == set(algo.expects)) and (
            not base.PLAYGROUND or "Playgrounds" in algo.puts or "Playgrounds" in base.puts)
        # print(base.puts, algo.expects, ok),
        return ok

    print "Performing all experiments"

    ec = experiment_config

    report = {"Config": experiment_config, "Results": []}

    for nh in ec['Problem instances']['Number of residences']:
        for pg in ec['Problem instances']['Enable playgrounds']:
            for dim in ec['Problem instances']['Area dimensions']:
                for prop in ec['Problem instances']['Building proportions']:
                    for experiment_key in ec['Experiments']:

                        experiment = ec['Experiments'][experiment_key]

                        if "Bases" not in experiment['variables']:
                            continue

                        # loops tailored for our experiments
                        # todo generify

                        if experiment_key == 'Zoom':
                            param_search_method = zoom.zoom
                        elif experiment_key == 'SimulatedAnnealing_2':
                            param_search_method = sa_2
                        elif experiment_key == 'HillClimberRandom':
                            param_search_method = hc

                        for b in experiment['variables']['Bases']:

                            base = b(nh, pg, width=dim['width'], height=dim['height']).deepCopy()

                            if experiment_key == 'Zoom' or experiment_key == 'SimulatedAnnealing_2':

                                for t in experiment['variables']['Tight Fit functions']:

                                    if not valid_plan(base, t): continue

                                    report['Results'].append({
                                        'coordinates': {'nh': nh, 'pg': pg, 'dim': dim, 'prop': prop,
                                                        'experiment key': experiment_key, 'base': base.name,
                                                        'tf': t.name},
                                        'result': param_search_method(base.deepCopy(), experiment, t, frame)
                                    })

                            elif experiment_key == 'HillClimberRandom':

                                if not valid_plan(base, HillClimber): continue

                                for i in experiment['variables']["Number of candidate moves"]:
                                    report['Results'].append(
                                        {
                                            'coordinates': {'nh': nh, 'pg': pg, 'dim': dim, 'prop': prop,
                                                            'experiment key': experiment_key, 'base': base.name,
                                                            'nc': i},
                                            'result': param_search_method(base.deepCopy(), experiment, i, frame)
                                        }
                                    )

    return report
