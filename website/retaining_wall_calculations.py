from math import sin, radians

def dry_horizontal_back_retaining_wall_calculate(problem):
    # unpack the variables
    gs = problem['gs']
    gb = problem['gb']
    phi = problem['phi']
    bc = problem['bc']
    bb = problem['bb']
    bh = problem['bh']
    p = problem['p']
    H = problem['H']
    B = problem['B']

    # Weights
    w1 = gs*bb*bh
    w2 = gs*B*(H - bh)
    w3 = gs*(bb - B - 2*p)*(H-bh)/2
    w4 = gb*(bb - B - 2*p)*(H-bh)/2
    w5 = gb*p*(H - bh)
    sumw =  w1 + w2 + w3 + w4 + w5
    
    # Lever arms
    x1 = bb/2
    x2 = p + B/2
    x3 = p + B + (bb-2*p-B)/3
    x4 = p + B + 2*(bb - 2*p - B)/3
    x5 = bb - p/2

    # Stability conditions
    ka = (1-sin(radians(phi)))/(1+sin(radians(phi)))
    pa = 1/2*gb*ka*H**2
    y = H/3

    # Overturning
    stabilizing_moment = w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5
    overTurning_moment = pa*y
    factor_of_safety_overturning = stabilizing_moment/overTurning_moment

    overturning_results = {'stabilizing_moment': stabilizing_moment, 
    'overTurning_moment': overTurning_moment, 
    'factor_of_safety_overturning': factor_of_safety_overturning}

    # Sliding
    frictional_resistance = sin(radians(phi))*sumw
    sliding_force = pa
    factor_of_safety_sliding = frictional_resistance/sliding_force

    sliding_results = {'frictional_resistance': frictional_resistance, 
    'sliding_force': sliding_force, 
    'factor_of_safety_sliding': factor_of_safety_sliding}

    # Tension check at the heel
    a = (stabilizing_moment - overTurning_moment)/sumw
    # Bearing capacity check
    bearing_pressure_at_the_toe = (4*bb - 6*a)*sumw/(bb**2)
    factor_of_safety_bearing_capacity = bc/bearing_pressure_at_the_toe
    
    bearing_capacity_results = {'a':a, 
    'bearing_pressure_at_the_toe': bearing_pressure_at_the_toe, 
    'factor_of_safety_bearing_capacity': factor_of_safety_bearing_capacity}

    results = {'overturning_results': overturning_results, 
    'sliding_results': sliding_results, 
    'bearing_capacity_results': bearing_capacity_results}

    return results
