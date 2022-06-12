from tkinter import Tk
from tkinter.ttk import Notebook, Frame
from focus_tab import FocusTab

class Program(Tk):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.wm_title("Time management program")
        self.wm_minsize(width=600, height=300)

        self.nb = Notebook(self)
        self.nb.add(FocusTab(self), text="Focus")
        # TODO: add this
        # nb.add(DiagramTab(self), text="Focus Graph")
        self.nb.pack(expand=True, fill="both")


    def cleanup(self):
        for child in self.children.values():
            if isinstance(child, Frame):
                try:
                    child.killall()
                except Exception as e:
                    print(e)

    def run(self):
        self.mainloop()
