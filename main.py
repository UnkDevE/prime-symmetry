#!/bin/python

from math import *

times_video_out = 0


# the graph structure of a node connecting to itself
class SymGraph:
    # 1 in radians is 45 deg
    # angle takes in the slope of a line in radians and transforms it each time
    def __init__(self, angle_func, stop=1000,
                 n=1, angle=1.0, knots=[]):
        self.n = n
        self.angle = angle
        self.stop = stop
        # pointer to last graph
        self.knots = []
        self.knots += knots
        self.angle_func = angle_func
        self.next = None

        # circle is not needed but is visually shown in diagrams
        # now split into two
        if stop != 0:
            self.next = self.symmetrize(angle)

    # find symmetry of graph and generate split on next graph
    # angle is clockwise at centre point 0 starts at x=0
    def symmetrize(self, intersect):
        from sympy import sieve
        # find intersect from circle using lines angle
        # calculate knots via previous lines
        knot_points = [a for a in self.knots]
        out_knot_points = []

        # mirror the lines using intersect line
        # this must be called once to get going
        if knot_points != []:
            for knot in knot_points:
                # intersect line not intersect knots
                if intersect != knot:
                    reflected_line = (-intersect + -knot)
                    if not (reflected_line in knot_points):
                        out_knot_points.append(reflected_line)
                    if not (intersect in knot_points):
                        out_knot_points.append(-intersect)

                    # remove knots from covered reflection
                    if not (reflected_line < knot < intersect):
                        out_knot_points.append(knot)

                else:
                    print("hitting knot point")
                    out_knot_points.append(intersect)
        else:
            out_knot_points.append(-intersect)
            out_knot_points.append(intersect)

        out_knot_points = list(set(out_knot_points))
        n = len(out_knot_points)

        if n in sieve:
            print("Knot creation successful prime number {} achieved".
                  format(str(n)))
        else:
            print("Failure at: {}".format(str(n)))

        return SymGraph(self.angle_func, stop=self.stop - 1, n=n,
                        angle=self.angle_func(intersect),
                        knots=out_knot_points)

    def to_list(self):
        xs = []
        while self.next is not None:
            xs.append(self)
            self = self.next

        return xs


# draw graphs with symmetry lines
def draw_symmetry(graph):
    global times_video_out
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt
    import math

    times_video_out += 1

    # create graph for drawing
    fig, _ = plt.subplots()
    circle1 = plt.Circle((0, 0), 1.0, color='r', fill=False)
    plt.gca().add_patch(circle1)

    plt.ion()
    def update(frame):
        g = graph[frame]
        # create symmetry line
        plt.axline((0, 0), slope=g.angle, color='b')

        # create knot lines
        for k in g.knots:
            plt.axline((0, 0), slope=k, color='g')
        # show n
        plt.xlabel("n " + str(g.n))

    ani = animation.FuncAnimation(fig=fig, func=update,
                                  frames=10, interval=1000)

    ani.save("primegraph" + str(times_video_out) + ".mp4")


def main():
    last = None
    while True:
        funcstr = input("give function for prime testing (where a is var):")
        if funcstr != "draw":
            last = SymGraph(eval("lambda a: " + funcstr), stop=10)
        else:
            print("drawing")
            draw_symmetry(last.to_list())


if __name__ == "__main__":
    main()
