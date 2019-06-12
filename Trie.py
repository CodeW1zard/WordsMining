import collections
import numpy as np
from time import time
from queue import Queue
from Entropy import entropy



def n_gram_list(text, n):
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def loglinear(x):
    return x * np.log2(x)


class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.count = 0
        self.entropy = 0
        self.end = None


class Trie:
    def __init__(self, direction='prefix'):
        self.root = TrieNode()
        self.direction = direction

    def insert(self, word, n):
        assert len(word) == n, '{}-gram序列构建Trie' % n

        current = self.root

        if self.direction == 'prefix':
            word = word[::-1]

        for letter in word:
            tmp = current.children[letter]
            if tmp.count == 0 or tmp.end == n:
                tmp.count += 1
            current = tmp
        current.end = n

    def set_entropy(self):
        tic = time()
        node = self.root
        queue = Queue()
        queue.put(node)

        while not queue.empty():
            node = queue.get()
            cnts = []
            for child in node.children.values():
                queue.put(child)
                cnts.append(child.count)
            if cnts:
                cnts = np.array(cnts)
                node.entropy = entropy(cnts)
            else:
                node.entropy = 0


    def search(self, word):
        if self.direction == 'prefix':
            word = word[::-1]
        current = self.root

        for letter in word:
            if current is None:
                # not found
                return None
            current = current.children.get(letter)

        return current


if __name__ == "__main__":
    text = "吃葡萄不吐葡萄皮不吃葡萄倒吐葡萄皮"

    prefixTree = Trie()
    suffixTree = Trie(direction='suffix')
    for i in range(3):
        n_gram = n_gram_list(text, i + 1)
        for word in n_gram:
            prefixTree.insert(word, i + 1)
            suffixTree.insert(word, i + 1)

    print(suffixTree.search('葡萄'))
    print(prefixTree.search('皮'))
