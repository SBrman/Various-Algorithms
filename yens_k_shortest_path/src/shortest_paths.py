#! python3

__author__ = "Simanta Barman"
__email__ = "barma017@umn.edu"


import logging
from typing import Union
from network import Network
from constants import Node, Link

logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s -- %(message)s')
logger = logging.getLogger("k-shortest paths")

INF = float('inf')


class PathNotFoundException(KeyError):
    def __init__(self, message=' '):
        message = f'Path to {message} not found.'
        super().__init__(message)


class ShortestPath:
    def __init__(self, graph):
        self.G = graph
        self._cached_one_to_all_sps = {}
        self._ksp_original_weights = {}
        self.travel_time_cache: dict[Node, dict[Node, float]] = {}

    def travel_time(self, r: Node, s: Node) -> float:
        """Returns the shortest paths travel time for the OD pair."""

        if (r, s) not in self.travel_time_cache:
            self.travel_time_cache.setdefault(r, {})
            labels, _ = self.dijkstra_sps(source=r)
            for ss, label in labels.items():
                self.travel_time_cache[r][ss] = label

        return self.travel_time_cache[r][s]

    def dijkstra_sps(self, source, weights=None) -> tuple[dict, dict]:
        """
        Returns the labels and backnodes. Finds one source to all nodes shortest paths using dijkstra's algorithm.
        """
        if not weights:
            weights = self.G.weights

        labels = {node: INF for node in self.G.nodes}
        labels[source] = 0

        backnodes = {node: -1 for node in self.G.nodes}

        finalized = set()

        while True:
            min_label, i = min((label, node) for node, label in labels.items() if node not in finalized)
            finalized.add(i)

            for (i, j) in self.G.forward_star(i):
                new_label_j = min(labels[j], labels[i] + weights[(i, j)])

                if new_label_j < labels[j]:
                    labels[j] = new_label_j
                    backnodes[j] = i

            if len(finalized) == len(self.G.nodes):
                break
        
        return labels, backnodes

    @staticmethod
    def _shortest_paths_from_backnode(backnodes: dict) -> dict[Union[int, str], list]:
        """Returns the shortest path from the backnodes."""
        shortest_paths = {}
        for node, back_node in backnodes.items():
            last_node = node
            shortest_path = [node]
            while back_node != -1:
                shortest_path.append(back_node)
                node = back_node
                back_node = backnodes[node]

            if node != last_node and len(shortest_path) > 1:
                shortest_paths[last_node] = shortest_path[::-1]

        return shortest_paths

    def one_to_all_shortest_paths(self, source, weights) -> dict:
        """Returns one to all shortest path using dijkstras algorithm."""

        if source not in self._cached_one_to_all_sps or weights != self.G.weights:
            labels, backnodes = self.dijkstra_sps(source=source, weights=weights)
            self._cached_one_to_all_sps[source] = self._shortest_paths_from_backnode(backnodes)

        return self._cached_one_to_all_sps[source]

    def one_to_one_shortest_path(self, source, destination, weights) -> list:
        """Returns the one to one shortest path."""

        try:
            return self.one_to_all_shortest_paths(source, weights)[destination]
        except KeyError as e:
            raise PathNotFoundException(str(e))

    @staticmethod
    def path_cost(path_of_links, weights):
        """Returns the path cost."""
        return sum(weights[link] for link in path_of_links)

    def minimum_length_path(self, paths, weights):
        """Returns the minimum length path."""
        new_paths_in_links = [list(zip(path[:-1], path[1:])) for path in paths]
        min_cost, min_path = min((self.path_cost(path, weights), path) for path in new_paths_in_links)
        return list(list(zip(*min_path))[0]) + [min_path[-1][-1]]

    def restore_graph(self):
        """Procedure: restores the graph to original state."""
        for link, weight in self._ksp_original_weights.items():
            self.G.add_edge(link, weight)
        self._cached_one_to_all_sps = {}
        return self._ksp_original_weights

    def k_shortest_paths(self, source, destination, k, weights):
        """Returns the k-shortest paths from source node to the destination node."""

        self._ksp_original_weights = weights.copy()
        weights = weights.copy()

        if source == destination:
            return [0], [[source]]

        shortest_paths = [self.one_to_one_shortest_path(source, destination, weights)]
        potential_shortest_paths = []

        for kk in range(1, k):
            for i in range(len(shortest_paths[kk - 1]) - 1):
                spur_node = shortest_paths[kk - 1][i]
                root_path = shortest_paths[kk - 1][:i + 1]

                for spath in shortest_paths:
                    if root_path == spath[:i + 1]:
                        edge_to_remove = spath[i], spath[i + 1]
                        if edge_to_remove in self.G.links:
                            self.G.remove_edge(edge_to_remove)
                        # weights[edge_to_remove] = INF

                for node in root_path[:-1]:
                    if node in self.G.nodes:
                        self.G.remove_node(node)

                try:
                    spur_path = self.one_to_one_shortest_path(source=spur_node, destination=destination,
                                                              weights=weights)
                except PathNotFoundException as e:
                    logger.debug(f"Spur {str(e)} with {root_path = }. Continuing...")
                    continue

                total_shortest_path = root_path + spur_path[1:]

                if total_shortest_path not in potential_shortest_paths:
                    potential_shortest_paths.append(total_shortest_path)

                weights = self.restore_graph()

            if potential_shortest_paths:
                new_shortest_path = self.minimum_length_path(paths=potential_shortest_paths, weights=weights)
                nsp_index = potential_shortest_paths.index(new_shortest_path)
                potential_shortest_paths.pop(nsp_index)
            else:
                break

            shortest_paths.append(new_shortest_path)

        self.restore_graph()
        return shortest_paths


if __name__ == "__main__":
    # A = {(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4)}
    # W = {(1, 2): 1, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 1}

    A = {('C', 'D'), ('C', 'E'), ('E', 'D'), ('E', 'F'), ('E', 'G'), ('D', 'F'), ('F', 'G'), ('F', 'H'), ('G', 'H')}
    W = {('C', 'D'): 3, ('C', 'E'): 2, ('E', 'D'): 1, ('E', 'F'): 2, ('E', 'G'): 3, ('D', 'F'): 4,
         ('F', 'G'): 2, ('F', 'H'): 1, ('G', 'H'): 2}

    G = Network(links=A, weights=W.copy())
    # sp = ShortestPath(G)
    print(G.sp.k_shortest_paths(source='C', destination='H', k=4, weights=W))
    spp = G.sp.one_to_one_shortest_path('C', 'H', W)
    print(spp)
