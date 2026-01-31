from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class HomeScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Removed the branding badge as requested

        title = QLabel("Integer Programming\nSolver")
        title.setStyleSheet("font-size:42px; font-weight:800; color: #1e293b; line-height: 1.2;")
        title.setAlignment(Qt.AlignCenter)

        # Specialized Information Text for your Mini Project
        info_text = (
            "This mini-project explores Integer Programming (IP) models to solve "
            "discrete optimization problems. Unlike linear programming, IP requires "
            "some or all variables to be integers, making it essential for real-world "
            "scenarios like resource allocation, scheduling, and selection tasks "
            "where 'half-measures' are not an option."
        )

        subtitle = QLabel(info_text)
        subtitle.setStyleSheet("color:#475569; font-size:16px; line-height: 1.6;")
        subtitle.setWordWrap(True)
        subtitle.setFixedWidth(650)
        subtitle.setAlignment(Qt.AlignCenter)

        btn = QPushButton("Explore Applications →")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(220)
        btn.setFixedHeight(45)
        btn.clicked.connect(lambda: stack.setCurrentWidget(stack.apps))

        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(subtitle, 0, Qt.AlignCenter)
        layout.addSpacing(40)
        layout.addWidget(btn, 0, Qt.AlignCenter)
        layout.addStretch()