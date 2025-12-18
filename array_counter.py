# 基于数组的词频统计
from node import WordNode


def count_words_array(words):
    table = []
    for index, word in enumerate(words):  # 遍历所有单词
        found = False
        for node in table:
            if node.word == word:
                node.count += 1
                found = True
                break
        if not found:
            table.append(WordNode(word, index))

    return table
