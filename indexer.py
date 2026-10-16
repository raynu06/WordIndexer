import sys
import re

class LineNode:
    def __init__(self, line_num):
        self.line_num = line_num
        self.next = None

class LineQueue:
    def __init__(self):
        self.head = self.tail = None

    def enqueue(self, line_num):
        if self.tail and self.tail.line_num == line_num:
            return
        node = LineNode(line_num)
        if not self.head:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def to_list(self):
        res, curr = [], self.head
        while curr:
            res.append(str(curr.line_num))
            curr = curr.next
        return res

# 1. Trie Index
class TrieNode:
    def __init__(self):
        self.children = {}
        self.lines = LineQueue()
        self.is_word = False

class TrieIndex:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_num):
        curr = self.root
        for char in word:
            curr = curr.children.setdefault(char, TrieNode())
        curr.is_word = True
        curr.lines.enqueue(line_num)

    def search(self, word):
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_word

    def get_lexicographical_index(self):
        result = []
        def dfs(node, path):
            if node.is_word:
                result.append((path, node.lines.to_list()))
            for char in sorted(node.children.keys()):
                dfs(node.children[char], path + char)
        dfs(self.root, "")
        return result

# 2. BST Index
class BSTNode:
    def __init__(self, word):
        self.word = word
        self.lines = LineQueue()
        self.left = self.right = None

class BSTIndex:
    def __init__(self):
        self.root = None

    def insert(self, word, line_num):
        if not self.root:
            self.root = BSTNode(word)
            self.root.lines.enqueue(line_num)
            return
        curr = self.root
        while True:
            if word == curr.word:
                curr.lines.enqueue(line_num)
                return
            elif word < curr.word:
                if not curr.left:
                    curr.left = BSTNode(word)
                    curr.left.lines.enqueue(line_num)
                    return
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = BSTNode(word)
                    curr.right.lines.enqueue(line_num)
                    return
                curr = curr.right

    def search(self, word):
        curr = self.root
        while curr:
            if word == curr.word:
                return True
            curr = curr.left if word < curr.word else curr.right
        return False

    def get_lexicographical_index(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append((node.word, node.lines.to_list()))
                inorder(node.right)
        inorder(self.root)
        return result

# 3. Dictionary Index
class DictIndex:
    def __init__(self):
        self.store = {}

    def insert(self, word, line_num):
        if word not in self.store:
            self.store[word] = LineQueue()
        self.store[word].enqueue(line_num)

    def search(self, word):
        return word in self.store

    def get_lexicographical_index(self):
        return [(w, self.store[w].to_list()) for w in sorted(self.store.keys())]

def parse_and_index(input_file, index_struct):
    pattern = re.compile(r'[^ \t\n\r\f\v\.\,\:\;\ ]+')
    with open(input_file, 'r', encoding='ascii', errors='ignore') as f:
        for line_num, line in enumerate(f, start=1):
            for word in pattern.findall(line):
                index_struct.insert(word, line_num)

def write_output(index_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, lines in index_data:
            f.write(f"{word}: {', '.join(lines)}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python indexer.py <input_file> <output_file>")
        sys.exit(1)
    indexer = TrieIndex()
    parse_and_index(sys.argv[1], indexer)
    write_output(indexer.get_lexicographical_index(), sys.argv[2])
    print("Indexing complete.")