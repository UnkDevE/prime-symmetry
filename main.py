#!/bin/python

from math import *

times_video_out = 0


# wraps x around an interval
def wrap(interval, x):
    if (x < interval[0]):
        x = interval[1] - (interval[0] - x) % (interval[1] - interval[0])
    else:
        x = interval[0] + (x - interval[0]) % (interval[1] - interval[0])
    return x


# the graph structure of a node connecting to itself
class SymGraph:
    # starts at 2x
    # angle takes in the slope of a line in radians and transforms it each time
    # slope func is the angle function
    # c func is the line positioning function takes in slope
    def __init__(self, slope_func, c_func, stop=1000,
                 n=0, angle=1.0, knots=[]):

        self.n = n
        self.angle = angle
        self.stop = stop
        # pointer to last graph
        self.knots = []
        self.knots += knots

        self.wrapper = lambda x: wrap((-1, 1), x)
        self.c_func = c_func

        # wrapped version of c func
        self.c_funcw = lambda x: self.wrapper(c_func(x))
        self.slope_func = slope_func
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
                    reflected_line = (-intersect + -knot[0],
                                      self.c_funcw(-intersect + -knot[0]))
                    if not (reflected_line in knot_points):
                        out_knot_points.append(
                            reflected_line)
                    if not (intersect, -reflected_line[1]) in knot_points:
                        out_knot_points.append((
                            -intersect,
                            self.c_funcw(-intersect)))

                    # omit knots from covered reflection
                    if not (reflected_line[0] < knot[0] < intersect) and (
                            reflected_line[1] < knot[1] < intersect):
                        out_knot_points.append(knot)

                else:
                    print("hitting knot point")
                    out_knot_points.append((
                        intersect,
                        self.c_funcw(intersect)))
        else:
            out_knot_points.append((intersect,
                                    self.c_funcw(intersect)))

            out_knot_points.append((-intersect,
                                    self.c_funcw(-intersect)))

        out_knot_points = list(set(out_knot_points))
        n = len(out_knot_points)

        if n in sieve:
            print("Knot creation successful prime number {} achieved".
                  format(str(n)))
        else:
            print("Failure at: {}".format(str(n)))

        return SymGraph(self.slope_func, self.c_func, stop=self.stop - 1, n=n,
                        angle=self.slope_func(intersect),
                        knots=out_knot_points)

    def to_list(self):
        xs = []
        while self.next is not None:
            xs.append(self)
            self = self.next

        return xs


# draw graphs with symmetry lines
def draw_symmetry(graph, funcstrs):
    global times_video_out
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

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
            plt.axline((k[1], 0), slope=k[0], color='g')
        # show n
        plt.xlabel("n " + str(g.n))

        # print title
        plt.title("y = ({})x + {}".format(funcstrs[0], funcstrs[1]))

    ani = animation.FuncAnimation(fig=fig, func=update,
                                  frames=10, interval=1000)

    ani.save("primegraph" + str(times_video_out) + ".mp4")


def main():
    last = None
    funcstrs = None
    while True:
        afuncstr = input(
            "give function for prime testing (where a is var for slope):")
        if afuncstr != "draw":
            cfuncstr = input(
                "give function for position (where a is position):")
            last = SymGraph(eval("lambda a: " + afuncstr),
                            eval("lambda a: " + cfuncstr),
                            stop=10)
            funcstrs = [afuncstr, cfuncstr]
        else:
            print("drawing")
            draw_symmetry(last.to_list(), funcstrs)


if __name__ == "__main__":
    main()
