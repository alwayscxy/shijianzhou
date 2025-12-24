# 使用线性探测法解决冲突
from node import WordNode

class HashTableLinear:
    def __init__(self, size=1000000):
        self.size = size
        self.table = [None] * size
        self.conflicts = 0
        self.insert_count = 0  # 插入次数，不过没用到，因为可以用单词表的长度来计算

    def _hash(self, word):
        return sum(ord(c) for c in word) % self.size

    def insert(self, word, position):
        index = self._hash(word)

        while self.table[index] is not None:
            self.conflicts += 1
            if self.table[index].word == word:
                self.table[index].count += 1
                return
            index = (index + 1) % self.size

        self.table[index] = WordNode(word, position)
        self.insert_count += 1

    def build(self, words):
        for index, word in enumerate(words):
            self.insert(word, index)

    def get_all_nodes(self):
        return [node for node in self.table if node is not None]
