import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from styles import APP_STYLE

from ui.home import HomeScreen
from ui.applications import ApplicationsScreen
from ui.knapsack_ui import KnapsackUI
from ui.job_sequencing_ui import JobSequencingUI


class OptiSolver(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimization Software – Integer Programming")
        self.setGeometry(100, 100, 1100, 700)

        self.setStyleSheet(APP_STYLE)

        self.home = HomeScreen(self)
        self.apps = ApplicationsScreen(self)
        self.knapsack = KnapsackUI(self)
        self.job_seq = JobSequencingUI(self)

        self.addWidget(self.home)
        self.addWidget(self.apps)
        self.addWidget(self.knapsack)
        self.addWidget(self.job_seq)

        self.setCurrentWidget(self.home)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptiSolver()
    window.show()
    sys.exit(app.exec_())