class Edge:
    def __init__(self, to, capacity=1):
        self.to = to
        self.capacity = capacity
        self.usage = 0

    def get_capacity(self):
        return self.capacity
