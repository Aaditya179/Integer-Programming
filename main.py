import tkinter as tk
from tkinter import ttk
from ui_helpers import BG, SURFACE, PRIMARY, BORDER, TEXT_B, FONT_FAMILY
from home_page import HomePage
from integer_gui import GeneralSolverPage
from knapsack_gui import KnapsackPage
from job_sequencing_gui import JobSequencingPage

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

if __name__ == "__main__":
    app = Application()
    app.mainloop()
