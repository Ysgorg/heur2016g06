import time

from algos.Hillclimber_Random import HillClimber
from param_searchers import zoom
from param_searchers.hc import hc
from param_searchers.sa_2 import sa_2
from src.Groundplan import Groundplan


def print_log_line(plan, counters, t, init_time, best):
    value = str(0 if not plan.isValid() else int(plan.getPlanValue()))
    processing_time = str(int(time.time() - t)) # ms
    total_time = str(int(time.time()-init_time))
    print counters,'\t'+ value+'\t'+ processing_time+'\t\t'+ total_time+'\t\t'+ str(best.getPlanValue())


def perform_all_experiments(experiment_config, frame=None):

    print "Performing all experiments"

    print '-----------------------------------------------------------------'
    print 'counters\tvalue\t\tprocessing time\ttotal time\tbest value'
    print '-----------------------------------------------------------------'

    name = "TightFit_A"
    expects = ['Waterbodies', "Playgrounds"]
    puts = ["Residences"]

    fields = ['Number of residences','Enable playground','Search function','Base','Residence placer',
              'Mansion clearance','Bungalow clearance','Familyhome clearance','Plan value'
              ,'Number of candidates', 'Processing time']

    rows = []

    def valid_plan(base, algo):
        result = (set(base.puts) == set(algo.expects)) and \
               (not base.PLAYGROUND or "Playgrounds" in algo.puts or "Playgrounds" in base.puts)

        return result

    ec = experiment_config

    report = {"Config": experiment_config, "Results": []}

    init_time = time.time()


    counters = [0,0,0,0]

    best = None

    # loops tailored for our experiments
    # todo generify

    for nh in ec['Problem instances']['Number of residences']:
        counters[0]=0
        for pg in ec['Problem instances']['Enable playgrounds']:
            counters[0]+=1
            counters[1]=0
            for dim in ec['Problem instances']['Area dimensions']:
                for prop in ec['Problem instances']['Building proportions']:
                    for experiment_key in ec['Experiments']:

                        counters[1]+=1
                        counters[2]=0

                        experiment = ec['Experiments'][experiment_key]

                        if "Bases" not in experiment['variables']:continue

                        if experiment_key == 'Zoom': f = zoom.zoom
                        elif experiment_key == 'SA': f = sa_2
                        elif experiment_key == 'HC': f = hc


                        for b in experiment['variables']['Bases']:

                            counters[2]+=1
                            counters[3]=0

                            base = b(nh, pg, width=dim['width'], height=dim['height']).deepCopy()

                            for wb_ in base.waterbodies: assert base.correctlyPlaced(wb_)
                            for pg_ in base.playgrounds: assert base.correctlyPlaced(pg_)

                            # todo generify

                            if experiment_key == 'Zoom' or experiment_key == 'SA':
                                variable = experiment['variables']['Tight Fit functions']
                                for v in variable:
                                    if not valid_plan(base,v): continue

                                    t = time.time()
                                    res_ = f(base.deepCopy(), experiment, v, frame)['Plan']
                                    tim = time.time()-t
                                    if best is None or result.getPlanValue() > best.getPlanValue(): best = result
                                    counters[3]+=1
                                    print_log_line(res_,counters,t,init_time,best)

                                    rows.append({
                                        'Number of residences':nh,
                                        'Enable playground':pg,
                                        'Search function':experiment_key,
                                        'Base':base.name,
                                        'Residence placer': v.name,
                                        'Plan value': res_.getPlanValue() if res_.isValid() else 0,
                                        'Processing time': tim,
                                        'Familyhome clearance':res_.params[0],
                                        'Bungalow clearance':res_.params[1],
                                        'Mansion clearance':res_.params[2]
                                    })

                            elif experiment_key == 'HC':

                                if not valid_plan(base,HillClimber): continue

                                for v in experiment['variables']["Number of candidate moves"]:

                                    t = time.time()
                                    result = HillClimber(base.deepCopy(),{'max_iterations':1000},v,frame).getPlan().deepCopy()
                                    tim = time.time()-t
                                    if best is None or result.getPlanValue() > best.getPlanValue(): best = result
                                    counters[3]+=1
                                    print_log_line(result,counters,t,init_time,best)

                                    rows.append({
                                        'Number of residences':nh,
                                        'Enable playground':pg,
                                        'Base':base.name,
                                        'Residence placer': experiment_key,
                                        'Plan value': result.getPlanValue() if result.isValid() else 0,
                                        'Processing time': tim,
                                        'Number of candidates':v
                                    })


    return [fields,rows]