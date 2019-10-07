import queue


class BST(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.right = None
            self.left = None

        @property
        def is_leaf(self)->bool:
            return not self.left and not self.right

        def __ge__(self, other):
            return self.val >= other.val

        def __le__(self, other):
            return self.val <= other.val

        def __lt__(self, other):
            return self.val < other.val

        def __gt__(self, other):
            return self.val > other.val

        def __eq__(self, other):
            return self.val == other.val

        def __str__(self):
            return f'<{self.__class__.__name__}: {self.val}>'

        def __repr__(self):
            return str(self)

        def __xor__(self, other):
            return self.val != other.val

    def __init__(self):
        self.root = None

    def insert(self, val):
        node = self.Node(val)
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)

    def _insert(self, root: Node, node: Node):
        if root.left is None and root > node:
            root.left = node
        elif root.right is None and root <= node:
            root.right = node
        elif root.left is not None and root > node:
            self._insert(root.left, node)
        elif root.right is not None and root <= node:
            self._insert(root.right, node)

    def exist(self, val)->bool:
        return bool(BST._get_node(self.root, self.Node(val)))

    @staticmethod
    def _get_node(root: Node, node: Node):
        if root is None:
            return
        elif root == node:
            return root
        elif root > node:
            return BST._get_node(root.left, node)
        elif root < node:
            return BST._get_node(root.right, node)

    def traverse(self, order: str):
        if not hasattr(self, f'_{order}'):
            raise ValueError(f'Unexpected argument {order}')
        return getattr(self, f'_{order}')(self.root)

    @staticmethod
    def _pre_order(root: Node):
        stack = queue.LifoQueue()
        stack.put(root)
        while not stack.empty():
            node = stack.get()
            yield node
            if node.right is not None:
                stack.put(node.right)
            if node.left is not None:
                stack.put(node.left)

    @staticmethod
    def _post_order(root: Node):
        stack = queue.LifoQueue()
        stack.put(root)

        while not stack.empty():
            node = stack.get()
            yield node
            if node.left is not None:
                stack.put(node.left)
            if node.right is not None:
                stack.put(node.right)

    @staticmethod
    def _in_order(root: Node):
        stack = queue.LifoQueue()
        stack.put(root)
        node = root
        while not stack.empty():
            if node is not None:
                stack.put(node)
                node = node.left
            else:
                node = stack.get()
                yield node
                node = node.right

    @staticmethod
    def _level_order(root: Node):
        q = list([root, None])

        while True:
            node = q.pop(0)

            if node is None and len(q) and q[0] is None:
                break
            if node is not None:
                yield node
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            else:
                q.append(None)

    def height(self)->int:
        return BST._height(self.root)

    @staticmethod
    def _height(root: Node)->int:
        if root is None:
            return -1
        return 1 + max(BST._height(root.left), BST._height(root.right))

    def min(self):
        if self.root is None:
            raise ValueError('Tree have no nodes')
        return BST._min(self.root)

    @staticmethod
    def _min(root: Node):
        if root.left is None:
            return root.val
        return BST._min(root.left)

    def __eq__(self, other):
        return BST._eq(self.root, other.root)

    @staticmethod
    def _eq(one: Node, other: Node):
        if one is None and other is None:
            return True
        elif one is not None and other is not None:
            return one == other and BST._eq(one.left, other.left) and BST._eq(one.right, other.right)
        return False

    def is_bst(self):
        return BST._is_bst(self.root, float('-inf'), float('+inf'))

    @staticmethod
    def _is_bst(root: Node, lower, upper):
        if root is None:
            return True
        if root.val < lower or root.val > upper:
            return False
        return BST._is_bst(root.left, lower, root.val) and BST._is_bst(root.right, root.val, upper)

    def nodes_at(self, k):
        return BST._nodes_at_distance(self.root, k)

    @staticmethod
    def _nodes_at_distance(root: Node, k: int):
        if root is None:
            return
        if k == 0:
            yield root.val
        yield from BST._nodes_at_distance(root.left, k - 1)
        yield from BST._nodes_at_distance(root.right, k - 1)

    def size(self):
        return BST._size(self.root)

    @staticmethod
    def _size(root: Node, n: int = 0)->int:
        if root is None:
            return 0
        return 1 + BST._size(root.left, n + 1) + BST._size(root.right, n + 1)

    def count_leaves(self):
        return BST._count_leaves(self.root)

    @staticmethod
    def _count_leaves(root: Node)->int:
        if root is None:
            return 0
        elif root.is_leaf:
            return 1
        return BST._count_leaves(root.left) + BST._count_leaves(root.right)

    def max(self):
        return BST._max(self.root)

    @staticmethod
    def _max(root: Node)->Node:
        if root is None:
            raise ValueError('Tree have no nodes')
        elif root.right is None:
            return root
        return BST._max(root.right)

    def are_siblings(self, a, b):
        return BST._are_siblings(self.root, a, b)

    @staticmethod
    def _are_siblings(root: Node, a, b)->bool:
        if root.left is None or root.right is None:
            return False
        if (
                root.left.val == a and root.right.val == b or
                root.left.val == b and root.right.val == a
        ):
            return True
        return BST._are_siblings(root.left, a, b) or BST._are_siblings(root.right, a, b)

    @staticmethod
    def _bc(root: Node)->int:
        if root is None:
            return 0
        if root.left and not root.right or root.right and not root.left:
            return 1
        return 2


# tree = BST()
# tree.insert(10)
# tree.insert(12)
# tree.insert(11)
# tree.insert(8)
# tree.insert(13)
# tree.insert(16)
# tree.insert(12)
# tree.insert(13)
# tree.insert(9)



