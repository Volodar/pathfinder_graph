
INF = 10E+15


class Node:

    def __init__(self, name=''):
        self.name = name
        self.x = 0
        self.y = 0
        self.links = []
        self.weight = 0

    def __repr__(self):
        return '{} [{}]'.format(self.name, self.weight)


class Link:

    def __init__(self):
        self.a = None
        self.b = None
        self.weight = 0

    def compute_weight(self):
        self.weight = self.a.x * self.a.x + self.b.x * self.b.x


class Graph:

    def __init__(self):
        self.nodes = []
        self.links = []

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        for link in node.links:
            nodeB = link.a if link.a != node else link.b
            del nodeB.links[nodeB.links.index(link)]
            del self.links[self.links.index(link)]

    def add_link(self, nodeA, nodeB):
        link = Link()
        link.a = nodeA
        link.b = nodeB

        nodeA.links.append(link)
        nodeB.links.append(link)

        link.compute_weight()
        self.links.append(link)

    def find_node_by_point(self, x, y):
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node
        return None

    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None


def dijkstra(graph, nodeA, nodeB):
    for node in graph.nodes:
        node.weight = INF
        node.visit = False

    nodeA.weight = 0

    def wave(node):
        node.visit = True
        for link in node.links:
            weight = node.weight + link.weight
            neighbor = link.a if link.a != node else link.b
            if not neighbor.visit and neighbor.weight > weight:
                neighbor.weight = weight
            if not neighbor.visit:
                wave(neighbor)
    wave(nodeA)

    node = nodeB
    path = []
    while True:
        path.append(node)
        if node == nodeA:
            break

        min_weight = INF
        next = None
        for i, link in enumerate(node.links):
            neighbor = link.a if link.a != node else link.b
            if min_weight > neighbor.weight:
                min_weight = neighbor.weight
                next = neighbor
        node = next
    path.reverse()
    return path


if __name__ == '__main__':
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    a.x, a.y = 100, 100
    b.x, b.y = 200, 100
    c.x, c.y = 150, 200
    d.x, d.y = 200, 300
    graph = Graph()
    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)
    graph.add_node(d)

    graph.add_link(a, c)
    # graph.add_link(a, b)
    graph.add_link(b, c)
    graph.add_link(b, d)
    graph.add_link(c, d)

    # for nodeA in graph.nodes:
    #     for nodeB in graph.nodes:
    #         if nodeA == nodeB:
    #             continue
    #         graph.add_link(nodeA, nodeB)

    path = dijkstra(graph, a, d)
    print path
