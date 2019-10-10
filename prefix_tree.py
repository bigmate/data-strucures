class Trie(object):
    def __init__(self):
        self.root = self.Node(None)

    class Node(object):
        def __init__(self, char, is_end=False):
            self.char = char
            self.children = {}
            self.is_end = is_end

        def has_child(self, char: str)->bool:
            return char in self.children

        @property
        def has_any(self):
            return len(self.children) != 0

        def add_child(self, char: str):
            self.children[char] = self.__class__(char)

        def get_child(self, char: str):
            return self.children.get(char)

        def get_children(self)->[]:
            return self.children.values()

        def remove_child(self, char):
            if not self.has_child(char):
                raise ValueError(f'Child `{char}` does not exist')
            del self.children[char]

        def __str__(self):
            return f'<Node: {self.char}>'

        def __repr__(self):
            return str(self)

    def insert(self, word):
        self._insert(self.root, word)

    @classmethod
    def _insert(cls, root: Node, word: str):
        char = word[0]
        if not root.has_child(char):
            root.add_child(char)
        if len(word) == 1:
            root.get_child(char).is_end = True
            return
        cls._insert(root.get_child(char), word[1:])

    def remove(self, word):
        if word is None or word == '':
            return
        self._remove(self.root, word)

    @classmethod
    def _remove(cls, root: Node, word: str):
        char = word[0]
        child = root.get_child(char)
        if child is None:
            return
        if len(word) == 1:
            child.is_end = False
        else:
            cls._remove(child, word[1:])
        if not child.has_any and not child.is_end:
            root.remove_child(char)

    def count_words(self)->int:
        return sum([1 for node in self._traverse_pre(self.root) if node.is_end])

    def longest_common_prefix(self, prefix: str = ''):
        longest_prefix = ['']
        self.lcp(self.root, longest_prefix, prefix)
        return longest_prefix[0]

    @classmethod
    def lcp(cls, root: Node, longest_prefix: [str], prefix: str = ''):
        if root.is_end and root.has_any and len(prefix) > len(longest_prefix[0]):
            longest_prefix[0] = prefix
        for node in root.get_children():
            cls.lcp(node, longest_prefix, prefix + node.char)

    @classmethod
    def _contains(cls, root: Node, word: str)->bool:
        char = word[0]
        if not root.has_child(char):
            return False
        if len(word) == 1:
            return root.get_child(char).is_end
        return cls._contains(root.get_child(char), word[1:])

    def autocomplete(self, prefix: str)->[str]:
        root = self.chase(prefix)
        words = []
        if root is None:
            return words
        self._autocomplete(root, prefix, words)
        return words

    @classmethod
    def _autocomplete(cls, root: Node, prefix: str, words: [str]):
        if root.is_end:
            words.append(prefix)
        for node in root.get_children():
            cls._autocomplete(node, prefix + node.char, words)

    def chase(self, prefix):
        return self._chase(self.root, prefix)

    @classmethod
    def _chase(cls, root: Node, prefix: str, index: int = 0):
        if root is None or prefix is None:
            return None
        if len(prefix) == index:
            return root
        return cls._chase(root.get_child(prefix[index]), prefix, index + 1)

    def traverse(self, order: str):
        name = f'_traverse_{order}'
        if not hasattr(self, name):
            raise ValueError(f'Invalid order: {order}')
        for child in self.root.get_children():
            yield from getattr(self, name)(child)

    @classmethod
    def _traverse_pre(cls, root: Node):
        yield root
        for child in root.get_children():
            yield from cls._traverse_pre(child)

    @classmethod
    def _traverse_post(cls, root: Node):
        for child in root.get_children():
            yield from cls._traverse_pre(child)
        yield root

    def __contains__(self, word)->bool:
        if len(word) == 0 or word is None:
            return False
        return self._contains(self.root, word)


