from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMessageBox
)
from solvers.knapsack_solver import solve_knapsack


class KnapsackUI(QWidget):
    """
    UI for 0/1 Knapsack Problem
    Uses Integer Programming (PuLP) with binary variables
    """

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)

        title = QLabel("0/1 Knapsack Problem")
        title.setStyleSheet("font-size:28px;font-weight:700;")

        self.weights_input = QLineEdit()
        self.profits_input = QLineEdit()
        self.capacity_input = QLineEdit()

        solve_btn = QPushButton("Solve Knapsack")
        solve_btn.clicked.connect(self.solve)

        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: stack.setCurrentWidget(stack.apps))

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size:16px;font-weight:600;")
        self.result_label.setWordWrap(True)

        layout.addWidget(back_btn)
        layout.addWidget(title)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Weights (comma separated)"))
        layout.addWidget(self.weights_input)

        layout.addWidget(QLabel("Profits (comma separated)"))
        layout.addWidget(self.profits_input)

        layout.addWidget(QLabel("Knapsack Capacity"))
        layout.addWidget(self.capacity_input)

        layout.addSpacing(20)
        layout.addWidget(solve_btn)
        layout.addSpacing(20)
        layout.addWidget(self.result_label)

    def solve(self):
        try:
            weights = list(map(int, self.weights_input.text().split(",")))
            profits = list(map(int, self.profits_input.text().split(",")))
            capacity = int(self.capacity_input.text())

            if len(weights) != len(profits):
                raise ValueError

            selection, max_profit = solve_knapsack(
                weights, profits, capacity
            )

            self.result_label.setText(
                f"Maximum Profit: {max_profit}\n"
                f"Selection Vector (0/1): {selection}"
            )

        except Exception:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid numeric inputs.\n"
                "Example:\nWeights: 2,3,4\nProfits: 3,4,5\nCapacity: 6"
            )