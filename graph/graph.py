


class Graph:
    def __init__(self, data):
        self.zones = {}
        self.start = None
        self.end = None
        self.nb_drones = data.nb_drones

    def add_zone(self, zone):
        if zone.name in self.zones:
            return
        self.zones[zone.name] = zone

    def add_connection(self, connection):
        if connection.zone_a == self.start.name:
            self.start.add_neighbors(connection)
        if connection.zone_b == self.end.name:
            self.end.add_neighbors(connection)
        if connection.zone_a != self.start.name:
            self.zones[connection.zone_a].add_neighbors(connection)
        if connection.zone_b != self.end.name:
            self.zones[connection.zone_b].add_neighbors(connection)

    def set_start(self, zone):
        self.start = zone

    def set_end(self, zone):
        self.end = zone
