from PIL import Image, ImageDraw
from graph import *
import random
import math

im = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
GRAY = (128, 128, 128, 255)


def draw_line(x0, y0, x1, y1, color=(0, 0, 0, 255), width=1):
    y0 = im.height - y0
    y1 = im.height - y1
    draw.line((x0, y0, x1, y1), fill=color, width=width)


def draw_point(x, y, radius=1, color=(0, 0, 0, 255)):
    y = im.height - y
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def draw_poly(array, color):
    converted = []
    for (x, y) in array:
        y = im.height - y
        converted.append((x, y))
    draw.polygon(converted, fill=color)


def cross_edge(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d
    ma = (dx - cx) * (ay - cy) - (dy - cy) * (ax - cx)
    mb = (bx - ax) * (ay - cy) - (by - ay) * (ax - cx)
    zz = (dy - cy) * (bx - ax) - (dx - cx) * (by - ay)
    if zz == 0.0:
        return ma == 0.0
    ua = ma / zz
    ub = mb / zz
    return ua >= 0.0 and ua < 1.0 and ub >= 0.0 and ub < 1.0


class MapDesc:

    def __init__(self):
        self.polygons = [
            [(0, 150), (150, 150), (150, 350), (0, 350)],
            [(100, 0), (250, 200), (600, 200), (600, 0)],
            [(100, 550), (250, 300), (600, 300), (600, 550)],
        ]
        self.control_points = [
            (180, 140),
            (180, 360),
            (240, 250),
            (470, 250),
            (65, 85),
            (65, 450),
        ]

        self.graph = Graph()
        self.build_graph()

    def build_graph(self):
        i = 0
        for x, y in self.control_points:
            node = Node(str(i))
            node.x, node.y = x, y
            self.graph.add_node(node)
            i += 1
        for nodeA in self.graph.nodes:
            for nodeB in self.graph.nodes:
                if nodeA == nodeB:
                    continue
                a = nodeA.x, nodeA.y
                b = nodeB.x, nodeB.y
                if self._has_direct_path(a, b):
                    self.graph.add_link(nodeA, nodeB)

    def draw(self):
        for poly in self.polygons:
            draw_poly(poly, RED)
        for (x, y) in self.control_points:
            draw_point(x, y, 5, GREEN)
        for link in self.graph.links:
            draw_line(link.a.x, link.a.y, link.b.x, link.b.y, color=(128, 128, 128, 128))

    def draw_path(self, points, color=BLUE):
        if len(points) == 0:
            return

        A = points[0]
        B = points[-1]
        draw_point(A[0], A[1], 5, BLUE)
        draw_point(B[0], B[1], 5, BLUE)
        for index in xrange(len(points) - 1):
            a = points[index]
            b = points[index + 1]
            draw_line(a[0], a[1], b[0], b[1], color, width=2)

    def _has_direct_path(self, a, b):
        for poly in self.polygons:
            for i, r in enumerate(poly):
                c = poly[i]
                d = poly[i + 1 if i < len(poly) - 1 else 0]
                if cross_edge(a, b, c, d):
                    return False
        return True

    def build_path(self, a, b):
        if self._has_direct_path(a, b):
            print 'has direct'
            return [a, b]

        def add_node_with_links(node):
            self.graph.add_node(node)
            for nodeA in self.graph.nodes:
                if nodeA == node:
                    continue
                if self._has_direct_path((node.x, node.y), (nodeA.x, nodeA.y)):
                    self.graph.add_link(node, nodeA)
        nodeA = Node('none')
        nodeA.x, nodeA.y = a
        nodeB = Node('none')
        nodeB.x, nodeB.y = b
        add_node_with_links(nodeA)
        add_node_with_links(nodeB)
        path = dijkstra(self.graph, nodeA, nodeB)
        self.graph.remove_node(nodeA)
        self.graph.remove_node(nodeB)
        points = []
        for node in path:
            points.append((node.x, node.y))
        return points

    def improve_path(self, points):
        iterations = 16

        def length(path):
            r = 0
            for i in xrange(len(points) - 1):
                a = points[i + 0]
                b = points[i + 1]
                x, y = b[0] - a[0], b[1] - a[1]
                r += math.sqrt(x * x + y * y)
            return r
        before = length(points)
        for x in xrange(iterations):
            for i in xrange(len(points) - 2):
                a = points[i + 0]
                b = points[i + 1]
                c = points[i + 2]

                p0 = b
                p1 = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)
                for j in xrange(iterations):
                    p = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                    if self._has_direct_path(a, p) and self._has_direct_path(c, p):
                        p0, p1 = p, p1
                    else:
                        p0, p1 = p0, p
                points[i + 1] = p0
        after = length(points)
        print 'before: {}\nafter:  {}\n'.format(before, after)
        return points


if __name__ == '__main__':

    map = MapDesc()
    map.draw()

    path = map.build_path((50, 70), (25, 450))
    # path = map.build_path((50, 70), (160, 250))
    map.draw_path(path, color=(128, 128, 255, 255))
    map.draw_path(map.improve_path(path))

    path = map.build_path((20, 20), (500, 220))
    map.draw_path(path, color=(128, 128, 255, 255))
    map.draw_path(map.improve_path(path))

    im.save('path.png', "PNG")
