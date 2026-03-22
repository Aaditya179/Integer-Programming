import tkinter as tk
from tkinter import messagebox
from ui_helpers import (BG, SURFACE, PRIMARY, PRIMARY_LT, BORDER, TEXT_H, TEXT_M,
                        SUCCESS, SUCCESS_LT, font, make_btn, styled_entry, card,
                        section_label, make_navbar, ScrollableFrame)
import job_sequencing_solver

class JobSequencingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        make_navbar(self, self.controller,
                    title="Job Sequencing with Deadlines",
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
        col = tk.Frame(row, bg=SURFACE)
        col.pack(side="left")
        tk.Label(col, text="Number of Jobs", font=font(10), bg=SURFACE, fg=TEXT_M).pack(anchor="w")
        self.num_jobs_entry = styled_entry(col, width=10)
        self.num_jobs_entry.pack(anchor="w", pady=(4, 0))

        btn_row = tk.Frame(cfg, bg=SURFACE)
        btn_row.pack(anchor="w", padx=16, pady=(0, 14))
        make_btn(btn_row, "Generate Job Fields", self.generate_fields).pack()

        self.job_frame = None
        self.results_frame = None

    def generate_fields(self):
        try:
            n = int(self.num_jobs_entry.get())
            if n < 1: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of jobs (≥ 1).")
            return

        if self.job_frame: self.job_frame.destroy()
        if self.results_frame: self.results_frame.destroy()

        self.job_frame = card(self._body)
        self.job_frame.pack(fill="x", padx=24, pady=(0, 8))
        section_label(self.job_frame, "Job Details", 12).pack(anchor="w", padx=16, pady=(12, 6))

        tbl = tk.Frame(self.job_frame, bg=SURFACE)
        tbl.pack(anchor="w", padx=16, pady=(0, 12))

        for col_idx, (txt, w) in enumerate([("Job", 6), ("Profit", 10), ("Deadline", 10)]):
            tk.Label(tbl, text=txt, font=font(10, "bold"), width=w,
                     bg=PRIMARY, fg=SURFACE, pady=6).grid(row=0, column=col_idx, padx=2, pady=2)

        self.entries = []
        for i in range(n):
            bg_r = PRIMARY_LT if i % 2 == 0 else SURFACE
            tk.Label(tbl, text=f"{i+1}", font=font(10), width=6,
                     bg=bg_r, fg=TEXT_H, pady=4).grid(row=i+1, column=0, padx=2, pady=1)
            p_e = styled_entry(tbl, width=9)
            p_e.grid(row=i+1, column=1, padx=4, pady=2)
            d_e = styled_entry(tbl, width=9)
            d_e.grid(row=i+1, column=2, padx=4, pady=2)
            self.entries.append((p_e, d_e))

        btn_row = tk.Frame(self.job_frame, bg=SURFACE)
        btn_row.pack(anchor="w", padx=16, pady=(0, 14))
        make_btn(btn_row, "  Solve  ", self.solve_jobs, style="success", padx=24, pady=10).pack()

    def solve_jobs(self):
        try:
            jobs = [(i+1, float(p.get()), int(d.get())) for i, (p, d) in enumerate(self.entries)]
            profit, sequence = job_sequencing_solver.JobSequencingSolver.solve(jobs)

            if self.results_frame: self.results_frame.destroy()
            self.results_frame = card(self._body)
            self.results_frame.pack(fill="x", padx=24, pady=(0, 24))

            section_label(self.results_frame, "Optimal Job Schedule", 13).pack(anchor="w", padx=16, pady=(14, 6))
            tk.Frame(self.results_frame, bg=BORDER, height=1).pack(fill="x", padx=16)

            banner = tk.Frame(self.results_frame, bg=SUCCESS_LT, highlightthickness=1, highlightbackground=SUCCESS)
            banner.pack(fill="x", padx=16, pady=(8, 4))
            tk.Label(banner, text=f"Max Profit: {profit}", font=font(13, "bold"), bg=SUCCESS_LT, fg=SUCCESS, padx=16, pady=10).pack(side="left")

            seq_frame = tk.Frame(self.results_frame, bg=SURFACE)
            seq_frame.pack(fill="x", padx=16, pady=(4, 16))
            tk.Label(seq_frame, text="Job Sequence:", font=font(10, "bold"), bg=SURFACE, fg=TEXT_H).pack(side="left")
            for j_id in sequence:
                tk.Label(seq_frame, text=f" J{j_id} ", font=font(10, "bold"), bg=PRIMARY, fg=SURFACE, padx=6, pady=4).pack(side="left", padx=3, pady=6)
        except Exception as e:
            messagebox.showerror("Error", str(e))
