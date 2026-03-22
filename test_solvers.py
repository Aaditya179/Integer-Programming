import solvers

def test_simplex():
    print("Testing Simplex...")
    # Maximize Z = 3x1 + 2x2
    # s.t. 
    # 2x1 + x2 <= 18
    # 2x1 + 3x2 <= 42
    # 3x1 + x2 <= 24
    obj = [3, 2]
    constraints = [[2, 1], [2, 3], [3, 1]]
    rhs = [18, 42, 24]
    solver = solvers.SimplexSolver(2, 3, obj, constraints, rhs, is_maximization=True)
    if solver.solve():
        print(f"LP Solution: {solver.solution}, Val: {solver.optimal_val}")
    else:
        print("LP Unbounded or Infeasible")

def test_integer_programming():
    print("\nTesting Integer Programming...")
    # Maximize Z = 5x1 + 4x2
    # s.t.
    # x1 + x2 <= 3.5
    # x1 >= 0, x2 >= 0
    obj = [5, 4]
    constraints = [[1, 1]]
    rhs = [3.5]
    solver = solvers.IntegerSolver(2, 1, obj, constraints, rhs, is_maximization=True)
    sol, val = solver.solve()
    print(f"IP Solution: {sol}, Val: {val}")

def test_knapsack():
    print("\nTesting Knapsack...")
    items = [(60, 10, 1), (100, 20, 2), (120, 30, 3)]
    capacity = 50
    g_val, g_items = solvers.KnapsackSolver.solve_greedy(items, capacity)
    dp_val, dp_items = solvers.KnapsackSolver.solve_dp(items, capacity)
    print(f"Greedy Val: {g_val}, Items: {g_items}")
    print(f"DP Val: {dp_val}, Items: {dp_items}")

def test_job_sequencing():
    print("\nTesting Job Sequencing...")
    jobs = [(1, 100, 2), (2, 19, 1), (3, 27, 2), (4, 25, 1), (5, 15, 3)]
    profit, sequence = solvers.JobSequencingSolver.solve(jobs)
    print(f"Profit: {profit}, Sequence: {sequence}")

if __name__ == "__main__":
    test_simplex()
    test_integer_programming()
    test_knapsack()
    test_job_sequencing()
