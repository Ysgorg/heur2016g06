import time

from param_searchers import zoom
from param_searchers.simulated_annealing import sa_2
from residence_placers.HillClimber import HillClimber
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame


def print_log_line(plan, counters, t, init_time, best, frame):
    frame.repaint(plan)
    value = str(0 if not plan.isValid() else int(plan.getPlanValue()))
    processing_time = str(int(time.time() - t))  # ms
    total_time = str(int(time.time() - init_time))
    print counters, '\t' + value + '\t' + processing_time + '\t\t' + total_time + '\t\t' + str(int(best.getPlanValue()))


def perform_all_experiments(experiment_config, frame=None):
    """ perform a set of experiments, as determined by experiment_config"""

    frame_2 = GroundplanFrame(Groundplan())

    print "Performing all experiments"

    print '-----------------------------------------------------------------'
    print 'counters\tvalue\t\tprocessing time\ttotal time\tbest value'
    print '-----------------------------------------------------------------'

    name = "TightFit_A"
    expects = ['Waterbodies', "Playgrounds"]
    puts = ["Residences"]

    fields = ['Number of residences', 'Enable playground', 'Search function', 'Base', 'Residence placer',
              'Mansion clearance', 'Bungalow clearance', 'Familyhome clearance', 'Plan value'
        , 'Number of candidates', 'Processing time']

    rows = []
    lines = []

    def valid_plan(base, algo):
        result = (set(base.puts) == set(algo.expects)) and \
                 (not base.PLAYGROUND or "Playgrounds" in algo.puts or "Playgrounds" in base.puts)

        return result

    ec = experiment_config

    report = {"Config": experiment_config, "Results": []}

    init_time = time.time()

    counters = [0, 0, 0, 0]

    best = None

    # loops tailored for our experiments
    # todo generify

    counters[0] = 0
    for nh in ec['Problem instances']['Number of residences']:
        counters[0] += 1
        counters[1] = 0
        for pg in ec['Problem instances']['Enable playgrounds']:
            counters[1] += 1
            counters[2] = 0

            for dim in ec['Problem instances']['Area dimensions']:
                for prop in ec['Problem instances']['Building proportions']:
                    for experiment_key in ec['Experiments']:

                        counters[2] += 1

                        experiment = ec['Experiments'][experiment_key]

                        if "Bases" not in experiment['variables']: continue

                        if experiment_key == 'Zoom':
                            f = zoom.zoom
                        elif experiment_key == 'SA':
                            f = sa_2

                        for b in experiment['variables']['Bases']:

                            counters[2] += 1
                            counters[3] = 0

                            base = b(nh, pg, width=dim['width'], height=dim['height']).deepCopy()

                            for wb_ in base.waterbodies: assert base.correctlyPlaced(wb_)
                            for pg_ in base.playgrounds: assert base.correctlyPlaced(pg_)

                            # todo generify

                            if experiment_key == 'Zoom' or experiment_key == 'SA':
                                variable = experiment['variables']['Tight Fit functions']
                                for v in variable:
                                    if not valid_plan(base, v): continue

                                    t = time.time()
                                    sf = f(base.deepCopy(), experiment['constants'], v, frame)
                                    result = sf['Plan']
                                    tim = time.time() - t
                                    if best is None or result.getPlanValue() > best.getPlanValue(): best = result
                                    counters[3] += 1
                                    print_log_line(result, counters, t, init_time, best, frame_2)

                                    lines.append(
                                        [
                                            nh,
                                            pg,
                                            base.name,
                                            experiment_key,
                                            result.getPlanValue(),
                                            v.name
                                        ] + sf['it_vals']
                                    )
                                    sf['it_vals']=[]

                                    rows.append({
                                        'Number of residences': nh,
                                        'Enable playground': pg,
                                        'Search function': experiment_key,
                                        'Base': base.name,
                                        'Residence placer': v.name,
                                        'Plan value': result.getPlanValue() if result.isValid() else 0,
                                        'Processing time': tim,
                                        'Familyhome clearance': result.params[0],
                                        'Bungalow clearance': result.params[1],
                                        'Mansion clearance': result.params[2]
                                    })

                            elif experiment_key == 'HC':

                                if not valid_plan(base, HillClimber): continue

                                for v in experiment['variables']["Number of candidate moves"]:

                                    t = time.time()
                                    hc = HillClimber(base.deepCopy(), {'max_iterations': 1000,'number_of_candidate_moves': v}, frame)
                                    result = hc.getPlan().deepCopy()
                                    tim = time.time() - t
                                    if best is None or result.getPlanValue() > best.getPlanValue(): best = result
                                    counters[3] += 1
                                    print_log_line(result, counters, t, init_time, best, frame_2)
                                    lines.append([nh,pg,base.name,experiment_key,result.getPlanValue(),v]+hc.iteration_value_rows)
                                    hc.iteration_value_rows=[]

                                    rows.append({
                                        'Number of residences': nh,
                                        'Enable playground': pg,
                                        'Base': base.name,
                                        'Residence placer': experiment_key,
                                        'Plan value': result.getPlanValue() if result.isValid() else 0,
                                        'Processing time': tim,
                                        'Number of candidates': v
                                    })

        GroundplanFrame(best).repaint(best,"Overall best for nh="+str(nh))

    return [fields, rows,{'lines':lines}]
