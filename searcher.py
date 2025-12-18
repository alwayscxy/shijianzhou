# 单词查询
def search_in_array(nodes, target):
    comparisons = 0
    for node in nodes:
        comparisons += 1
        if node.word == target:
            return node, comparisons
    return None, comparisons


def search_in_hash_chaining(hash_table, target):
    index = hash_table._hash(target)
    chain = hash_table.table[index]
    comparisons = 0
    for node in chain:
        comparisons += 1
        if node.word == target:
            return node, comparisons
    return None, comparisons


def search_in_hash_linear(hash_table, target):
    index = hash_table._hash(target)
    size = hash_table.size
    comparisons = 0
    while hash_table.table[index] is not None:
        comparisons += 1
        if hash_table.table[index].word == target:
            return hash_table.table[index], comparisons
        index = (index + 1) % size
    return None, comparisons
