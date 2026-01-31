from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFrame, QComboBox, QScrollArea, QListView
)
from PyQt5.QtCore import Qt
from solvers.general_solver import solve_general_lp

# STYLESHEET: Forces visibility and adds borders
MODERN_STYLE = """
    QLineEdit, QComboBox {
        border: 2px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
        background-color: #ffffff;
        color: #000000;
        font-size: 14px;
        min-height: 48px;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 2px solid #2563eb;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #000000;
        selection-background-color: #2563eb;
        selection-color: #ffffff;
        outline: none;
    }
"""


class GeneralSolverUI(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.constraints = []

        # Main Layout (Matching ApplicationsScreen margins)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # HEADER: Title Left, Back Button Right (Same as your other apps)
        header = QHBoxLayout()
        title = QLabel("General Linear Programming")
        title.setStyleSheet("font-size:28px; font-weight:700;")

        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedWidth(100)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.stack.apps))

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.back_btn)
        self.main_layout.addLayout(header)
        self.main_layout.addSpacing(30)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: transparent;")

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(20)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

        # Sections
        self.container_layout.addWidget(QLabel("<b>Objective Function</b>"))
        self.setup_objective()

        self.container_layout.addWidget(QLabel("<b>Constraints</b>"))
        self.constraints_wrapper = QVBoxLayout()
        self.container_layout.addLayout(self.constraints_wrapper)

        add_btn = QPushButton("➕ Add Constraint")
        add_btn.setFixedWidth(160)
        add_btn.clicked.connect(self.add_constraint)
        self.container_layout.addWidget(add_btn)

        solve_btn = QPushButton("Run Solver")
        solve_btn.setFixedHeight(50)
        solve_btn.setCursor(Qt.PointingHandCursor)
        solve_btn.setStyleSheet("background: #2563eb; color: white; font-weight: bold; border-radius: 8px;")
        solve_btn.clicked.connect(self.solve_logic)
        self.container_layout.addWidget(solve_btn)

        self.output = QLabel("Enter values and click calculate.")
        self.output.setStyleSheet("padding: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 10px;")
        self.container_layout.addWidget(self.output)

        self.add_constraint()

    def setup_objective(self):
        row = QHBoxLayout()
        self.obj_type = QComboBox()
        self.obj_type.addItems(["Maximize", "Minimize"])
        self.obj_type.setStyleSheet(MODERN_STYLE)

        # FIX: Use a dedicated QListView to prevent the "deleted" error
        self.obj_type.setView(QListView())
        self.obj_type.setFixedWidth(130)

        self.obj_inputs = [QLineEdit(), QLineEdit()]
        for inp in self.obj_inputs:
            inp.setStyleSheet(MODERN_STYLE)
            inp.setFixedWidth(70)

        row.addWidget(self.obj_type)
        row.addWidget(self.obj_inputs[0]);
        row.addWidget(QLabel("x +"))
        row.addWidget(self.obj_inputs[1]);
        row.addWidget(QLabel("y"))
        row.addStretch()
        self.container_layout.addLayout(row)

    def add_constraint(self):
        row_data = {}
        frame = QFrame()
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(0, 0, 0, 0)

        x_in = QLineEdit();
        y_in = QLineEdit()
        for i in [x_in, y_in]:
            i.setStyleSheet(MODERN_STYLE);
            i.setFixedWidth(70)

        op = QComboBox()
        op.addItems(["≤", "≥", "=", "<", ">"])
        op.setStyleSheet(MODERN_STYLE)
        op.setView(QListView())  # FIX applied here as well
        op.setFixedWidth(80)

        rhs = QLineEdit()
        rhs.setStyleSheet(MODERN_STYLE);
        rhs.setFixedWidth(80)

        del_btn = QPushButton("Delete")
        del_btn.setFixedWidth(80)
        del_btn.setFixedHeight(48)
        del_btn.setStyleSheet("background-color: #ef4444; color: white; border-radius: 6px; font-weight: bold;")
        del_btn.clicked.connect(lambda: self.remove_row(row_data, frame))

        lay.addWidget(x_in);
        lay.addWidget(QLabel("x +"))
        lay.addWidget(y_in);
        lay.addWidget(QLabel("y"))
        lay.addWidget(op)
        lay.addWidget(rhs)
        lay.addWidget(del_btn)

        self.constraints_wrapper.addWidget(frame)
        row_data.update({"x": x_in, "y": y_in, "op": op, "rhs": rhs})
        self.constraints.append(row_data)

    def remove_row(self, data, widget):
        if len(self.constraints) > 1:
            self.constraints.remove(data)
            widget.deleteLater()

    def solve_logic(self):
        try:
            objective = [float(i.text() or 0) for i in self.obj_inputs]
            c_data = []
            for r in self.constraints:
                c_data.append(([float(r['x'].text() or 0), float(r['y'].text() or 0)],
                               r['op'].currentText(),
                               float(r['rhs'].text() or 0)))

            sol, res = solve_general_lp(2, objective, c_data, self.obj_type.currentText() == "Maximize")
            if sol:
                self.output.setText(f"Optimal Solution: {sol}\nZ = {res}")
            else:
                self.output.setText(f"Result: {res}")
        except Exception as e:
            QMessageBox.warning(self, "Input Error", str(e))