#!/bin/python

from sympy import seive
import math


# the graph structure of a node connecting to itself
class SymGraph:
    def __init__(self, n, angle, previous):
        self.n = n
        self.angle = angle
        # pointer to last graph
        self.previous = previous

    # find symmetry of graph and generate split on next graph
    # angle is clockwise at centre point 0 starts at x=0
    def symmetrize(self, angle):
        # place holder
        next = 0
        return SymGraph(next, angle, self)

    def __next__(self):
        return self.previous


# tests the symmetries of angles and checks for primes
def test_symmetry(range, step):
    graph = SymGraph(1, 0, None)

    for i in range(0, step):
        new_node = graph.symmetrize(i)
        if new_node.n in seive:
            graph = new_node

    return graph


# draw graphs with symmetry lines
def draw_symmetry(graph):
    import matplotlib.pyplot as plt
    import igraph as ig

    fig, ax = plt.subplots()
    for g in graph:
        # create symmetry line
        slope = math.tan(g.angle)
        plt.axline(0, slope=slope)

        # create graph for drawing
        plot_graph = ig.Graph(edges=[[0, n] for n in range(graph.n)])
        ig.plot(plot_graph)

        # add x and y labels for good measure
        plt.xlabel("angle=", str(g.angle))
        plt.xlabel("n", str(g.n))

        # save and clear
        plt.savefig("graph " + str(graph.n) + ".jpg")
        fig.clf()


def main():
    pass


if __name__ == "__main__":
    main()
