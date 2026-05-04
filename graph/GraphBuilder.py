from .graph import Graph


class GraphBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        graph = Graph(self.data)
        graph.set_start(self.data.start_hub)
        graph.set_end(self.data.end_hub)
        graph.add_zone(self.data.start_hub)
        graph.add_zone(self.data.end_hub)
        for x in self.data.hubs:
            graph.add_zone(x)
        for x in self.data.connections:
            graph.add_connection(x)
        return graph
