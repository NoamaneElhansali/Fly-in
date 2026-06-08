import heapq


class PathFinder:
    def __init__(self, graph):
        self.graph = graph
        self.paths = []
        self.use_nodes = set()
        self.blocked_edges = set()

    def get_cost(self, zone):
        cost = 1

        if zone.type == "restricted":
            cost += 5

        if zone.type == "priority":
            cost -= 1

        cost += max(0, 3 - zone.max_drones)

        return cost

    def get_path(self, path_find, start, end):
        path = []
        key = end
        if key not in path_find or start == end:
            return []
        while key != start:
            path.append(key)
            key = path_find[key]
        path.append(start)

        return path[::-1]

    def set_path(self, path):
        if not path:
            return
        self.paths.append(path)
        if len(path) > 1:
            self.blocked_edges.add((path[0], path[1]))

    def find_shortest_path(self, start, end):
        dist = {node: float("inf") for node in self.graph.zones}
        parent = {}
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            current_cost, node = heapq.heappop(heap)
            if current_cost > dist[node] or \
               self.graph.zones[node].type == "blocked":
                continue
            if node == end:
                break
            for neighbor in self.graph.zones[node].neighbors:
                if self.graph.zones[neighbor.to].type == "blocked" or \
                   neighbor.to == start:
                    continue
                if (node, neighbor.to) in self.blocked_edges:
                    continue
                cost = self.get_cost(self.graph.zones[neighbor.to])
                new_cost = current_cost + cost
                if new_cost < dist[neighbor.to]:
                    dist[neighbor.to] = new_cost
                    parent[neighbor.to] = node
                    heapq.heappush(heap, (new_cost, neighbor.to))
        path = self.get_path(parent, start, end)
        # self.set_path(path)
        return path

    def find_all_shortest_path(self):
        for key, _ in self.graph.zones.items():
            path = self.find_shortest_path(key, self.graph.end.name)
            while path:
                if path in self.paths:
                    break
                self.set_path(path)
                path = self.find_shortest_path(key, self.graph.end.name)
        return self.paths

    def format_paths(self):
        paths = {}

        for path in self.paths:
            if path:
                paths.setdefault(path[0], []).append(path)

        changed = True
        while changed:
            changed = False

            for node, node_paths in list(paths.items()):
                for path in node_paths:
                    if len(path) < 2:
                        continue

                    for suffix in paths.get(path[1], []):
                        candidate = [node] + suffix
                        if candidate not in node_paths:
                            node_paths.append(candidate)
                            changed = True

        return paths
