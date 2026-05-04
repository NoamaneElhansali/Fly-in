from models.drone import Drone


class Simulation:
    def __init__(self, graph, paths):
        self.zones = graph.zones
        self.start = graph.start
        self.end = graph.end
        self.drones = []
        self.nb_drones = graph.nb_drones
        self.paths = paths

    def run(self):
        finished = 0

        while finished < len(self.drones):
            occupied = set()
            moves = []

            for drone in self.drones:
                if drone.done:
                    continue

                node = drone.current_zone
                choices = self.paths.get(node, [])

                next_zone = None

                for path in sorted(choices, key=len):
                    if len(path) < 2:
                        continue

                    nxt = path[1]

                    if nxt != self.end.name and nxt in occupied:
                        continue

                    next_zone = nxt
                    drone.path = path
                    break

                if next_zone is None:
                    continue

                drone.current_zone = self.zones[next_zone].name
                moves.append(f"D{drone.id}-{next_zone}")

                if next_zone != self.end.name:
                    occupied.add(next_zone)

                if next_zone == self.end.name:
                    drone.done = True
                    finished += 1

            if not moves:
                break

            print(" ".join(moves))

    def create_drones(self):
        self.drones = [
            Drone(i + 1, self.start.name) for i in range(self.nb_drones)
            ]

    # def choose_path(self, node):
    #     choices = self.paths.get(node, [])
    #     if not choices:
    #         return None
    #     return min(choices, key=len)
