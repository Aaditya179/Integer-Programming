from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame


class ApplicationsScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)

        title = QLabel("Applications")
        title.setStyleSheet("font-size:28px;font-weight:700;")

        cards = QHBoxLayout()

        cards.addWidget(self.card(
            "0/1 Knapsack Problem",
            "Binary decision variables\nMaximize profit under capacity",
            lambda: stack.setCurrentWidget(stack.knapsack)
        ))

        cards.addWidget(self.card(
            "Job Sequencing Problem",
            "Schedule jobs with deadlines\nMaximize total profit",
            lambda: stack.setCurrentWidget(stack.job_seq)
        ))

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addLayout(cards)

    def card(self, title, desc, action):
        card = QFrame()
        v = QVBoxLayout(card)

        t = QLabel(title)
        t.setStyleSheet("font-size:18px;font-weight:700;")

        d = QLabel(desc)
        d.setStyleSheet("color:#475569;")

        btn = QPushButton("Open Solver →")
        btn.clicked.connect(action)

        v.addWidget(t)
        v.addWidget(d)
        v.addStretch()
        v.addWidget(btn)
        return card