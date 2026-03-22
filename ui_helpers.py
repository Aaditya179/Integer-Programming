import tkinter as tk
from tkinter import ttk

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

        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

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
