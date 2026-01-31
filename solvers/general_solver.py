import pulp


def solve_general_lp(num_vars, objective, constraints, maximize=True):
    sense = pulp.LpMaximize if maximize else pulp.LpMinimize
    prob = pulp.LpProblem("General_Solver", sense)

    # Decision variables defined as Integers
    varnames = ['x', 'y']
    variables = {varnames[i]: pulp.LpVariable(varnames[i], lowBound=0, cat='Integer')
                 for i in range(num_vars)}

    # Objective
    prob += pulp.lpSum([objective[i] * variables[varnames[i]] for i in range(num_vars)])

    # Handle Operators
    for coeffs, op, rhs in constraints:
        lhs = pulp.lpSum([coeffs[i] * variables[varnames[i]] for i in range(num_vars)])
        if op == "≤" or op == "<":
            prob += (lhs <= rhs)
        elif op == "≥" or op == ">":
            prob += (lhs >= rhs)
        elif op == "=":
            prob += (lhs == rhs)

    # Solver
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[prob.status] == 'Optimal':
        return {v.name: v.varValue for v in prob.variables()}, pulp.value(prob.objective)
    return None, "No feasible integer solution found."