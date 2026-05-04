import heapq

graph = {
    "start": ["A", "B"],
    "A": ["C"],
    "B": ["C"],
    "C": ["D", "E"],
    "D": ["goal"],
    "E": ["goal"],
    "goal": []
}

costs = {
    "start": 0,
    "A": 1,
    "B": 2,
    "C": 1,
    "D": 1,
    "E": 2,
    "goal": 1
}


def dijkstra(graph, costs, start, end):
    dist = {node: float("inf") for node in graph}
    parent = {}

    dist[start] = 0
    heap = [(0, start)]

    while heap:
        current_cost, node = heapq.heappop(heap)

        if current_cost > dist[node]:
            continue
        for neighbor in graph[node]:
            new_cost = current_cost + costs[neighbor]
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return dist, parent


print(dijkstra(graph, costs, "start", "goal"))
