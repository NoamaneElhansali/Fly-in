from models.drone import Drone


class Simulation:
    def __init__(self, graph, paths):
        self.zones = graph.zones
        self.start = graph.start
        self.end = graph.end
        self.nb_drones = graph.nb_drones
        self.paths = paths
        self.drones = []
        self.history_turn = []

    def create_drones(self):
        self.drones = [
            Drone(i + 1, None)
            for i in range(self.nb_drones)
        ]

    def count_path_cost(self, path):
        return sum(
            2 if self.zones[x].type == "restricted" else 1 for x in path
        )

    def current_occupancy(self):
        occupied = {}

        for drone in self.drones:
            if drone.done:
                continue

            if drone.current_zone is None:
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

            if drone.wait > 0:
                drone.wait -= 1
                if (
                    drone.wait == 1
                        and self.zones[drone.current_zone].type == "restricted"
                        ):
                    moves.append(
                        f"D{drone.id}-{drone.current_zone}-{drone.target_zone}"
                        )
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
        sorted_choices = sorted(choices, key=lambda p: len(p))

        if sorted_choices:
            min_len = len(sorted_choices[0])
            sorted_choices = [p for p in sorted_choices if len(p) == min_len]

        for path in sorted_choices:
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
        launched = 0

        while True:
            moves = []
            turn_data = {
                "turn": turn,
                "moves": []
            }

            occupied = self.current_occupancy()
            self.resolve_transit(occupied, moves)

            start_count = sum(
                1 for d in self.drones
                if d.current_zone == self.start.name and not d.done
            )
            if (launched < self.nb_drones
                    and start_count < self.start.max_drones):
                self.drones[launched].current_zone = self.start.name
                launched += 1

            edge_used = {}
            planned = []

            for drone in self.drones:
                if drone.done or drone.wait > 0:
                    continue

                if drone.current_zone is None:
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
                if node not in [self.start.name, self.end.name]:
                    occupied[node] = max(0, occupied.get(node, 0) - 1)

            for drone, node, next_zone, neighbor, path in planned:
                zone = self.zones[next_zone]
                drone.path = path

                if zone.type == "restricted":
                    drone.wait = 2
                    drone.target_zone = next_zone
                    turn_data['moves'].append({
                        'drone': drone.id,
                        'from': node,
                        'to': next_zone
                    })
                else:
                    drone.current_zone = next_zone
                    moves.append(f"D{drone.id}-{next_zone}")
                    turn_data['moves'].append({
                        'drone': drone.id,
                        'from': node,
                        'to': next_zone
                    })

                    if next_zone == self.end.name:
                        drone.done = True

            if moves:
                print(" ".join(moves))
                turn += 1
                self.history_turn.append(
                    turn_data
                )

            active = any(not drone.done for drone in self.drones)

            if not active:
                break

            if not moves and not planned:
                break

        print("<<----[ turns =", turn, " ]---->>")
        return self.history_turn
