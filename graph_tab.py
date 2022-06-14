from tkinter.ttk import Frame, Button, OptionMenu
from tkinter import StringVar
from manager import Manager
from datetime import date
from pandas import DataFrame
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphTab(Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.hash_map = {a.name: a for a in Manager().activities}
        self.options = [a.name for a in Manager().activities]

        self.init_ui()

    def init_ui(self):
        self.pack(fill="both", expand=True)
        cc = StringVar(self)
        OptionMenu(self, cc, "None", *self.options, command=self.graph).grid(
            column=1, row=1
        )

    def graph(self, activity):
        activity = self.hash_map.get(activity)
        stats = self.get_stats(activity)
        if stats:
            df = DataFrame(stats)
            fig = Figure(figsize=(6, 5), dpi=100)
            ax = fig.add_subplot(111)

            chart_type = FigureCanvasTkAgg(fig, self)
            chart_type.get_tk_widget().grid(column=1, row=2)

            df.plot(kind="line", legend=True, ax=ax)
            ax.set_title(activity.name)

    def get_stats(self, activity):
        dataset = {}
        if not activity.emotions:
            return
        for emotion in activity.emotions:
            if not dataset.get(emotion.name):
                dataset.setdefault(emotion.name, [emotion.value])
            else:
                dataset[emotion.name].append(emotion.value)
        return dataset
