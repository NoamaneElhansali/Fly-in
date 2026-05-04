class Edge:
    def __init__(self, to, capacity=1):
        self.to = to
        self.capacity = capacity
        self.usage = 0
