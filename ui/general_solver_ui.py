from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QRadioButton, QLineEdit, QMessageBox, QFrame, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt
from solvers.general_solver import solve_general_lp

# STYLESHEET: Forces visibility on dropdown lists and adds borders
MODERN_STYLE = """
    QLineEdit, QComboBox {
        border: 2px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
        background-color: white;
        color: black;
        font-size: 14px;
        min-height: 48px;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 2px solid #2563eb;
    }

    /* CRITICAL: Fix for dropdown options visibility */
    QComboBox QAbstractItemView {
        border: 2px solid #2563eb;
        background-color: white;
        color: black;
        selection-background-color: #2563eb;
        selection-color: white;
        outline: none;
        min-width: 100px;
    }

    /* Style for the list items inside the dropdown */
    QComboBox QListView {
        background-color: white;
        color: black;
    }
"""


class GeneralSolverUI(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.num_vars = 2
        self.constraints = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: #f8fafc;")

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        # Header
        header = QHBoxLayout()
        title = QLabel("General Equation Solver")
        title.setStyleSheet("font-size:26px; font-weight:800; color: #1e293b;")

        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(lambda: stack.setCurrentWidget(stack.apps))
        header.addWidget(title);
        header.addStretch();
        header.addWidget(back_btn)
        self.layout.addLayout(header)

        # Objective Function
        self.layout.addWidget(QLabel("<b>1. Objective Function</b>"))
        self.setup_objective()

        # Constraints Section
        self.layout.addWidget(QLabel("<b>2. Constraints</b>"))
        self.constraints_wrapper = QVBoxLayout()
        self.layout.addLayout(self.constraints_wrapper)

        add_btn = QPushButton("➕ Add Constraint")
        add_btn.setFixedWidth(160)
        add_btn.setFixedHeight(40)
        add_btn.clicked.connect(self.add_constraint)
        self.layout.addWidget(add_btn)

        # Solve Button
        solve_btn = QPushButton("Calculate Solution")
        solve_btn.setFixedHeight(50)
        solve_btn.setStyleSheet("background: #2563eb; color: white; font-weight: bold; border-radius: 8px;")
        solve_btn.clicked.connect(self.solve_logic)
        self.layout.addWidget(solve_btn)

        self.output = QLabel("Results will be shown here.")
        self.output.setStyleSheet("padding: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 10px;")
        self.layout.addWidget(self.output)

        self.add_constraint()

    def setup_objective(self):
        row = QHBoxLayout()
        self.obj_type = QComboBox()
        self.obj_type.addItems(["Maximize", "Minimize"])
        self.obj_type.setStyleSheet(MODERN_STYLE)
        self.obj_type.setFixedWidth(140)

        self.obj_inputs = [QLineEdit(), QLineEdit()]
        for inp in self.obj_inputs:
            inp.setStyleSheet(MODERN_STYLE)
            inp.setFixedWidth(80)
            inp.setPlaceholderText("0")

        row.addWidget(self.obj_type)
        row.addSpacing(10)
        row.addWidget(self.obj_inputs[0]);
        row.addWidget(QLabel("x +"))
        row.addWidget(self.obj_inputs[1]);
        row.addWidget(QLabel("y"))
        row.addStretch()
        self.layout.addLayout(row)

    def add_constraint(self):
        row_data = {}
        frame = QFrame()
        lay = QHBoxLayout(frame)

        x_in = QLineEdit();
        y_in = QLineEdit()
        for i in [x_in, y_in]:
            i.setStyleSheet(MODERN_STYLE);
            i.setFixedWidth(80)

        op = QComboBox()
        op.addItems(["≤", "≥", "=", "<", ">"])
        op.setStyleSheet(MODERN_STYLE)
        op.setFixedWidth(80)

        rhs = QLineEdit()
        rhs.setStyleSheet(MODERN_STYLE);
        rhs.setFixedWidth(90)

        # Modified Delete Button: Text instead of icon
        del_btn = QPushButton("Delete")
        del_btn.setFixedWidth(80)
        del_btn.setFixedHeight(48)
        del_btn.setStyleSheet("background-color: #ef4444; color: white; font-weight: bold; border-radius: 6px;")
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
        else:
            QMessageBox.warning(self, "Warning", "You need at least one constraint row.")

    def solve_logic(self):
        try:
            obj = [float(i.text() or 0) for i in self.obj_inputs]
            c_data = []
            for r in self.constraints:
                c_data.append(([float(r['x'].text() or 0), float(r['y'].text() or 0)],
                               r['op'].currentText(),
                               float(r['rhs'].text() or 0)))

            sol, res = solve_general_lp(2, obj, c_data, self.obj_type.currentText() == "Maximize")
            if sol:
                self.output.setText(f"<b>Optimal Solution Found:</b><br>{sol}<br><b>Z = {res}</b>")
            else:
                self.output.setText(f"❌ Result: {res}")
        except Exception as e:
            QMessageBox.critical(self, "Input Error", str(e))