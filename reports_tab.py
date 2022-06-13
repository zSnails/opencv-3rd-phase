from tkinter import StringVar, Text
from tkinter.ttk import Frame, Label, OptionMenu
from pandas import DataFrame
from matplotlib.pyplot import Figure  # TODO: change this
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from manager import Manager
from datetime import date, timedelta
from operator import itemgetter


class ReportsTab(Frame):
    def __init__(self, *args):
        super().__init__(*args)

        self.dataset = {}
        self.hash_table = {a.name: a for a in Manager().activities}
        for activity in filter(lambda a: a.date == date.today(), Manager().activities):
            self.dataset.setdefault(activity.name, {})
            if not activity.emotions:
                continue
            for emotion in activity.emotions:
                if not self.dataset[activity.name].get(emotion.name):
                    self.dataset[activity.name].setdefault(emotion.name, emotion.value)
                else:
                    self.dataset[activity.name][emotion.name] += emotion.value

        self.init_ui()

    def init_ui(self):
        self.pack(fill="both", expand=True)

        options = [a.name for a in Manager().activities]
        clicked = StringVar(self, value=options[0])
        menu = OptionMenu(
            self, clicked, options[0], *options, command=self.update_stats
        )
        menu.grid(column=1, row=1)

        self.stats = Text(self)
        self.stats.configure(state="disabled")
        self.stats.grid(column=1, row=2)
        # df = DataFrame(self.dataset)
        # fig = Figure(figsize=(6, 5), dpi=100)
        # ax = fig.add_subplot(111)
        # chart_type = FigureCanvasTkAgg(fig, self)
        # chart_type.get_tk_widget().grid(column=1, row=1)
        # df.plot(kind="bar", legend=True, ax=ax)
        # ax.set_title("Zamn")

    def update_stats(self, val):

        act = self.hash_table.get(val)
        beginning = filter(
            lambda em: em.capture_time
            <= em.capture_time + timedelta(seconds=5).total_seconds(),
            act.emotions,
        )

        b_dataset = {}
        for emotion in beginning:
            if not b_dataset.get(emotion):
                b_dataset.setdefault(emotion.name, emotion.value)
            else:
                b_dataset[emotion.name] += emotion.value

        ending = filter(
            lambda em: em.capture_time
            >= em.capture_time - timedelta(seconds=5).total_seconds(),
            act.emotions,
        )

        e_dataset = {}
        for emotion in beginning:
            if not e_dataset.get(emotion):
                e_dataset.setdefault(emotion.name, emotion.value)
            else:
                e_dataset[emotion.name] += emotion.value

        self.stats.configure(state="normal")
        self.stats.delete(1.0, "end")
        self.stats.insert(
            "end",
            f"DM: {max(b_dataset.items(), key=itemgetter(1)) if b_dataset else 'no data'}\nDM: {max(e_dataset.items(), key=itemgetter(1)) if e_dataset else 'no data'}",
        )
        self.stats.configure(state="disabled")


if __name__ == "__main__":
    rt = ReportsTab()
