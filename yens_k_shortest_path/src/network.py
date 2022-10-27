__author__ = 'Simanta Barman'
__email__ = 'barma017@umn.edu'

from copy import copy, deepcopy
from typing import Iterable, Iterator, Union
from constants import Node, Link


class Network:
    def __init__(self, weights: dict, links: Iterable = None):

        self.links: set[Link] = set(links) if links else set(weights)
        self.nodes: set[Node] = {node for link in links for node in link}
        self.weights: dict[Link, float] = weights
        self._sp = None

    @property
    def sp(self):
        """Returns the shortest path object created for the network."""

        if not self._sp:
            from shortest_paths import ShortestPath
            self._sp = ShortestPath(self)

        return self._sp

    def __star(self, node: Node, method: str) -> Iterator:

        index = 0 if method == 'forward' else 1

        for link in self.links.copy():
            if node == link[index]:
                yield link

    def forward_star(self, node: Node) -> Iterator:
        """Returns the forward star of the node"""
        return self.__star(node=node, method="forward")

    def reverse_star(self, node: Node) -> Iterator:
        """Returns the reverse star of the node"""
        return self.__star(node=node, method="reverse")

    def copy(self):
        """Returns a shallow copy of the graph object."""
        return copy(self)

    def add_node(self, node: Node):
        """Procedure: Adds the node to the graph."""
        self.nodes.add(node)

    def add_edge(self, edge: Link, weight: Union[float, None] = None):
        """Procedure: Adds edge and edge weight to the graph."""
        self.links.add(edge)
        if weight is not None:
            self.weights[edge] = weight
        for node in edge:
            self.add_node(node)

    def remove_edge(self, edge: Link):
        """
        Procedure: Removes the given edge from the graph.
        Also removes the weight associated with that edge.
        """
        self.links.remove(edge)
        del self.weights[edge]

    def remove_node(self, node: Node):
        """
        Procedure: Removes the given node from graph.
        This also removes all links created with the node."""
        self.nodes.remove(node)

        for i, j in self.forward_star(node):
            self.remove_edge((i, j))

        for h, i in self.reverse_star(node):
            self.remove_edge((h, i))

