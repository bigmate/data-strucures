class Trie(object):

    def __init__(self):
        self.root = self.Node(None)

    class Node(object):
        def __init__(self, char, is_end=False):
            self.char = char
            self.children = [None] * 26
            self.is_end = is_end

        def has_child(self, char: str) -> bool:
            return self.children[ord(char) - ord('a')] is not None

        def add_child(self, char: str):
            self.children[ord(char) - ord('a')] = self.__class__(char)

        def get_child(self, char: str):
            return self.children[ord(char) - ord('a')]

        def __str__(self):
            return f'<Node: {self.char}>'

        def __repr__(self):
            return str(self)

    def insert(self, word):
        Trie._insert(self.root, word)

    @classmethod
    def _insert(cls, root: Node, word: str):
        char = word[0]
        if not root.has_child(char):
            root.add_child(char)
        if len(word) == 1:
            root.get_child(char).is_end = True
            return
        cls._insert(root.get_child(char), word[1:])

