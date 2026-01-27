from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class HomeScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        badge = QLabel("Integer Programming Toolkit v1.0")
        badge.setStyleSheet(
            "background:#e0e7ff;padding:6px 16px;border-radius:16px;"
            "color:#1e3a8a;font-weight:600;"
        )

        title = QLabel("Optimization\nSoftware.")
        title.setStyleSheet("font-size:46px;font-weight:800;")

        subtitle = QLabel(
            "Interactive visualization and solvers for\n"
            "combinatorial optimization problems."
        )
        subtitle.setStyleSheet("color:#475569;font-size:16px;")
        subtitle.setAlignment(Qt.AlignCenter)

        btn = QPushButton("Explore Applications →")
        btn.clicked.connect(lambda: stack.setCurrentWidget(stack.apps))

        layout.addWidget(badge)
        layout.addSpacing(20)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(btn)