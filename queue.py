class Queue:
    """Queue data structure implementation"""


    def __init__(self, items=[]):
        """Creates a Queue type object from a pre-populated list"""
        self.queue = items

    def add(self, val):
        """Adds items to the queue"""
        self.queue.append(val)

    def remove(self):
        """Removes and returns the first item in the queue
        Returns None if there's nothing in the queue"""
        try:
            val = self.queue[0]
            del self.queue[0]
        except IndexError:
            return
        return val

    def peek(self):
        """Returns but does not remove the first item in the queue
        Returns None if there's nothing in the queue"""
        try:
            val = self.queue[0]
        except IndexError:
            return
        return self.queue[0]
