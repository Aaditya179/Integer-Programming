import tkinter as tk
from tkinter import ttk, messagebox
import solvers

# ─── Design Tokens ────────────────────────────────────────────────────────────
BG          = "#F0F6FF"          # Page background (very light blue-white)
SURFACE     = "#FFFFFF"          # Card / panel background
PRIMARY     = "#1565E8"          # Primary blue – vivid royal blue
PRIMARY_DK  = "#0D43B5"          # Darker blue (hover)
PRIMARY_LT  = "#DDEEFF"          # Very light blue (hover bg)
ACCENT      = "#3B82F6"          # Accent / highlight
TEXT_H      = "#0D2D6B"          # Heading text
TEXT_B      = "#1A2B40"          # Body text
TEXT_M      = "#5A6E8A"          # Muted text
BORDER      = "#C8DCFA"          # Subtle border
SUCCESS     = "#059669"          # Vivid emerald green
SUCCESS_LT  = "#D1FAE5"
WARNING     = "#B45309"
WARNING_LT  = "#FEF3C7"
ERROR       = "#DC2626"          # Bright red
ERROR_LT    = "#FEE2E2"
PIVOT_YLW   = "#FFC107"
ROW_HL      = "#E8F5E9"
COL_HL      = "#E3F0FF"

FONT_FAMILY = "Helvetica"

def font(size=11, weight="normal"):
    return (FONT_FAMILY, size, weight)


# ─── Hover Button Helper ───────────────────────────────────────────────────────
def make_btn(parent, text, command, style="primary", width=None, padx=16, pady=8):
    """Create a styled button using Label for better macOS support."""
    styles = {
        "primary":  dict(bg=PRIMARY,   fg=SURFACE,    hover_bg=PRIMARY_DK,  hover_fg=SURFACE),
        "outline":  dict(bg=SURFACE,   fg=PRIMARY,    hover_bg=PRIMARY_LT,  hover_fg=PRIMARY_DK),
        "success":  dict(bg=SUCCESS,   fg=SURFACE,    hover_bg="#047857",   hover_fg=SURFACE),
        "danger":   dict(bg=ERROR,     fg=SURFACE,    hover_bg="#B91C1C",   hover_fg=SURFACE),
        "ghost":    dict(bg=BG,        fg=PRIMARY,    hover_bg=PRIMARY_LT,  hover_fg=PRIMARY_DK),
    }
    s = styles.get(style, styles["primary"])

    btn = tk.Label(parent, text=text, bg=s["bg"], fg=s["fg"],
                  font=font(11, "bold"), padx=padx, pady=pady,
                  cursor="hand2", anchor="center")
    
    if width:
        btn.config(width=width)

    def on_enter(e):
        btn.config(bg=s["hover_bg"], fg=s["hover_fg"])
    def on_leave(e):
        btn.config(bg=s["bg"], fg=s["fg"])
    def on_click(e):
        command()

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_click)
    return btn


def styled_entry(parent, width=12):
    e = tk.Entry(parent, width=width, font=font(11),
                 bg=SURFACE, fg=TEXT_B,
                 relief="flat", bd=0,
                 insertbackground=PRIMARY,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=PRIMARY)
    return e


def card(parent, padx=16, pady=12, **kw):
    """Raised card-like frame."""
    f = tk.Frame(parent, bg=SURFACE,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 **kw)
    return f


def section_label(parent, text, size=13):
    return tk.Label(parent, text=text, font=font(size, "bold"),
                    bg=SURFACE, fg=TEXT_H)


def body_label(parent, text, **kw):
    return tk.Label(parent, text=text, font=font(11),
                    bg=SURFACE, fg=TEXT_B, **kw)


# ─── Scrollable Frame ──────────────────────────────────────────────────────────
class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg=BG, *args, **kwargs):
        super().__init__(container, bg=bg, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        style = ttk.Style()
        style.configure("Thin.Vertical.TScrollbar", troughcolor=BG, background=BORDER)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview,
                                       style="Thin.Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self._win = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Expand inner frame with canvas width
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))
        # Mouse-wheel scrolling
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))


# ─── Application Shell ─────────────────────────────────────────────────────────
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimization Problem Solver")
        self.geometry("960x720")
        self.minsize(800, 600)
        self.configure(bg=BG)
        self.eval('tk::PlaceWindow . center')

        # TTK style for combobox
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
                         fieldbackground=SURFACE,
                         background=SURFACE,
                         foreground=TEXT_B,
                         selectbackground=PRIMARY,
                         selectforeground=SURFACE,
                         bordercolor=BORDER,
                         arrowcolor=PRIMARY,
                         font=(FONT_FAMILY, 11))

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, GeneralSolverPage, KnapsackPage, JobSequencingPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# ─── Navigation Bar ────────────────────────────────────────────────────────────
def make_navbar(parent, controller, title="Optimization Solver", back_page=None):
    nav = tk.Frame(parent, bg=PRIMARY, pady=14)
    nav.pack(fill="x")

    inner = tk.Frame(nav, bg=PRIMARY)
    inner.pack(fill="x", padx=20)

    if back_page:
        back_btn = tk.Label(
            inner, text="← Back",
            bg="#2563EB", fg=SURFACE, font=font(10, "bold"),
            cursor="hand2", padx=14, pady=5,
            highlightthickness=1,
            highlightbackground="#60A5FA"
        )
        back_btn.pack(side="left")

        def on_enter(e):
            back_btn.config(bg="#1E40AF", highlightbackground="#93C5FD")
        def on_leave(e):
            back_btn.config(bg="#2563EB", highlightbackground="#60A5FA")
        def on_click(e):
            controller.show_frame(back_page)

        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)
        back_btn.bind("<Button-1>", on_click)

    tk.Label(inner, text=title, font=font(16, "bold"),
             bg=PRIMARY, fg=SURFACE).pack(side="left", padx=(20 if back_page else 0))
    return nav


# ─── HomePage ──────────────────────────────────────────────────────────────────
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


# ─── GeneralSolverPage ─────────────────────────────────────────────────────────
class GeneralSolverPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        make_navbar(self, self.controller,
                    title="Integer Programming Solver",
                    back_page="HomePage")

        # Scrollable body
        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True)
        body = scroll.scrollable_frame

        # ── Config Card ──
        cfg_card = card(body)
        cfg_card.pack(fill="x", padx=24, pady=(18, 0))

        section_label(cfg_card, "Problem Configuration", 13).pack(anchor="w", padx=16, pady=(12, 8))

        row = tk.Frame(cfg_card, bg=SURFACE)
        row.pack(fill="x", padx=16, pady=(0, 12))

        # Optimization type
        opt_col = tk.Frame(row, bg=SURFACE)
        opt_col.pack(side="left", padx=(0, 24))
        tk.Label(opt_col, text="Optimization Type", font=font(10), bg=SURFACE, fg=TEXT_M).pack(anchor="w")
        self.opt_type = tk.StringVar(value="Maximize")
        combo = ttk.Combobox(opt_col, textvariable=self.opt_type,
                             values=["Maximize", "Minimize"],
                             state="readonly", width=14,
                             style="Custom.TCombobox")
        combo.pack(anchor="w", pady=(4, 0))

        # Number of vars
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

        # Placeholder for dynamic input
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

        # --- Constraints ---
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
            ip_solver = solvers.IntegerSolver(v_count, len(constraints), obj,
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

        # ── Simplex Steps ──
        simplex_card = card(self.results_frame)
        simplex_card.pack(fill="x", pady=(0, 10))
        section_label(simplex_card, "Simplex Method – Step-by-Step", 13).pack(
            anchor="w", padx=16, pady=(14, 6))

        for idx, tableau in enumerate(lp_solver.history):
            self.draw_tableau(simplex_card, tableau, idx + 1)

        # LP summary
        lp_summary = tk.Frame(simplex_card, bg=PRIMARY_LT,
                              highlightthickness=1, highlightbackground=BORDER)
        lp_summary.pack(fill="x", padx=16, pady=(8, 14))
        lp_sol_str = "  |  ".join([f"x{i+1} = {lp_solver.solution[i]:.3f}"
                                   for i in range(len(lp_solver.solution))])
        tk.Label(lp_summary, text=f"LP Relaxation Optimum:  {lp_sol_str}",
                 font=font(10, "bold"), bg=PRIMARY_LT, fg=TEXT_H, pady=6).pack(side="left", padx=12)
        tk.Label(lp_summary, text=f"Z = {lp_solver.optimal_val:.3f}",
                 font=font(10, "bold"), bg=PRIMARY_LT, fg=PRIMARY).pack(side="right", padx=12)

        # ── B&B Result ──
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

        # Iteration header
        hdr = tk.Frame(wrap, bg=SURFACE)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"Iteration {iter_num}", font=font(10, "bold"),
                 bg=PRIMARY_LT, fg=PRIMARY, padx=10, pady=4).pack(side="left")
        if tableau.pivot_row is not None and tableau.pivot_col is not None:
            entering = tableau.col_labels[tableau.pivot_col]
            leaving  = tableau.row_labels[tableau.pivot_row]
            elem     = tableau.matrix[tableau.pivot_row][tableau.pivot_col]
            tk.Label(hdr,
                     text=f"  Pivot → entering: {entering},  leaving: {leaving},  element: {elem:.3f}",
                     font=font(9, "bold"), bg=PRIMARY_LT, fg=TEXT_M, padx=8, pady=4).pack(side="left")
        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x")

        tbl = tk.Frame(wrap, bg=SURFACE)
        tbl.pack(anchor="w")

        cell_w = 9
        # Header row
        tk.Label(tbl, text="Basis", font=font(9, "bold"), width=cell_w,
                 bg=PRIMARY, fg=SURFACE, relief="flat", pady=5).grid(row=0, column=0, padx=1, pady=1)
        for j, lbl in enumerate(tableau.col_labels):
            is_pivot_col = (j == tableau.pivot_col)
            bg = PRIMARY if is_pivot_col else "#4A90D9"
            tk.Label(tbl, text=lbl, font=font(9, "bold"), width=cell_w,
                     bg=bg, fg=SURFACE, relief="flat", pady=5
                     ).grid(row=0, column=j+1, padx=1, pady=1)

        # Data rows
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


# ─── KnapsackPage ──────────────────────────────────────────────────────────────
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

        # Config card
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

        # Header
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
            g_val, g_items = solvers.KnapsackSolver.solve_greedy(items, capacity)
            dp_val, dp_items = solvers.KnapsackSolver.solve_dp(items, int(capacity))

            if self.results_frame:
                self.results_frame.destroy()
            self.results_frame = tk.Frame(self._body, bg=BG)
            self.results_frame.pack(fill="x", padx=24, pady=(0, 24))

            self._result_card(
                self.results_frame,
                "Fractional Knapsack – Greedy",
                f"Max Profit: {g_val:.3f}",
                f"Selected Items (ID, Fraction): {g_items}"
            )
            self._result_card(
                self.results_frame,
                "0/1 Knapsack – Dynamic Programming",
                f"Max Profit: {dp_val}",
                f"Selected Item IDs: {dp_items}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _result_card(self, parent, title, line1, line2):
        c = card(parent)
        c.pack(fill="x", pady=6)
        section_label(c, title, 12).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Frame(c, bg=BORDER, height=1).pack(fill="x", padx=16)
        tk.Label(c, text=line1, font=font(11, "bold"),
                 bg=SURFACE, fg=SUCCESS, anchor="w").pack(anchor="w", padx=16, pady=(6, 2))
        tk.Label(c, text=line2, font=font(10),
                 bg=SURFACE, fg=TEXT_B, anchor="w", wraplength=700, justify="left"
                 ).pack(anchor="w", padx=16, pady=(0, 14))


# ─── JobSequencingPage ─────────────────────────────────────────────────────────
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
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of jobs (≥ 1).")
            return

        if self.job_frame:
            self.job_frame.destroy()
        if self.results_frame:
            self.results_frame.destroy()

        self.job_frame = card(self._body)
        self.job_frame.pack(fill="x", padx=24, pady=(0, 8))
        section_label(self.job_frame, "Job Details", 12).pack(
            anchor="w", padx=16, pady=(12, 6))

        tbl = tk.Frame(self.job_frame, bg=SURFACE)
        tbl.pack(anchor="w", padx=16, pady=(0, 12))

        for col_idx, (txt, w) in enumerate([("Job", 6), ("Profit", 10), ("Deadline", 10)]):
            tk.Label(tbl, text=txt, font=font(10, "bold"), width=w,
                     bg=PRIMARY, fg=SURFACE, pady=6
                     ).grid(row=0, column=col_idx, padx=2, pady=2)

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
            jobs = [(i+1, float(p.get()), int(d.get()))
                    for i, (p, d) in enumerate(self.entries)]
            profit, sequence = solvers.JobSequencingSolver.solve(jobs)

            if self.results_frame:
                self.results_frame.destroy()
            self.results_frame = card(self._body)
            self.results_frame.pack(fill="x", padx=24, pady=(0, 24))

            section_label(self.results_frame, "Optimal Job Schedule", 13).pack(
                anchor="w", padx=16, pady=(14, 6))
            tk.Frame(self.results_frame, bg=BORDER, height=1).pack(fill="x", padx=16)

            banner = tk.Frame(self.results_frame, bg=SUCCESS_LT,
                              highlightthickness=1, highlightbackground=SUCCESS)
            banner.pack(fill="x", padx=16, pady=(8, 4))
            tk.Label(banner, text=f"Max Profit: {profit}",
                     font=font(13, "bold"), bg=SUCCESS_LT, fg=SUCCESS,
                     padx=16, pady=10).pack(side="left")

            seq_frame = tk.Frame(self.results_frame, bg=SURFACE)
            seq_frame.pack(fill="x", padx=16, pady=(4, 16))
            tk.Label(seq_frame, text="Job Sequence:", font=font(10, "bold"),
                     bg=SURFACE, fg=TEXT_M).pack(side="left")
            for j_id in sequence:
                tk.Label(seq_frame,
                         text=f" J{j_id} ", font=font(10, "bold"),
                         bg=PRIMARY, fg=SURFACE, padx=6, pady=4,
                         relief="flat"
                         ).pack(side="left", padx=3, pady=6)

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ─── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = Application()
    app.mainloop()
