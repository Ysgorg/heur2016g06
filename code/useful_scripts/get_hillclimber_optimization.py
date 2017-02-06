def get_hillclimber_optimization(plan):
    # pass the plan to hillclimber,
    # return hillclimber output plan
    from residence_placers.HillClimber import HillClimber
    return HillClimber(plan,{'max_iterations':100})
    pass