import queue


class Graph:
    class Node:
        def __init__(self, label: str):
            self.label = label

        def __str__(self):
            return f'{self.label}'

    def __init__(self):
        self.nodes = {}
        self.adjacency_map = {}

    def add_node(self, label: str):
        node = self.Node(label)
        self.nodes.setdefault(label, node)
        self.adjacency_map.setdefault(node, set())

    def add_edge(self, fr: str, to: str):
        from_node = self.nodes.get(fr)
        to_node = self.nodes.get(to)
        if not from_node or not to_node:
            raise ValueError(f"Invalid parameters: {fr}, {to}")
        self.adjacency_map.get(from_node).add(to_node)

    def remove_node(self, label: str):
        node = self.nodes.get(label)

        if not node:
            return

        del self.adjacency_map[node]
        del self.nodes[label]

        for i in self.adjacency_map.values():
            if node in i:
                i.remove(node)

    def remove_edge(self, fr: str, to: str):
        from_node = self.nodes.get(fr)
        to_node = self.nodes.get(to)
        if not from_node or not to_node:
            return
        self.adjacency_map.get(from_node).remove(to_node)

    def iterate(self):
        for key, val in self.adjacency_map.items():
            yield f'{key}: [{", ".join(map(str, val))}]'

    def __str__(self):
        return "\n".join(self.iterate())

    def __repr__(self):
        return str(self)

    def traverse(self, root: str):
        """
        Call the method that traverses recursively depth first
        :param root:
        :return:
        """
        node = self.nodes.get(root)
        if node is None:
            raise ValueError(f"Node {root} does not exist")
        self._traverse_recursively(node, set())

    def _traverse_recursively(self, root: Node, visited: set):
        """
        Traverse the Graph recursively depth first
        :param root:
        :param visited:
        :return:
        """
        if root is None:
            return
        print(root)
        visited.add(root)
        next_nodes = self.adjacency_map.get(root)
        for node in next_nodes:
            if node not in visited:
                self._traverse_recursively(node, visited)

    def traverse_iterative(self, label: str):
        """
        Traverse Graph iteratively depth first
        :param label:
        :return:
        """
        root = self.nodes.get(label)
        if root is None:
            raise ValueError(f"Node {label} does not exist")
        stack = queue.LifoQueue()
        stack.put(root)
        visited = set()
        while not stack.empty():
            current = stack.get()
            if current in visited:
                continue
            for i in self.adjacency_map.get(current):
                stack.put(i)
            print(current)
            visited.add(current)

    def traverse_iterative_breadth(self, label: str):
        """
        Traverse Graph iteratively breadth first
        :param label:
        :return:
        """
        root = self.nodes.get(label)
        if root is None:
            raise ValueError(f"Node {label} does not exist")
        stack = queue.Queue()
        stack.put(root)
        visited = set()
        while not stack.empty():
            current = stack.get()
            if current in visited:
                continue
            for i in self.adjacency_map.get(current):
                stack.put(i)
            print(current)
            visited.add(current)

    def topological_sort(self) -> list:
        stack = queue.LifoQueue()
        visited = set()
        for node in self.nodes.values():
            self._topological_sort(node, visited, stack)
        sorted_nodes = []
        while not stack.empty():
            sorted_nodes.append(stack.get().label)
        return sorted_nodes

    def _topological_sort(self, root: Node, visited: set, stack: queue.LifoQueue):
        if root in visited:
            return
        visited.add(root)
        for node in self.adjacency_map[root]:
            self._topological_sort(node, visited, stack)
        stack.put(root)

    def has_cycle(self) -> bool:
        nodes = {node for node in self.nodes.values()}
        visiting = set()
        visited = set()
        while len(nodes) != 0:
            node = list(nodes)[0]
            if self._has_cycle(node, nodes, visiting, visited):
                return True
        return False

    def _has_cycle(self, node: Node, nodes: set, visiting: set, visited: set) -> bool:
        nodes.remove(node)
        visiting.add(node)
        for neighbour in self.adjacency_map.get(node):
            if neighbour in visited:
                continue
            if neighbour in visiting:
                return True
            if self._has_cycle(neighbour, nodes, visiting, visited):
                return True
        visiting.remove(node)
        visited.add(node)
        return False


if __name__ == "__main__":
    graph = Graph()
    graph.add_node("X")
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("P")

    graph.add_edge("X", "B")
    graph.add_edge("X", "A")
    graph.add_edge("A", "P")
    graph.add_edge("B", "P")
    graph.add_edge("P", "X")

    print(graph)
    print(graph.has_cycle())

