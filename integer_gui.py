import tkinter as tk
from tkinter import messagebox
from ui_helpers import (BG, SURFACE, PRIMARY, PRIMARY_LT, BORDER, TEXT_H, TEXT_B, TEXT_M,
                        ERROR, ERROR_LT, SUCCESS, SUCCESS_LT, PIVOT_YLW, ROW_HL, COL_HL,
                        font, make_btn, styled_entry, card, section_label, make_navbar, ScrollableFrame)
import integer_solver

class GeneralSolverPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        make_navbar(self, self.controller,
                    title="Integer Programming Solver",
                    back_page="HomePage")

        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True)
        body = scroll.scrollable_frame

        cfg_card = card(body)
        cfg_card.pack(fill="x", padx=24, pady=(18, 0))

        section_label(cfg_card, "Problem Configuration", 13).pack(anchor="w", padx=16, pady=(12, 8))

        row = tk.Frame(cfg_card, bg=SURFACE)
        row.pack(fill="x", padx=16, pady=(0, 12))

        opt_col = tk.Frame(row, bg=SURFACE)
        opt_col.pack(side="left", padx=(0, 24))
        tk.Label(opt_col, text="Optimization Type", font=font(10), bg=SURFACE, fg=TEXT_M).pack(anchor="w")
        self.opt_type = tk.StringVar(value="Maximize")
        from tkinter import ttk
        combo = ttk.Combobox(opt_col, textvariable=self.opt_type,
                             values=["Maximize", "Minimize"],
                             state="readonly", width=14,
                             style="Custom.TCombobox")
        combo.pack(anchor="w", pady=(4, 0))

        def labeled_entry(parent_frame, label_text):
            col = tk.Frame(parent_frame, bg=SURFACE)
            col.pack(side="left", padx=(0, 24))
            tk.Label(col, text=label_text, font=font(10), bg=SURFACE, fg=TEXT_M).pack(anchor="w")
            e = styled_entry(col, width=8)
            e.pack(anchor="w", pady=(4, 0))
            return e

        self.num_vars_entry = labeled_entry(row, "Number of Variables")
        self.num_constr_entry = labeled_entry(row, "Number of Constraints")

        btn_row = tk.Frame(cfg_card, bg=SURFACE)
        btn_row.pack(anchor="w", padx=16, pady=(0, 16))
        gen_btn = make_btn(btn_row, "Generate Input Fields",
                           self.generate_fields, style="primary")
        gen_btn.pack(side="left")

        self.dynamic_area = tk.Frame(body, bg=BG)
        self.dynamic_area.pack(fill="x", padx=24, pady=8)

        self.input_fields_frame = None
        self.results_frame = None
        self._body = body

    def generate_fields(self):
        try:
            vars_count = int(self.num_vars_entry.get())
            constr_count = int(self.num_constr_entry.get())
            if vars_count < 1 or constr_count < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error",
                                 "Please enter positive integers for variables and constraints.")
            return

        if self.input_fields_frame:
            self.input_fields_frame.destroy()
        if self.results_frame:
            self.results_frame.destroy()

        self.input_fields_frame = card(self.dynamic_area)
        self.input_fields_frame.pack(fill="x", pady=(0, 8))

        section_label(self.input_fields_frame, "Objective Function  (Z = …)", 12).pack(
            anchor="w", padx=16, pady=(12, 4))
        tk.Label(self.input_fields_frame, text="Maximize/Minimize the value of Z",
                 font=font(9), bg=SURFACE, fg=TEXT_M).pack(anchor="w", padx=16)

        obj_row = tk.Frame(self.input_fields_frame, bg=SURFACE)
        obj_row.pack(anchor="w", padx=16, pady=(6, 12))
        self.obj_entries = []
        for i in range(vars_count):
            tk.Label(obj_row, text=f"x{i+1}", font=font(10, "bold"),
                     bg=SURFACE, fg=PRIMARY).grid(row=0, column=i*2, padx=(0, 2))
            e = styled_entry(obj_row, width=6)
            e.grid(row=0, column=i*2+1, padx=(0, 12))
            self.obj_entries.append(e)
            if i < vars_count - 1:
                tk.Label(obj_row, text="+", font=font(11),
                         bg=SURFACE, fg=TEXT_M).grid(row=0, column=i*2+2)

        section_label(self.input_fields_frame, "Constraints  (≤ RHS)", 12).pack(
            anchor="w", padx=16, pady=(8, 6))
        self.constr_entries = []
        for i in range(constr_count):
            c_row = tk.Frame(self.input_fields_frame, bg=SURFACE)
            c_row.pack(anchor="w", padx=16, pady=4)
            tk.Label(c_row, text=f"C{i+1}:", font=font(10, "bold"),
                     bg=SURFACE, fg=TEXT_M, width=3).grid(row=0, column=0)
            row_entries = []
            for j in range(vars_count):
                tk.Label(c_row, text=f"x{j+1}", font=font(10),
                         bg=SURFACE, fg=PRIMARY).grid(row=0, column=j*2+1, padx=(4, 2))
                e = styled_entry(c_row, width=5)
                e.grid(row=0, column=j*2+2, padx=(0, 8))
                row_entries.append(e)
                if j < vars_count - 1:
                    tk.Label(c_row, text="+", font=font(10),
                             bg=SURFACE, fg=TEXT_M).grid(row=0, column=j*2+3)
            tk.Label(c_row, text=" ≤ ", font=font(10, "bold"),
                     bg=SURFACE, fg=TEXT_M).grid(row=0, column=vars_count*2+1)
            rhs = styled_entry(c_row, width=6)
            rhs.grid(row=0, column=vars_count*2+2, padx=(2, 0))
            row_entries.append(rhs)
            self.constr_entries.append(row_entries)

        solve_row = tk.Frame(self.input_fields_frame, bg=SURFACE)
        solve_row.pack(anchor="w", padx=16, pady=(8, 16))
        make_btn(solve_row, "  Solve  ", self.solve_ip, style="success", padx=24, pady=10).pack()

    def solve_ip(self):
        try:
            v_count = int(self.num_vars_entry.get())
            obj = [float(e.get()) for e in self.obj_entries]
            constraints, rhs = [], []
            for row in self.constr_entries:
                constraints.append([float(row[j].get()) for j in range(v_count)])
                rhs.append(float(row[-1].get()))

            is_max = self.opt_type.get() == "Maximize"
            ip_solver = integer_solver.IntegerSolver(v_count, len(constraints), obj,
                                              constraints, rhs, is_max)
            int_solution, int_val = ip_solver.solve()
            initial_lp_solver = ip_solver.history_of_solvers[0]
            self.display_results(initial_lp_solver, int_solution, int_val)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def display_results(self, lp_solver, int_sol, int_val):
        if self.results_frame:
            self.results_frame.destroy()
        self.results_frame = tk.Frame(self._body, bg=BG)
        self.results_frame.pack(fill="x", padx=24, pady=(0, 24))

        simplex_card = card(self.results_frame)
        simplex_card.pack(fill="x", pady=(0, 10))
        section_label(simplex_card, "Simplex Method – Step-by-Step", 13).pack(
            anchor="w", padx=16, pady=(14, 6))

        for idx, tableau in enumerate(lp_solver.history):
            self.draw_tableau(simplex_card, tableau, idx + 1)

        lp_summary = tk.Frame(simplex_card, bg=PRIMARY_LT,
                               highlightthickness=1, highlightbackground=BORDER)
        lp_summary.pack(fill="x", padx=16, pady=(8, 14))
        lp_sol_str = "  |  ".join([f"x{i+1} = {lp_solver.solution[i]:.3f}"
                                    for i in range(len(lp_solver.solution))])
        tk.Label(lp_summary, text=f"LP Relaxation Optimum:  {lp_sol_str}",
                 font=font(10, "bold"), bg=PRIMARY_LT, fg=TEXT_H, pady=6).pack(side="left", padx=12)
        tk.Label(lp_summary, text=f"Z = {lp_solver.optimal_val:.3f}",
                 font=font(10, "bold"), bg=PRIMARY_LT, fg=PRIMARY).pack(side="right", padx=12)

        bb_card = card(self.results_frame)
        bb_card.pack(fill="x", pady=4)
        section_label(bb_card, "Branch & Bound – Integer Solution", 13).pack(
            anchor="w", padx=16, pady=(14, 6))

        if int_sol is None:
            result_bg, result_fg = ERROR_LT, ERROR
            result_txt = "No feasible integer solution found."
        else:
            result_bg, result_fg = SUCCESS_LT, SUCCESS
            sol_str = "  |  ".join([f"x{i+1} = {int_sol[i]}" for i in range(len(int_sol))])
            result_txt = f"{sol_str}    →   Z = {int_val}"

        banner = tk.Frame(bb_card, bg=result_bg,
                          highlightthickness=1, highlightbackground=result_fg)
        banner.pack(fill="x", padx=16, pady=(0, 14))
        tk.Label(banner, text=result_txt, font=font(12, "bold"),
                 bg=result_bg, fg=result_fg, pady=12, padx=16).pack()

    def draw_tableau(self, parent, tableau, iter_num):
        wrap = tk.Frame(parent, bg=BG, padx=16, pady=6)
        wrap.pack(fill="x")
        hdr = tk.Frame(wrap, bg=SURFACE)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"Iteration {iter_num}", font=font(10, "bold"),
                 bg=PRIMARY_LT, fg=PRIMARY, padx=10, pady=4).pack(side="left")
        if tableau.pivot_row is not None and tableau.pivot_col is not None:
            entering = tableau.col_labels[tableau.pivot_col]
            leaving  = tableau.row_labels[tableau.pivot_row]
            elem     = tableau.matrix[tableau.pivot_row][tableau.pivot_col]
            tk.Label(hdr, text=f"  Pivot → entering: {entering},  leaving: {leaving},  element: {elem:.3f}",
                     font=font(9, "bold"), bg=PRIMARY_LT, fg=TEXT_M, padx=8, pady=4).pack(side="left")
        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x")

        tbl = tk.Frame(wrap, bg=SURFACE)
        tbl.pack(anchor="w")

        cell_w = 9
        tk.Label(tbl, text="Basis", font=font(9, "bold"), width=cell_w,
                 bg=PRIMARY, fg=SURFACE, relief="flat", pady=5).grid(row=0, column=0, padx=1, pady=1)
        for j, lbl in enumerate(tableau.col_labels):
            is_pivot_col = (j == tableau.pivot_col)
            bg = PRIMARY if is_pivot_col else "#4A90D9"
            tk.Label(tbl, text=lbl, font=font(9, "bold"), width=cell_w,
                     bg=bg, fg=SURFACE, relief="flat", pady=5
                     ).grid(row=0, column=j+1, padx=1, pady=1)

        for i, row in enumerate(tableau.matrix):
            rl = tableau.row_labels[i]
            is_pivot_row = (i == tableau.pivot_row)
            row_bg_lbl = ROW_HL if is_pivot_row else SURFACE
            tk.Label(tbl, text=rl, font=font(9, "bold"), width=cell_w,
                     bg=row_bg_lbl, fg=TEXT_H, pady=4
                     ).grid(row=i+1, column=0, padx=1, pady=1)

            for j, val in enumerate(row):
                is_pivot = (i == tableau.pivot_row and j == tableau.pivot_col)
                is_pr    = (i == tableau.pivot_row)
                is_pc    = (j == tableau.pivot_col)
                if is_pivot:
                    bg_c, fg_c = PIVOT_YLW, "#333"
                elif is_pr:
                    bg_c, fg_c = ROW_HL, TEXT_B
                elif is_pc:
                    bg_c, fg_c = COL_HL, TEXT_B
                else:
                    bg_c, fg_c = SURFACE, TEXT_B
                tk.Label(tbl, text=f"{val:8.3f}", width=cell_w,
                         font=font(9), bg=bg_c, fg=fg_c, pady=4
                         ).grid(row=i+1, column=j+1, padx=1, pady=1)

        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x", pady=(6, 0))
