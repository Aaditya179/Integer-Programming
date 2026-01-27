import pulp


def solve_knapsack(weights, profits, capacity):
    n = len(weights)

    model = pulp.LpProblem("Knapsack", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(n)]

    model += pulp.lpSum(profits[i] * x[i] for i in range(n))
    model += pulp.lpSum(weights[i] * x[i] for i in range(n)) <= capacity

    model.solve(pulp.PULP_CBC_CMD(msg=0))

    selection = [int(pulp.value(x[i])) for i in range(n)]
    max_profit = int(pulp.value(model.objective))

    return selection, max_profit