import collections

class Tableau:
    """Helper class to store a single step of the Simplex method."""
    def __init__(self, matrix, basis, obj_val, row_labels, col_labels, pivot_row=None, pivot_col=None):
        # matrix is 2D list: constraints + objective row
        self.matrix = [row[:] for row in matrix]
        self.basis = basis[:]
        self.obj_val = obj_val
        self.row_labels = row_labels[:]
        self.col_labels = col_labels[:]
        self.pivot_row = pivot_row
        self.pivot_col = pivot_col

    def __str__(self):
        # For debugging purposes
        return f"Basis: {self.basis}\nMatrix: {self.matrix}"

class SimplexSolver:
    """
    Implements the Simplex method for Linear Programming.
    
    The Simplex method is an iterative procedure for finding the optimal solution 
    to a linear programming problem. This implementation handles standard 
    maximization and minimization problems by converting them to a standard form 
    with slack variables.
    """
    def __init__(self, num_vars, num_constraints, obj_coeffs, constraint_coeffs, rhs_values, is_maximization=True):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.is_maximization = is_maximization
        
        # Original objective coefficients
        self.original_obj_coeffs = obj_coeffs[:]
        
        # Adjust for maximization/minimization
        # Simplex standard is maximization. For minimization, we maximize -Z.
        if is_maximization:
            self.obj_coeffs = [-c for c in obj_coeffs]
        else:
            # For minimization: min Z = sum(c_i * x_i) is max -Z = sum(-c_i * x_i)
            # Standard simplex maximizes Z. We set Z = -Z_original.
            # Bottom row: Z - sum(-c_i * x_i) = 0 => Z + sum(c_i * x_i) = 0
            self.obj_coeffs = [c for c in obj_coeffs]
            
        self.constraint_coeffs = [row[:] for row in constraint_coeffs]
        self.rhs_values = rhs_values[:]
        
        self.history = [] # List of Tableau objects
        self.solution = None
        self.optimal_val = None
        self.status = "Incomplete" # Incomplete, Optimal, Unbounded, Infeasible

    def solve(self):
        # 1. Create initial tableau
        # Standard form: maximize Z = c1*x1 + ... + cn*xn subject to Ai*x <= bi
        # Tableau matrix: [A | I | b]
        # Bottom row: [c | 0 | 0]
        
        matrix = []
        for i in range(self.num_constraints):
            row = self.constraint_coeffs[i] + [0] * self.num_constraints + [self.rhs_values[i]]
            row[self.num_vars + i] = 1 # Slack variable
            matrix.append(row)
            
        # Objective row (Z)
        obj_row = self.obj_coeffs + [0] * self.num_constraints + [0]
        matrix.append(obj_row)
        
        col_labels = [f"x{i+1}" for i in range(self.num_vars)] + \
                     [f"s{i+1}" for i in range(self.num_constraints)] + ["RHS"]
        row_labels = [f"s{i+1}" for i in range(self.num_constraints)] + ["Z"]
        basis = [f"s{i+1}" for i in range(self.num_constraints)]
        
        while True:
            # 2. Check for optimality
            # In a maximization problem, if all coefficients in the objective row 
            # are non-negative, the current solution is optimal.
            obj_row = matrix[-1]
            min_val = min(obj_row[:-1])
            
            if min_val >= -1e-9: # Optimal reached (using epsilon for float precision)
                self.status = "Optimal"
                self.save_tableau(matrix, basis, -matrix[-1][-1], row_labels, col_labels)
                break
                
            pivot_col = obj_row.index(min_val)
            
            # Minimum ratio test
            min_ratio = float('inf')
            pivot_row = -1
            for i in range(self.num_constraints):
                val = matrix[i][pivot_col]
                if val > 1e-9:
                    ratio = matrix[i][-1] / val
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i
                        
            if pivot_row == -1:
                self.status = "Unbounded"
                self.save_tableau(matrix, basis, -matrix[-1][-1], row_labels, col_labels, pivot_col=pivot_col)
                return False
                
            self.save_tableau(matrix, basis, -matrix[-1][-1], row_labels, col_labels, pivot_row, pivot_col)
            
            # Pivot operation
            pivot_val = matrix[pivot_row][pivot_col]
            # Normalize pivot row
            matrix[pivot_row] = [x / pivot_val for x in matrix[pivot_row]]
            
            for i in range(len(matrix)):
                if i != pivot_row:
                    factor = matrix[i][pivot_col]
                    matrix[i] = [matrix[i][j] - factor * matrix[pivot_row][j] for j in range(len(matrix[0]))]
            
            # Update basis
            basis[pivot_row] = col_labels[pivot_col]
            row_labels[pivot_row] = col_labels[pivot_col]
            
        # Extract solution
        self.solution = [0.0] * self.num_vars
        for i in range(self.num_vars):
            label = f"x{i+1}"
            if label in basis:
                idx = basis.index(label)
                self.solution[i] = matrix[idx][-1]
        
        self.optimal_val = matrix[-1][-1]
        if not self.is_maximization:
            # If we were minimizing, we maximized -Z. So Z = -optimal_val.
            self.optimal_val = -self.optimal_val
            
        return True

    def save_tableau(self, matrix, basis, obj_val, row_labels, col_labels, pivot_row=None, pivot_col=None):
        self.history.append(Tableau(matrix, basis, obj_val, row_labels, col_labels, pivot_row, pivot_col))

class IntegerSolver:
    """
    Implements the Branch and Bound algorithm for Integer Programming.
    
    Branch and Bound works by first solving the LP relaxation (no integer constraints). 
    If the solution isn't integer, it 'branches' by creating two sub-problems 
    with new constraints (x <= floor(v) and x >= ceil(v)) and continues recursively.
    """
    def __init__(self, num_vars, num_constraints, obj_coeffs, constraint_coeffs, rhs_values, is_maximization=True):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.obj_coeffs = obj_coeffs
        self.constraint_coeffs = constraint_coeffs
        self.rhs_values = rhs_values
        self.is_maximization = is_maximization
        
        self.best_solution = None
        self.best_val = float('-inf') if is_maximization else float('inf')
        self.history_of_solvers = [] # To store all simplex runs if needed

    def solve(self):
        self._branch_and_bound(self.constraint_coeffs, self.rhs_values)
        return self.best_solution, self.best_val

    def _branch_and_bound(self, current_constraints, current_rhs):
        solver = SimplexSolver(self.num_vars, len(current_constraints), self.obj_coeffs, current_constraints, current_rhs, self.is_maximization)
        self.history_of_solvers.append(solver)
        
        if not solver.solve():
            return # Infeasible or unbounded
            
        val = solver.optimal_val
        sol = solver.solution
        
        # Bounding
        if self.is_maximization:
            if val <= self.best_val:
                return
        else:
            if val >= self.best_val:
                return
                
        # Check for integer solution
        branch_idx = -1
        for i in range(len(sol)):
            if abs(sol[i] - round(sol[i])) > 1e-4:
                branch_idx = i
                break
                
        if branch_idx == -1: # Integer solution found
            self.best_val = val
            self.best_solution = [round(x) for x in sol]
            return
            
        # Branching
        # constraint: x_i <= floor(sol[i])
        new_row1 = [0] * self.num_vars
        new_row1[branch_idx] = 1
        constraints1 = current_constraints + [new_row1]
        rhs1 = current_rhs + [int(sol[branch_idx])]
        self._branch_and_bound(constraints1, rhs1)
        
        # constraint: x_i >= ceil(sol[i])  =>  -x_i <= -ceil(sol[i])
        new_row2 = [0] * self.num_vars
        new_row2[branch_idx] = -1
        constraints2 = current_constraints + [new_row2]
        rhs2 = current_rhs + [-int(sol[branch_idx]) - 1]
        self._branch_and_bound(constraints2, rhs2)

class KnapsackSolver:
    """
    Implements solvers for the Knapsack problem:
    1. Greedy: Optimal for Fractional Knapsack (can take parts of items).
    2. Dynamic Programming: Optimal for 0/1 Knapsack (must take whole items).
    """
    @staticmethod
    def solve_greedy(items, capacity):
        # items: list of (value, weight, id)
        # Sort by value/weight ratio
        sorted_items = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
        total_value = 0
        current_weight = 0
        selected = [] # (id, fraction)
        
        for v, w, i in sorted_items:
            if current_weight + w <= capacity:
                current_weight += w
                total_value += v
                selected.append((i, 1.0))
            else:
                remaining = capacity - current_weight
                fraction = remaining / w
                total_value += v * fraction
                selected.append((i, fraction))
                break
        return total_value, selected

    @staticmethod
    def solve_dp(items, capacity):
        # items: list of (value, weight, id)
        n = len(items)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            v, w, _ = items[i-1]
            w_int = int(w)
            for j in range(capacity + 1):
                if w_int <= j:
                    dp[i][j] = max(dp[i-1][j], dp[i-1][j-w_int] + v)
                else:
                    dp[i][j] = dp[i-1][j]
                    
        # Backtrack to find items
        res = dp[n][capacity]
        selected = []
        w_curr = capacity
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == dp[i-1][w_curr]:
                continue
            else:
                selected.append(items[i-1][2]) # Store ID
                v_item, w_item, _ = items[i-1]
                res -= v_item
                w_curr -= int(w_item)
                
        return dp[n][capacity], selected

class JobSequencingSolver:
    """
    Implements the Greedy algorithm for Job Sequencing with Deadlines.
    
    Jobs are sorted by profit descending, and each job is assigned to the 
    latest possible available slot before its deadline.
    """
    @staticmethod
    def solve(jobs):
        # jobs: list of (id, profit, deadline)
        # Sort jobs by profit in descending order
        n = len(jobs)
        jobs.sort(key=lambda x: x[1], reverse=True)
        
        max_deadline = max(job[2] for job in jobs)
        result = [None] * max_deadline
        total_profit = 0
        sequence = []
        
        for i in range(n):
            # Find a free slot for this job (from its deadline backwards)
            for j in range(min(max_deadline, jobs[i][2]) - 1, -1, -1):
                if result[j] is None:
                    result[j] = jobs[i][0]
                    total_profit += jobs[i][1]
                    break
                    
        sequence = [job_id for job_id in result if job_id is not None]
        return total_profit, sequence
