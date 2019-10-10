class Trie(object):
    def __init__(self):
        self.root = self.Node(None)

    class Node(object):
        def __init__(self, char, is_end=False):
            self.char = char
            self.children = {}
            self.is_end = is_end
            self.contacts = []

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

    def insert(self, word, contact):
        self._insert(self.root, word, contact)

    @classmethod
    def _insert(cls, root: Node, word: str, contact):
        char = word[0]
        if not root.has_child(char):
            root.add_child(char)
        if len(word) == 1:
            end_node = root.get_child(char)
            end_node.is_end = True
            end_node.contacts.append(contact)
            return
        cls._insert(root.get_child(char), word[1:], contact)

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
        return sum([len(node.contacts) for node in self._traverse_pre(self.root) if node.is_end])

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

    def autocomplete(self, prefix: str)->[]:
        root = self.chase(prefix)
        contacts = []
        if root is None:
            return contacts
        self._autocomplete(root, prefix, contacts)
        return contacts

    @classmethod
    def _autocomplete(cls, root: Node, prefix: str, contacts: []):
        if root.is_end:
            contacts.extend(root.contacts)
        for node in root.get_children():
            cls._autocomplete(node, prefix + node.char, contacts)

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


class Contact(object):
    def __init__(self, phone: str, name: str, surname: str = '', address: str = ''):
        self.phone = phone
        self.name = name
        self.surname = surname
        self.address = address

    def __str__(self):
        return f'<{self.name}:{self.surname} phone={self.phone}>'

    def __repr__(self):
        return str(self)


class ContactList(object):
    def __init__(self):
        self._trie = Trie()

    def add(self, phone: str, name: str, surname: str = '', address: str = ''):
        contact = Contact(phone, name, surname, address)
        self._trie.insert(name, contact)

    def suggest(self, prefix: str)->[Contact]:
        return self._trie.autocomplete(prefix)

    def count(self)->int:
        return self._trie.count_words()

    def remove(self, name: str):
        self._trie.remove(name)

    def get_all(self):
        return self._trie.autocomplete('')

    def __contains__(self, item):
        return item in self._trie


contact_list = ContactList()
contact_list.add('89162342277', 'oliver', 'james')
contact_list.add('89163214576', 'jack', 'john')
contact_list.add('89565511573', 'harry', 'robbert')
contact_list.add('89162342277', 'jacob', 'michael')
contact_list.add('89163214576', 'tom', 'jerry')
contact_list.add('89162342277', 'nu', 'pogodi')
contact_list.add('89163214576', 'oscar', 'johnson')
contact_list.add('89162342277', 'george', 'williams')
contact_list.add('89993219856', 'quentin', 'tarantino')
contact_list.add('89162342277', 'mobi', 'dick')
contact_list.add('89993214354', 'jack', 'daniels')

print(contact_list.count())

