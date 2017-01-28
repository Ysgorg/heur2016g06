import logging
import types
import unittest

import sys

from algos.TightFit_A import TightFit_A
from algos.TightFit_B import TightFit_B
from algos.TightFitWB import TightFitWB
from bases.base_a import base_a
from bases.base_b import base_b
from bases.base_c import base_c
from bases.base_dynamic import base_dynamic
from experiments.all import perform_all_experiments
from neighborfunctions.neighbor_random import neighbor_random
from neighborfunctions.neighbor_tight import neighbor_tight
from src.Groundplan import Groundplan


class PrimesTestCase(unittest.TestCase):

    # report keys, in increasing depth
    problem_instances_nh = [40#,70,100
                            ]
    problem_instances_pg = [#True,
                            False]
    experiment_keys = [
        'HillClimberRandom',
        'SimulatedAnnealing_2',
        'Zoom'
    ]
    report_fields = ['Constants', 'Results']
    result_fields = ['Plan', 'Value', 'Processing time', 'Parameters']


    def test_reports(self):

        def test_report(report):

            for field in self.report_fields: self.assertTrue(field in report)

            for result in report['Results']:

                for i in self.result_fields: self.assertTrue(i in result,msg="{0}".format(i))

                # these three are required for all js
                self.assertTrue(isinstance(result['Plan'],Groundplan))
                self.assertTrue(isinstance(result['Value'],float) or result['Value']==0, msg="{0}".format(result["Value"]))
                self.assertTrue(isinstance(result['Processing time'], float))

                # the j also has a field for algorithm-specific parameters
                self.assertTrue(type(result['Parameters']) is types.DictType)

                # program must have taken some time
                self.assertTrue(result['Processing time'] > 0)

                # the listed value must equal the plan value, or the plan is invalid and zero is given as value.
                self.assertTrue(
                    # jed plans are either valid and with a positive getPlanValue() equal to the jed value
                    (result['Plan'].isValid() and result['Plan'].getPlanValue() == result['Value']  and result['Value'] > 0)
                    # or the plan is invalid with 0 jed as value
                    or (not result['Plan'].isValid() and result['Value'] == 0)
                )

        """Is the report structured as expected?"""

        bases = [Groundplan, base_a, base_b, base_c, base_dynamic]
        tight_algos = [TightFitWB, TightFit_A, TightFit_B]

        r0 = perform_all_experiments(self.problem_instances_nh,self.problem_instances_pg, bases,
                                     {
                                         "Zoom":{
                                             "algorithms":tight_algos,
                                             "constants":
                                                 {
                                                     'min':1.0,
                                                     'max':2.0,
                                                     'interval':1,
                                                    'interval_shrink_factor': 0.75,
                                                     'min_interval':0.9
                                                 }
                                         },
                                         "HillClimberRandom":{
                                             "constants":{
                                                 "max_iterations":2
                                             }
                                         },
                                         #
                                         #"SimulatedAnnealing_1":{
                                         #    "algorithms":[TightFitWB],
                                         #    "constants":{
                                         #        "neigbor_functions" : [neighbor_tight, neighbor_random],
                                         #        "init_state_functions": []
                                         #    }
                                         #},
                                         "SimulatedAnnealing_2":{
                                             "algorithms":tight_algos,
                                             "constants":{
                                                 "max_iterations": 2,
                                                 'min': 1,
                                                 'max': 2
                                             }
                                         }
                                     }
                                     )

        # the top report object must be a nested dict with problem instance values as keys

        # the top level must have problem_instances_nh as keys
        self.assertTrue(type(r0) is types.DictType)
        self.assertTrue(len(r0)==len(self.problem_instances_nh))
        for r1 in r0:
            l1 = r0[r1]
            # the second level must have problem_instances_pg as keys

            self.assertTrue(type(l1) is types.DictType, msg='{0}'.format(type(l1)))
            self.assertTrue(len(l1)==len(self.problem_instances_pg))

            for r2 in l1:
                l2 = l1[r2]
                # each report must be a dict having experiment_keys as keys
                self.assertTrue(type(l2) is types.DictType)
                self.assertTrue(len(l2)==len(self.experiment_keys))

                for r3 in l2:
                    report = l2[r3]
                    # each sub-report must be a dict having report_fields as keys
                    self.assertTrue(type(report) is types.DictType)
                    self.assertTrue(len(report)==len(self.report_fields))
                    test_report(report)


if __name__ == '__main__':
    unittest.main()