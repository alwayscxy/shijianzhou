from searcher import (
    search_in_array,
    search_in_hash_chaining,
    search_in_hash_linear,
)


def search_word(word, array_nodes, hash_chain, hash_linear):
    result = {}

    # 数组
    arr = search_in_array(array_nodes, word)
    result["array"] = {
        "found": arr["success"],
        "count": arr["node"].count if arr["node"] else 0,
        "first_pos": arr["node"].first_pos if arr["node"] else None,
        "comparisons": arr["comparisons"],
        "detail": arr,
    }

    # 拉链哈希
    ch = search_in_hash_chaining(hash_chain, word)
    result["hash_chain"] = {
        "found": ch["success"],
        "count": ch["node"].count if ch["node"] else 0,
        "first_pos": ch["node"].first_pos if ch["node"] else None,
        "comparisons": ch["comparisons"],
        "detail": ch,
    }

    # 线性探测哈希
    ln = search_in_hash_linear(hash_linear, word)
    result["hash_linear"] = {
        "found": ln["success"],
        "count": ln["node"].count if ln["node"] else 0,
        "first_pos": ln["node"].first_pos if ln["node"] else None,
        "comparisons": ln["comparisons"],
        "detail": ln,
    }

    return result


def hash_performance_analysis(nodes, hash_chain, hash_linear):
    # 哈希表整体性能分析（ASL / 装载因子 / 冲突）
    total_cmp_chain = 0  # 哈希表拉链法总比较次数
    total_cmp_linear = 0  # 哈希表线性探测总比较次数
    total_searches = len(nodes)  # 总搜索次数

    for node in nodes:
        ch = search_in_hash_chaining(hash_chain, node.word)
        ln = search_in_hash_linear(hash_linear, node.word)

        total_cmp_chain += ch["comparisons"]
        total_cmp_linear += ln["comparisons"]

    return {
        "chain": {
            "alpha": total_searches / hash_chain.size,  # 装载因子=表中元素数/表大小
            "conflicts": hash_chain.conflicts,  # 冲突次数
            "asl": total_cmp_chain / total_searches,  # 平均查找长度ASL=总比较次数/总搜索次数
        },
        "linear": {
            "alpha": total_searches / hash_linear.size,
            "conflicts": hash_linear.conflicts,
            "asl": total_cmp_linear / total_searches,
        },
    }
