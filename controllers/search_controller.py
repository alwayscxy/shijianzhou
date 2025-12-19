from searcher import (
    search_in_array,
    search_in_hash_chaining,
    search_in_hash_linear,
)


def search_word(word, array_nodes, hash_chain, hash_linear):
    print("\n====== 单词查找结果 ======")
    print(f"查询目标：{word}\n")

    # 数组查找
    res_array, cmp_array = search_in_array(array_nodes, word)
    if res_array:
        print(f"【数组查找】")
        print(f"次数={res_array.count}, 首次位置={res_array.first_pos}, 比较次数={cmp_array}")
    else:
        print(f"【数组查找】未找到, 比较次数={cmp_array}")

    # 拉链哈希
    res_chain, cmp_chain = search_in_hash_chaining(hash_chain, word)
    if res_chain:
        print(f"\n【拉链哈希】")
        print(f"次数={res_chain.count}, 首次位置={res_chain.first_pos}, 比较次数={cmp_chain}")
    else:
        print(f"\n【拉链哈希】未找到, 比较次数={cmp_chain}")

    # 线性探测哈希
    res_linear, cmp_linear = search_in_hash_linear(hash_linear, word)
    if res_linear:
        print(f"\n【线性探测哈希】")
        print(f"次数={res_linear.count}, 首次位置={res_linear.first_pos}, 比较次数={cmp_linear}")
    else:
        print(f"\n【线性探测哈希】未找到, 比较次数={cmp_linear}")

    print("\n====== 查找结束 ======\n")


def hash_performance_analysis(nodes, hash_chain, hash_linear):
    """
    哈希表性能分析：ASL、装载因子、冲突次数
    """
    print("\n====== 哈希表性能分析 ======")

    total_cmp_chain = 0
    total_cmp_linear = 0
    total_searches = len(nodes)

    for node in nodes:
        _, cmp_chain = search_in_hash_chaining(hash_chain, node.word)
        _, cmp_linear = search_in_hash_linear(hash_linear, node.word)
        total_cmp_chain += cmp_chain
        total_cmp_linear += cmp_linear

    asl_chain = total_cmp_chain / total_searches
    asl_linear = total_cmp_linear / total_searches

    alpha_chain = total_searches / hash_chain.size
    alpha_linear = total_searches / hash_linear.size

    print("\n【拉链法哈希表】")
    print(f"容量：{hash_chain.size}")
    print(f"装载因子 α：{alpha_chain:.2f}")
    print(f"冲突次数：{hash_chain.conflicts}")
    print(f"平均查找长度 ASL：{asl_chain:.2f}")

    print("\n【线性探测哈希表】")
    print(f"容量：{hash_linear.size}")
    print(f"装载因子 α：{alpha_linear:.2f}")
    print(f"冲突次数：{hash_linear.conflicts}")
    print(f"平均查找长度 ASL：{asl_linear:.2f}")

    print("\n====== 哈希分析结束 ======\n")
