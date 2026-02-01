import pulp
def solve_job_sequencing(jobs, deadlines, profits):
    n = len(jobs)
    max_deadline = max(deadlines)

    model = pulp.LpProblem("JobSequencing", pulp.LpMaximize)

    x = {
        (i, t): pulp.LpVariable(f"x_{i}_{t}", cat="Binary")
        for i in range(n)
        for t in range(1, max_deadline + 1)
    }

    model += pulp.lpSum(profits[i] * x[i, t]
                        for i in range(n)
                        for t in range(1, deadlines[i] + 1))

    for i in range(n):
        model += pulp.lpSum(x[i, t] for t in range(1, deadlines[i] + 1)) <= 1

    for t in range(1, max_deadline + 1):
        model += pulp.lpSum(x[i, t]
                            for i in range(n)
                            if t <= deadlines[i]) <= 1

    model.solve(pulp.PULP_CBC_CMD(msg=0))

    selected = []
    total_profit = 0
    for i in range(n):
        for t in range(1, deadlines[i] + 1):
            if pulp.value(x[i, t]) == 1:
                selected.append(jobs[i])
                total_profit += profits[i]

    return selected, total_profit