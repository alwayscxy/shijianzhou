# 定义单词结点的数据结构
class WordNode:
    def __init__(self, word, position):
        self.word = word  # 保存单词内容
        self.count = 1  # 第一次出现的时候单词个数为1
        self.first_pos = position  # 单词第一次出现的位置

    # def __repr__(self):
    #     return f"{self.word}:{self.count}(first at {self.first_pos})"
