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
