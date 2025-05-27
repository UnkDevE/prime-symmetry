#!/bin/python

from math import *
# the graph structure of a node connecting to itself
class SymGraph:
    # 1 in radians is 45 deg
    # angle takes in the slope of a line in radians and transforms it each time
    def __init__(self, angle_func, stop = 1000, n = 2, angle = 1.0, knots = []):
        self.n = n
        self.angle = angle
        self.stop = stop
        # pointer to last graph
        self.knots = []
        self.knots += knots
        self.angle_func = angle_func

        # circle is not needed but is visually shown in diagrams
        # now split into two
        if stop != 0:
            self.symmetrize(angle)

    # find symmetry of graph and generate split on next graph
    # angle is clockwise at centre point 0 starts at x=0
    def symmetrize(self, intersect):
        from sympy import sieve 
        # find intersect from circle using lines angle
        # calculate knots via previous lines
        knot_points = [a for a in self.knots]
        out_knot_points = knot_points

        # mirror the lines using intersect line
        # this must be called once to get going
        if knot_points != []:
            for knot in knot_points:
                # intersect line not intersect knots
                if intersect != knot:
                    reflected_line = (-intersect+ -knot)
                    if not(reflected_line in knot_points):
                        out_knot_points.append(-intersect+ -knot)
                    if not(intersect in knot_points):
                        out_knot_points.append(intersect)
                else: 
                    print("hitting knot point")
        else:
            out_knot_points.append(intersect)

        n = len(out_knot_points) 

        if n in sieve:
            print("Knot creation successful prime number {} achieved".format(str(n)))
        else:
            print("Failure at: {}".format(str(n)))

        return SymGraph(self.angle_func, stop = self.stop-1, n = n, 
                        angle=self.angle_func(intersect), 
                        knots=out_knot_points)

# draw graphs with symmetry lines
def draw_symmetry(graph):
    import matplotlib.pyplot as plt
    import igraph as ig
    import math

    fig, _ = plt.subplots()
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
    while True:
        funcstr = input("give function for prime testing (where a is var):")
        SymGraph(eval("lambda a: "+funcstr), stop=10)

if __name__ == "__main__":
    main()
