from pydantic import BaseModel
from datetime import date, time
from typing import List


# Node
class Emotion:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return f"Emotion(name={self.name!r} value={self.value!r} left={self.left!r} right={self.right!r})"

    def find(self, name: str):
        if self.name == name:
            return self
        if self.left:
            return self.left.find(name)
        if self.right:
            return self.right.find(name)

    def insert(self, new_node: "Emotion") -> None:
        if new_node.name <= self.name:
            if not self.left:
                self.left = new_node
            else:
                self.left.insert(new_node)
        elif new_node.name > self.name:
            if not self.right:
                self.right = new_node
            else:
                self.right.insert(new_node)

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right


class Activity:
    def __init__(self, id, name, date, start, end):
        self.id = id
        self.name: str = name
        self.date: date = date
        self.start: time = start
        self.end: time = end
        self.emotions: Emotion = None


if __name__ == "__main__":
    a = Emotion("Happiness", 33)
    a.insert(Emotion("Sadness", 20))
    a.insert(Emotion("Hatred", 666))
    a.insert(Emotion("Idk", 99))

    for node in a:
        print(node)
