class AVLTree(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.height = 0
            self.right = None
            self.left = None

        @property
        def is_leaf(self)->bool:
            return not self.left and not self.right

        def set_height(self):
            self.height = max(AVLTree._height(self.left), AVLTree._height(self.right)) + 1

        def rotate_left(self):
            new_root = self.right
            self.right = new_root.left
            new_root.left = self
            self.set_height()
            new_root.set_height()
            return new_root

        def rotate_right(self):
            new_root = self.left
            self.left = new_root.right
            new_root.right = self
            self.set_height()
            new_root.set_height()
            return new_root

        def __str__(self):
            return f'<{self.__class__.__name__}: {self.val}>'

        def __repr__(self):
            return str(self)

    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, root: Node, val) -> Node:
        if root is None:
            return self.Node(val)
        if val < root.val:
            root.left = self._insert(root.left, val)
        else:
            root.right = self._insert(root.right, val)
        root.set_height()
        return AVLTree._balance(root)

    @staticmethod
    def _balance(root: Node)->Node:
        if AVLTree._is_left_heavy(root):
            if AVLTree._balance_factor(root.left) > 0:
                root = root.rotate_right()
            else:
                root.left = root.left.rotate_left()
                root = root.rotate_right()
        elif AVLTree._is_right_heavy(root):
            if AVLTree._balance_factor(root.right) < 0:
                root = root.rotate_left()
            else:
                root.right = root.right.rotate_right()
                root = root.rotate_left()
        return root

    @staticmethod
    def _balance_factor(root: Node):
        return AVLTree._height(root.left) - AVLTree._height(root.right) if root else 0

    @staticmethod
    def _is_right_heavy(root: Node):
        return -1 > AVLTree._balance_factor(root)

    @staticmethod
    def _is_left_heavy(root: Node):
        return 1 < AVLTree._balance_factor(root)

    @staticmethod
    def _height(node: Node)->int:
        return -1 if node is None else node.height

    @property
    def _is_balanced(self)->bool:
        """Short and smart way"""
        if self.root.left and self.root.right:
            return abs(self.root.left.height - self.root.right.height) <= 1
        return (self.root.left or self.root.right).height <= 1

    @property
    def is_balanced(self)->bool:
        _, flag = AVLTree._is_balanced_(self.root)
        return flag

    @staticmethod
    def _is_balanced_(root: Node)->(int, bool):
        if root is None:
            return -1, True
        lh, lf = AVLTree._is_balanced_(root.left)
        rh, rf = AVLTree._is_balanced_(root.right)
        if not lf or not rf:
            return max(lh, rh) + 1, False
        return max(lh, rh) + 1, abs(lh - rh) <= 1

    def is_perfect(self)->bool:
        # Perfect Tree size is (2^(height + 1) - 1)
        if self.root is None:
            raise ValueError("Tree is empty")
        return 2 ** (self.root.height + 1) - 1 == self.size()

    def size(self):
        return AVLTree._size(self.root)

    @staticmethod
    def _size(root: Node)->int:
        if root is None:
            return 0
        return AVLTree._size(root.left) + AVLTree._size(root.right) + 1


tree = AVLTree()
tree.insert(10)
tree.insert(12)
tree.insert(11)
tree.insert(8)
tree.insert(13)
tree.insert(16)
tree.insert(12)
tree.insert(13)
tree.insert(9)
tree.insert(11)
tree.insert(17)
tree.insert(7)
tree.insert(8)
tree.insert(9)
tree.insert(10)

print(tree.is_perfect())
