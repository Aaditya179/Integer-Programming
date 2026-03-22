import tkinter as tk
from ui_helpers import (BG, SURFACE, PRIMARY, PRIMARY_LT, BORDER, TEXT_H, TEXT_M, PRIMARY_DK,
                        font, make_navbar)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        # Top gradient bar
        nav = tk.Frame(self, bg=PRIMARY, pady=24)
        nav.pack(fill="x")
        tk.Label(nav, text="⚙  Optimization Problem Solver",
                 font=font(20, "bold"), bg=PRIMARY, fg=SURFACE,
                 pady=8).pack()
        tk.Label(nav, text="Choose a solver to begin",
                 font=font(11), bg=PRIMARY, fg="#B3D1F7").pack()

        # Cards container
        center = tk.Frame(self, bg=BG)
        center.pack(expand=True, fill="both", padx=60, pady=40)

        solvers_info = [
            ("General Integer Programming",
             "Simplex + Branch & Bound",
             "Solve LP & IP problems step-by-step with tableau visualization.",
             "GeneralSolverPage", "🔢"),
            ("Knapsack Problem",
             "Greedy & Dynamic Programming",
             "Maximize value within a weight capacity using two approaches.",
             "KnapsackPage", "🎒"),
            ("Job Sequencing with Deadlines",
             "Greedy Algorithm",
             "Find the optimal schedule to maximize total profit.",
             "JobSequencingPage", "📅"),
        ]

        for icon, title, desc, page, emoji in solvers_info:
            self._solver_card(center, emoji, icon, title, desc, page)

    def _solver_card(self, parent, icon, title, subtitle, desc, page):
        c = tk.Frame(parent, bg=SURFACE,
                     highlightthickness=1, highlightbackground=BORDER,
                     cursor="hand2")
        c.pack(fill="x", pady=10)

        inner = tk.Frame(c, bg=SURFACE)
        inner.pack(fill="x", padx=20, pady=16)

        # Icon circle
        icon_lbl = tk.Label(inner, text=icon, font=font(28),
                            bg=PRIMARY_LT, width=3,
                            relief="flat")
        icon_lbl.pack(side="left", padx=(0, 16))

        text_frame = tk.Frame(inner, bg=SURFACE)
        text_frame.pack(side="left", fill="x", expand=True)

        tk.Label(text_frame, text=title, font=font(13, "bold"),
                 bg=SURFACE, fg=TEXT_H, anchor="w").pack(fill="x")
        tk.Label(text_frame, text=subtitle, font=font(10, "bold"),
                 bg=SURFACE, fg=PRIMARY, anchor="w").pack(fill="x")
        tk.Label(text_frame, text=desc, font=font(10),
                 bg=SURFACE, fg=TEXT_M, anchor="w",
                 wraplength=480, justify="left").pack(fill="x")

        arrow = tk.Label(inner, text="→", font=font(18, "bold"),
                         bg=SURFACE, fg=PRIMARY)
        arrow.pack(side="right", padx=8)

        # Hover effects
        def enter(e):
            c.config(bg=PRIMARY_LT, highlightbackground=PRIMARY)
            inner.config(bg=PRIMARY_LT)
            text_frame.config(bg=PRIMARY_LT)
            for w in text_frame.winfo_children():
                w.config(bg=PRIMARY_LT)
            icon_lbl.config(bg=PRIMARY)
            arrow.config(bg=PRIMARY_LT, fg=PRIMARY_DK)

        def leave(e):
            c.config(bg=SURFACE, highlightbackground=BORDER)
            inner.config(bg=SURFACE)
            text_frame.config(bg=SURFACE)
            for w in text_frame.winfo_children():
                w.config(bg=SURFACE)
            icon_lbl.config(bg=PRIMARY_LT)
            arrow.config(bg=SURFACE, fg=PRIMARY)

        def click(e):
            self.controller.show_frame(page)

        for widget in [c, inner, text_frame, icon_lbl, arrow] + list(text_frame.winfo_children()):
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
            widget.bind("<Button-1>", click)
