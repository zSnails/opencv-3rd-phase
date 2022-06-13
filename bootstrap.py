from pickle import dump
from models import Activity
from datetime import date, time


acts = [
    Activity(1, "Ahorita", date.today(), time(20), time(21)),
    Activity(2, "Despues", date.today(), time(21), time(22)),
]

with open("./data.zeta", "wb") as d:
        dump(acts, d)
