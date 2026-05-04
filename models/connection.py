class Connection:
    def __init__(self, zone_a, zone_b, capacity: int = 1):
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.capacity = capacity
