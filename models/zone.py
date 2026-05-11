from .edge import Edge


class Zone:
    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 _type: str = 'normal',
                 zone_type: str = 'hub',
                 max_drones: int = 1,
                 color: str = None):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.color = color
        self.neighbors = []
        self.type = _type
    def add_neighbors(self, neighbor):
        to_zone = neighbor.zone_a if neighbor.zone_b == self.name \
            else neighbor.zone_b
        self.neighbors.append(Edge(to_zone, neighbor.capacity))
