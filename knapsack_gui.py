import tkinter as tk
from tkinter import messagebox
from ui_helpers import (BG, SURFACE, PRIMARY, PRIMARY_LT, BORDER, TEXT_H, TEXT_B, TEXT_M,
                        SUCCESS, SUCCESS_LT, font, make_btn, styled_entry, card,
                        section_label, make_navbar, ScrollableFrame)
import knapsack_solver

class KnapsackPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        make_navbar(self, self.controller,
                    title="Knapsack Problem Solver",
                    back_page="HomePage")

        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True)
        body = scroll.scrollable_frame
        self._body = body

        cfg = card(body)
        cfg.pack(fill="x", padx=24, pady=18)
        section_label(cfg, "Problem Setup", 13).pack(anchor="w", padx=16, pady=(12, 8))

        row = tk.Frame(cfg, bg=SURFACE)
        row.pack(anchor="w", padx=16, pady=(0, 12))

        def lentry(parent_row, lbl):
            col = tk.Frame(parent_row, bg=SURFACE)
            col.pack(side="left", padx=(0, 20))
            tk.Label(col, text=lbl, font=font(10), bg=SURFACE, fg=TEXT_M).pack(anchor="w")
            e = styled_entry(col, width=10)
            e.pack(anchor="w", pady=(4, 0))
            return e

        self.num_items_entry = lentry(row, "Number of Items")
        self.capacity_entry  = lentry(row, "Knapsack Capacity")

        btn_row = tk.Frame(cfg, bg=SURFACE)
        btn_row.pack(anchor="w", padx=16, pady=(0, 14))
        make_btn(btn_row, "Generate Item Fields", self.generate_fields).pack()

        self.item_frame = None
        self.results_frame = None

    def generate_fields(self):
        try:
            n = int(self.num_items_entry.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of items (≥ 1).")
            return

        if self.item_frame:
            self.item_frame.destroy()
        if self.results_frame:
            self.results_frame.destroy()

        self.item_frame = card(self._body)
        self.item_frame.pack(fill="x", padx=24, pady=(0, 8))
        section_label(self.item_frame, "Item Details", 12).pack(
            anchor="w", padx=16, pady=(12, 6))

        tbl = tk.Frame(self.item_frame, bg=SURFACE)
        tbl.pack(anchor="w", padx=16, pady=(0, 12))

        for col_idx, (txt, w) in enumerate([("Item", 6), ("Value", 10), ("Weight", 10)]):
            tk.Label(tbl, text=txt, font=font(10, "bold"), width=w,
                     bg=PRIMARY, fg=SURFACE, pady=6
                     ).grid(row=0, column=col_idx, padx=2, pady=2)

        self.entries = []
        for i in range(n):
            bg_r = PRIMARY_LT if i % 2 == 0 else SURFACE
            tk.Label(tbl, text=f"{i+1}", font=font(10), width=6,
                     bg=bg_r, fg=TEXT_H, pady=4).grid(row=i+1, column=0, padx=2, pady=1)
            v_e = styled_entry(tbl, width=9)
            v_e.grid(row=i+1, column=1, padx=4, pady=2)
            w_e = styled_entry(tbl, width=9)
            w_e.grid(row=i+1, column=2, padx=4, pady=2)
            self.entries.append((v_e, w_e))

        btn_row = tk.Frame(self.item_frame, bg=SURFACE)
        btn_row.pack(anchor="w", padx=16, pady=(0, 14))
        make_btn(btn_row, "  Solve  ", self.solve_knapsack, style="success", padx=24, pady=10).pack()

    def solve_knapsack(self):
        try:
            capacity = float(self.capacity_entry.get())
            items = [(float(v.get()), float(w.get()), i+1)
                     for i, (v, w) in enumerate(self.entries)]
            g_val, g_items = knapsack_solver.KnapsackSolver.solve_greedy(items, capacity)
            dp_val, dp_items = knapsack_solver.KnapsackSolver.solve_dp(items, int(capacity))

            if self.results_frame:
                self.results_frame.destroy()
            self.results_frame = tk.Frame(self._body, bg=BG)
            self.results_frame.pack(fill="x", padx=24, pady=(0, 24))

            self._result_card(self.results_frame, "Fractional Knapsack – Greedy",
                              f"Max Profit: {g_val:.3f}", f"Selected Items (ID, Fraction): {g_items}")
            self._result_card(self.results_frame, "0/1 Knapsack – Dynamic Programming",
                              f"Max Profit: {dp_val}", f"Selected Item IDs: {dp_items}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _result_card(self, parent, title, line1, line2):
        c = card(parent)
        c.pack(fill="x", pady=6)
        section_label(c, title, 12).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Frame(c, bg=BORDER, height=1).pack(fill="x", padx=16)
        tk.Label(c, text=line1, font=font(11, "bold"),
                 bg=SURFACE, fg=SUCCESS, anchor="w").pack(anchor="w", padx=16, pady=(6, 2))
        tk.Label(c, text=line2, font=font(10), bg=SURFACE, fg=TEXT_B,
                 anchor="w", wraplength=700, justify="left").pack(anchor="w", padx=16, pady=(0, 14))
