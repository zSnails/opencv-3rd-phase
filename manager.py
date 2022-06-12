from pickle import load, dump


class Manager:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            try:
                cls.__instance.load()
            except EOFError:
                print("warning: data file is empty")
        return cls.__instance

    # def __init__(self):
    #     self.activities = []

    def load(self):
        with open("./data.zeta", "rb") as d:
            self.activities = load(d)

    def save(self):
        with open("./data.zeta", "wb") as d:
            dump(self.activities, d)



if __name__ == "__main__":
    c1 = Manager()
    c2 = Manager()

    print(c1, c2)
