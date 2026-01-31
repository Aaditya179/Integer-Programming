from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMessageBox
)
from solvers.job_sequencing_solver import solve_job_sequencing


class JobSequencingUI(QWidget):
    """
    UI for Job Sequencing with Deadlines
    Solved using Integer Programming (not greedy)
    """

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)

        title = QLabel("Job Sequencing Problem")
        title.setStyleSheet("font-size:28px;font-weight:700;")

        self.jobs_input = QLineEdit()
        self.deadlines_input = QLineEdit()
        self.profits_input = QLineEdit()

        solve_btn = QPushButton("Solve Job Sequencing")
        solve_btn.clicked.connect(self.solve)

        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: stack.setCurrentWidget(stack.apps))

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size:16px;font-weight:600;")
        self.result_label.setWordWrap(True)

        layout.addWidget(back_btn)
        layout.addWidget(title)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Job IDs (comma separated)"))
        layout.addWidget(self.jobs_input)

        layout.addWidget(QLabel("Deadlines (comma separated)"))
        layout.addWidget(self.deadlines_input)

        layout.addWidget(QLabel("Profits (comma separated)"))
        layout.addWidget(self.profits_input)

        layout.addSpacing(20)
        layout.addWidget(solve_btn)
        layout.addSpacing(20)
        layout.addWidget(self.result_label)

    def solve(self):
        try:
            jobs = self.jobs_input.text().split(",")
            deadlines = list(map(int, self.deadlines_input.text().split(",")))
            profits = list(map(int, self.profits_input.text().split(",")))

            if not (len(jobs) == len(deadlines) == len(profits)):
                raise ValueError

            selected_jobs, total_profit = solve_job_sequencing(
                jobs, deadlines, profits
            )

            self.result_label.setText(
                f"Selected Jobs: {selected_jobs}\n"
                f"Total Profit: {total_profit}"
            )

        except Exception:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid inputs.\n"
                "Example:\nJobs: j1,j2,j3\nDeadlines: 2,1,3\nProfits: 50,10,40"
            )