from bases.base_a import base_a
from bases.base_b import base_b
from bases.base_dynamic import base_dynamic
from residence_placers.TightFitWB import TightFitWB
from residence_placers.TightFit_A import TightFit_A
from residence_placers.TightFit_B import TightFit_B

tight_fit_algos = [#TightFitWB,
                   TightFit_A, TightFit_B]

bases = [base_a, base_b, base_dynamic]

MAX_ITERATIONS = 100

zoom = {
    "variables": {
        "Bases": bases,
        "Tight Fit functions": tight_fit_algos
    },
    "constants": {
        'min': 1.0,
        'max': 10.0,
        'interval': 3.0,
        'interval_shrink_factor': 0.1,
        'min_interval': 2.0
    }
}

hc = {
    "variables": {
        "Bases": bases,
        "Number of candidate moves": [2,3#,6
                                      ]
    },
    "constants": {
        "max_iterations": MAX_ITERATIONS
    }
}

sa_2 = {
    "variables": {
        "Bases": bases,
        "Tight Fit functions": tight_fit_algos
    },
    "constants": {
        "max_iterations": MAX_ITERATIONS,
        'min': 1.0,
        'max': 2.0
    }
}

test_config = {
    "Problem instances": {

        # as defined by course manual

        "Number of residences": [40, 70 , 100],  # ,70,100],#[i*10+10 for i in range(10)],
        "Enable playgrounds": [True  # , False
                               ],
        "Area dimensions": [{"width": 200.0, "height": 170.0}],
        "Building proportions": [{"Mansion": 0.2, "Bungalow": 0.3, "FamilyHome": 0.5}]
    },
    "Experiments": {
        "Zoom": zoom,
        "HC": hc,
        "SA": sa_2
    }
}
