from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt


class ApplicationsScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        # ================= HEADER =================
        header = QHBoxLayout()

        title = QLabel("Applications")
        title.setStyleSheet("font-size:28px;font-weight:700;")

        back_btn = QPushButton("← Back to Home")
        back_btn.setFixedWidth(160)
        back_btn.clicked.connect(lambda: stack.setCurrentWidget(stack.home))

        header.addWidget(title)
        header.addStretch()
        header.addWidget(back_btn)

        layout.addLayout(header)
        layout.addSpacing(40)

        # ================= CARDS =================
        cards = QHBoxLayout()
        cards.setSpacing(30)

        # ---- General Equation Solver (FIRST) ----
        cards.addWidget(self.card(
            "General Equation Solver",
            "Solve linear equations with\n2 or 3 decision variables",
            lambda: stack.setCurrentWidget(stack.general_solver)
        ))

        # ---- Knapsack ----
        cards.addWidget(self.card(
            "0/1 Knapsack Problem",
            "Binary decision variables\nMaximize profit under capacity",
            lambda: stack.setCurrentWidget(stack.knapsack)
        ))

        # ---- Job Sequencing ----
        cards.addWidget(self.card(
            "Job Sequencing Problem",
            "Schedule jobs with deadlines\nMaximize total profit",
            lambda: stack.setCurrentWidget(stack.job_seq)
        ))

        layout.addLayout(cards)
        layout.addStretch()

    # ================= CARD TEMPLATE =================
    def card(self, title, desc, action):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setMinimumWidth(330)   # wider cards
        card.setMaximumWidth(360)

        v = QVBoxLayout(card)
        v.setContentsMargins(25, 25, 25, 25)
        v.setSpacing(15)

        t = QLabel(title)
        t.setWordWrap(True)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("font-size:17px;font-weight:700;")

        d = QLabel(desc)
        d.setWordWrap(True)
        d.setAlignment(Qt.AlignCenter)
        d.setStyleSheet("color:#475569;font-size:14px;")

        btn = QPushButton("Open Solver →")
        btn.setFixedHeight(40)
        btn.clicked.connect(action)

        v.addWidget(t)
        v.addWidget(d)
        v.addStretch()
        v.addWidget(btn)

        return card