from models.drone import Drone


class Simulation:
    def __init__(self, graph, paths):
        self.zones = graph.zones
        self.start = graph.start
        self.end = graph.end
        self.nb_drones = graph.nb_drones
        self.paths = paths
        self.drones = []

    def create_drones(self):
        self.drones = [
            Drone(i + 1, self.start.name)
            for i in range(self.nb_drones)
        ]

    def choice_key(self, path):
        if len(path) < 2:
            return (1, len(path))

        nxt = self.zones[path[1]]
        priority_rank = 0 if nxt.type == "priority" else 1

        return (priority_rank, len(path))

    def current_occupancy(self):
        occupied = {}

        for drone in self.drones:
            if drone.done:
                continue

            if drone.wait > 0:
                continue

            zone = drone.current_zone

            if zone not in [self.start.name, self.end.name]:
                occupied[zone] = occupied.get(zone, 0) + 1

        return occupied

    def resolve_transit(self, occupied, moves):
        for drone in self.drones:
            if drone.done:
                continue

            if drone.wait == 0:
                continue

            drone.wait -= 1

            if drone.wait == 0:
                zone = drone.target_zone
                drone.current_zone = zone
                drone.target_zone = None

                if zone != self.end.name:
                    occupied[zone] = occupied.get(zone, 0) + 1

                moves.append(f"D{drone.id}-{zone}")

                if zone == self.end.name:
                    drone.done = True

    def choose_path(self, node, occupied, edge_used):
        choices = self.paths.get(node, [])

        for path in sorted(choices, key=self.choice_key):
            if len(path) < 2:
                continue

            nxt = path[1]
            zone = self.zones[nxt]

            if nxt != self.end.name:
                if occupied.get(nxt, 0) >= zone.max_drones:
                    continue

            neighbor = None
            for edge in self.zones[node].neighbors:
                if edge.to == nxt:
                    neighbor = edge
                    break

            if neighbor is None:
                continue

            edge_key = tuple(sorted((node, nxt)))

            if edge_used.get(edge_key, 0) >= neighbor.get_capacity():
                continue

            return path, nxt, neighbor

        return None, None, None

    def run(self):
        self.create_drones()
        turn = 0

        while True:
            moves = []
            turn += 1

            occupied = self.current_occupancy()
            self.resolve_transit(occupied, moves)
            occupied = self.current_occupancy()

            edge_used = {}
            planned = []

            for drone in self.drones:
                if drone.done or drone.wait > 0:
                    continue

                node = drone.current_zone

                path, next_zone, neighbor = self.choose_path(
                    node,
                    occupied,
                    edge_used,
                )

                if next_zone is None:
                    continue

                planned.append((drone, node, next_zone, neighbor, path))

                edge_key = tuple(sorted((node, next_zone)))
                edge_used[edge_key] = edge_used.get(edge_key, 0) + 1

                if next_zone != self.end.name:
                    occupied[next_zone] = occupied.get(next_zone, 0) + 1

            for drone, node, next_zone, neighbor, path in planned:
                zone = self.zones[next_zone]
                drone.path = path

                if zone.type == "restricted":
                    drone.wait = 1
                    drone.target_zone = next_zone
                    moves.append(f"D{drone.id}-{node}-{next_zone}")
                    continue

                drone.current_zone = next_zone
                moves.append(f"D{drone.id}-{next_zone}")

                if next_zone == self.end.name:
                    drone.done = True

            if moves:
                print(" ".join(moves))

            active = any(not drone.done for drone in self.drones)

            if not active:
                break

            if not moves and not planned:
                break
        print("turn = ", turn)
