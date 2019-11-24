class WeightedGraph:
    class Node:
        def __init__(self, label: str):
            self.label = label
            self._edges = set()

        def add_edge(self, to, weight: int):
            self._edges.add(WeightedGraph.Edge(self, to, weight))

        @property
        def edges(self):
            return self._edges

        def __str__(self):
            return f'{self.label}'

    class Edge:
        def __init__(self, fr, to, weight: int):
            self.fr = fr
            self.to = to
            self.weight = weight

        def __str__(self):
            return f'{self.fr}{self.to}({self.weight})'

    def __init__(self):
        self.nodes = {}

    def add_node(self, label: str):
        self.nodes.setdefault(label, self.Node(label))

    def add_edge(self, fr: str, to: str, weight: int):
        from_node = self.nodes.get(fr)
        to_node = self.nodes.get(to)
        if not from_node or not to_node:
            raise ValueError(f"Invalid parameters: {fr}, {to}")
        from_node.add_edge(to_node, weight)
        to_node.add_edge(from_node, weight)

    def iterate(self):
        for key, val in self.nodes.items():
            yield f'{key}: [ {", ".join(map(str, val.edges))} ]'

    def __str__(self):
        return "\n".join(self.iterate())

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    g = WeightedGraph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_edge("A", "B", 4)
    g.add_edge("B", "C", 8)
    g.add_edge("C", "A", 2)
    print(g)
