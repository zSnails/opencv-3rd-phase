from pickle import load


with open("./data.zeta", "rb") as d:
    activities = load(d)

for activity in activities:
    print(activity.name)
    if activity.emotions:
        for emotion in activity.emotions:
            print(emotion)