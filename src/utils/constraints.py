"""
Constraint handling utilities for the medical supply scheduling problem.
Implements all constraints (18)–(30) as described in the problem statement.
"""

def constraint_18(ajk, xijk, xjjk, bjk, m, K1):
    # Open military medical service must reserve minimum amount bjk of each type of supply
    for j in range(m):
        for k in range(K1):
            total = ajk[j][k] - sum(xijk[i][j][k] for i in range(m)) - sum(xjjk[j][jp][k] for jp in range(m, 2*m))
            if total < bjk[j][k]:
                return False
    return True

def constraint_19(ajk, xijk, xjjk, bjk, m, K1):
    # Closed military medical service must reserve minimum amount bjk of each type of supply
    for j in range(m, 2*m):
        for k in range(K1):
            total = ajk[j][k] - sum(xijk[i][j][k] for i in range(m)) - sum(xjjk[j][jp][k] for jp in range(m))
            if total < bjk[j][k]:
                return False
    return True

def constraint_20(ajk, yo, ys, ym, yv, ro, rs, rm, rv, bjk, m, K1, K):
    # For fixed supplies at open military services
    for j in range(m):
        for k in range(K1, K):
            total = ajk[j][k] - (
                sum(yo[i][j] * ro[k] for i in range(m)) +
                sum(ys[i][j] * rs[k] for i in range(m)) +
                sum(ym[i][j] * rm[k] for i in range(m)) +
                sum(yv[i][j] * rv[k] for i in range(m))
            )
            if total < bjk[j][k]:
                return False
    return True

def constraint_21(yo, no_j, m):
    # Residents received by open military service
    for j in range(m):
        if sum(yo[i][j] for i in range(m)) > no_j[j]:
            return False
    return True

def constraint_22(ys, ns_j, m):
    for j in range(m):
        if sum(ys[i][j] for i in range(m)) > ns_j[j]:
            return False
    return True

def constraint_23(ym, nm_j, m):
    for j in range(m):
        if sum(ym[i][j] for i in range(m)) > nm_j[j]:
            return False
    return True

def constraint_24(yv, nv_j, m):
    for j in range(m):
        if sum(yv[i][j] for i in range(m)) > nv_j[j]:
            return False
    return True

def constraint_25(yo, no_i, m):
    for i in range(m):
        if sum(yo[i][j] for j in range(m)) > no_i[i]:
            return False
    return True

def constraint_26(ys, ns_i, m):
    for i in range(m):
        if sum(ys[i][j] for j in range(m)) > ns_i[i]:
            return False
    return True

def constraint_27(ym, nm_i, m):
    for i in range(m):
        if sum(ym[i][j] for j in range(m)) > nm_i[i]:
            return False
    return True

def constraint_28(yv, nv_i, m):
    for i in range(m):
        if sum(yv[i][j] for j in range(m)) > nv_i[i]:
            return False
    return True

def constraint_29(satisfaction_rate, S):
    return satisfaction_rate >= S

def constraint_30(total_cost, C):
    return total_cost <= C

def validate_solution(solution, params):
    """
    Validate a solution against all constraints (18)-(30).
    'params' should be a dictionary containing all required arrays and values.
    """
    return all([
        constraint_18(params['ajk'], params['xijk'], params['xjjk'], params['bjk'], params['m'], params['K1']),
        constraint_19(params['ajk'], params['xijk'], params['xjjk'], params['bjk'], params['m'], params['K1']),
        constraint_20(params['ajk'], params['yo'], params['ys'], params['ym'], params['yv'],
                      params['ro'], params['rs'], params['rm'], params['rv'],
                      params['bjk'], params['m'], params['K1'], params['K']),
        constraint_21(params['yo'], params['no_j'], params['m']),
        constraint_22(params['ys'], params['ns_j'], params['m']),
        constraint_23(params['ym'], params['nm_j'], params['m']),
        constraint_24(params['yv'], params['nv_j'], params['m']),
        constraint_25(params['yo'], params['no_i'], params['m']),
        constraint_26(params['ys'], params['ns_i'], params['m']),
        constraint_27(params['ym'], params['nm_i'], params['m']),
        constraint_28(params['yv'], params['nv_i'], params['m']),
        constraint_29(params['satisfaction_rate'], params['S']),
        constraint_30(params['total_cost'], params['C']),
    ])

# Optionally, you can keep or update the repair_solution and adjust_solution stubs as needed for your algorithm.
def repair_solution(solution, constraints):
    for constraint in constraints:
        if not constraint(solution):
            solution = adjust_solution(solution, constraint)
    return solution

def adjust_solution(solution, constraint):
    # Implement logic to adjust the solution to satisfy the constraint
    # This is a placeholder for the actual adjustment logic
    return solution  # Modify this to return a valid solution