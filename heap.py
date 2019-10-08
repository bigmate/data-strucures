class Heap(object):
    def __init__(self, size: int, is_max: bool = True):
        self._items = [None] * size
        self.size = 0
        self.is_max = is_max

    def insert(self, val):
        if self.is_full:
            raise ValueError('Tree overflowed')
        self._items[self.size] = val
        self.size += 1
        if self.is_max:
            self.bubble_up()
        else:
            self.bubble_down()

    def remove(self):
        if self.is_empty:
            raise IndexError("Empty heap")

        root = self._items[0]
        self.size -= 1
        self._items[0] = self._items[self.size]
        p = 0
        while p <= self.size and not self.valid_parent(p):
            i = self.next_child_i(p)
            self.swap(i, p)
            p = i
        return root

    def valid_parent(self, p: int)->bool:
        if not self.has_left_child(p):
            return True
        if self.is_max:
            if not self.has_right_child(p):
                return self._items[p] >= self.left_child(p)
            return self._items[p] >= self.left_child(p) and self._items[p] >= self.right_child(p)
        if not self.has_right_child(p):
            return self._items[p] < self.left_child(p)
        return self._items[p] < self.left_child(p) and self._items[p] < self.right_child(p)

    def bubble_up(self):
        index = self.size - 1
        while index > 0 and self._items[index] > self._items[Heap.parent(index)]:
            self.swap(index, Heap.parent(index))
            index = Heap.parent(index)

    def bubble_down(self):
        index = self.size - 1
        while index > 0 and self._items[index] < self._items[Heap.parent(index)]:
            self.swap(index, Heap.parent(index))
            index = Heap.parent(index)

    def left_child(self, p):
        return self._items[self.left_i(p)]

    def right_child(self, p):
        return self._items[self.right_i(p)]

    def next_child_i(self, p: int)->int:
        if not self.has_left_child(p):
            return p
        if not self.has_right_child(p):
            return self.left_i(p)
        if self.is_max:
            return self.left_i(p) if self.left_child(p) > self.right_child(p) else self.right_i(p)
        return self.left_i(p) if self.left_child(p) < self.right_child(p) else self.right_i(p)

    def has_left_child(self, p: int)->bool:
        return self.left_i(p) < self.size

    def has_right_child(self, p: int)->bool:
        return self.right_i(p) < self.size

    @staticmethod
    def left_i(p: int)->int:
        return 2*p + 1

    @staticmethod
    def right_i(p: int) -> int:
        return 2 * p + 2

    @staticmethod
    def parent(index: int)->int:
        return (index - 1)//2

    @property
    def is_full(self):
        return self.size == len(self._items)

    @property
    def is_empty(self):
        return self.size == 0

    def swap(self, i, p):
        self._items[i], self._items[p] = self._items[p], self._items[i]

    def __str__(self):
        return f'<{self.__class__.__name__}: {str(self._items)}>'

    def __repr__(self):
        return str(self)


# heap = Heap(6, is_max=False)
# 
# heap.insert(12)
# heap.insert(13)
# heap.insert(19)
# heap.insert(18)
# heap.insert(17)
# heap.insert(11)
# 
# for _ in range(6):
#     print(heap.remove())
