def search_in_array(nodes, target):
    comparisons = 0
    for idx, node in enumerate(nodes):
        comparisons += 1
        if node.word == target:
            return {
                "node": node,
                "comparisons": comparisons,
                "success": True,
                "index": idx
            }
    return {
        "node": None,
        "comparisons": comparisons,
        "success": False,
        "index": None
    }


def search_in_hash_chaining(hash_table, target):
    index = hash_table._hash(target)
    chain = hash_table.table[index]

    comparisons = 0
    for pos, node in enumerate(chain):
        comparisons += 1
        if node.word == target:
            return {
                "node": node,
                "success": True,
                "comparisons": comparisons,
                "hash_index": index, # 哈希地址
                "chain_length": len(chain),
                "chain_pos": pos # 链中位置
            }

    return {
        "node": None,
        "success": False,
        "comparisons": comparisons,
        "hash_index": index,
        "chain_length": len(chain),
        "chain_pos": None
    }


def search_in_hash_linear(hash_table, target):
    index = hash_table._hash(target)
    size = hash_table.size

    comparisons = 0
    start_index = index

    while hash_table.table[index] is not None:
        comparisons += 1
        if hash_table.table[index].word == target:
            return {
                "node": hash_table.table[index],
                "success": True,
                "comparisons": comparisons,
                "hash_index": start_index,
                "hit_index": index,
                "probe_steps": comparisons
            }
        index = (index + 1) % size
        if index == start_index:
            break

    return {
        "node": None,
        "success": False,
        "comparisons": comparisons,
        "hash_index": start_index,
        "hit_index": None,
        "probe_steps": comparisons
    }
