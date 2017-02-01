from algos.TightFitWB import TightFitWB
from algos.TightFit_A import TightFit_A
from algos.TightFit_B import TightFit_B
from bases.base_a import base_a
from bases.base_b import base_b
from bases.base_c import base_c
from bases.base_dynamic import base_dynamic
from src.Groundplan import Groundplan

tight_fit_algos = [TightFitWB, TightFit_A, TightFit_B]

bases = [Groundplan, #base_a, base_b, base_c,
         #base_dynamic
         base_b
         ]

zoom = {
    "variables": {
        "Bases": bases,
        "Tight Fit functions": tight_fit_algos
    },
    "constants": {
        'min': 1.0,
        'max': 2.0,
        'interval': 1.0,
        'interval_shrink_factor': 0.1,
        'min_interval': 0.5
    }
}

hc = {
    "variables": {
        "Bases": bases,
        "Number of candidate moves": [2]
    },
    "constants": {
        "max_iterations": 10
    }
}

sa_2 = {
    "variables": {
        "Bases": bases,
        "Tight Fit functions": tight_fit_algos
    },
    "constants": {
        "max_iterations": 10,
        'min': 1.0,
        'max': 8.0
    }
}

test_config = {
    "Problem instances": {

        # as defined by course manual

        "Number of residences": [i*10+10 for i in range(10)],
        "Enable playgrounds": [True, False],
        "Area dimensions": [{"width": 200.0, "height": 170.0}],
        "Building proportions": [{"Mansion": 0.2, "Bungalow": 0.3, "FamilyHome": 0.5}]
    },
    "Experiments": {
        "Zoom":zoom,
        "HillClimberRandom":hc,
        "SimulatedAnnealing_2": sa_2
    }
}
