# 使用拉链法解决冲突的哈希表实现
from node import WordNode


class HashTableChaining:
    def __init__(self, size=1000000):  # 初始化哈希表
        self.size = size
        self.table = [[] for _ in range(size)]
        self.conflicts = 0  # 冲突次数
        self.insert_count = 0  # 插入次数，不过没用到，因为可以用单词表的长度来计算

    def _hash(self, word):  # 计算单词的索引
        return sum(ord(c) for c in word) % self.size

    def insert(self, word, position):  # 在链表中查找是否存在该单词，存在的话就改变单词个数，不存在的话就创建新的结点
        index = self._hash(word)
        chain = self.table[index]

        if len(chain) > 0:  # 如果已有元素，说明发生冲突
            self.conflicts += 1
        for node in chain:
            if node.word == word:
                node.count += 1
                return
        chain.append(WordNode(word, position))
        self.insert_count += 1

    def build(self, words):  # 构建哈希表
        for index, word in enumerate(words):
            self.insert(word, index)

    def get_all_nodes(self):  # 获取所有结点，用于排序，输出
        result = []
        for chain in self.table:
            result.extend(chain)
        return result
