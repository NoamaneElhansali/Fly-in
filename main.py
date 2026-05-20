import sys
from Parser.parsing import Parser
from graph.GraphBuilder import GraphBuilder, Graph
from algorithms.pathfinding import PathFinder
from simulation.simulation import Simulation
from visual.display import Display

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        # try:
        lines = f.readlines()
        data = Parser.model_validate(lines)
        # print(data)
        graph_b = GraphBuilder(data)
        build_graph = graph_b.build()
        path = PathFinder(build_graph)
        path.find_all_shortest_path()
        # path.find_all_shortest_path(
        #     "waypoint1", build_graph.end.name)
        # print()
        sim = Simulation(build_graph, path.format_paths())
        turns = sim.run()
        # print(turns)

        dis = Display(build_graph.zones, data.connections, turns,
                      build_graph.nb_drones, build_graph.start,
                      build_graph.end)
        dis.test()
        # except Exception as e:
        #     print(f"Error: {e}")
        # for x in graph_b.build().zones.values():
        #     print(x.max_drones, x.neighbors)
        # print(graph_b.build().zones)
