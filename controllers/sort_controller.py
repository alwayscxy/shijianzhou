import sorter


def compare_sort_algorithms(nodes, top_n=10):
    print("\n====== 排序算法性能对比 ======")

    # 冒泡排序
    bubble_res, bubble_cmp, bubble_swap = sorter.bubble_sort(nodes)
    print("\n【冒泡排序】")
    print(f"比较次数：{bubble_cmp}")
    print(f"交换次数：{bubble_swap}")
    print("Top 结果：")
    for node in bubble_res[:top_n]:
        print(node)

    # 插入排序
    insert_res, insert_cmp, insert_move = sorter.insertion_sort(nodes)
    print("\n【插入排序】")
    print(f"比较次数：{insert_cmp}")
    print(f"移动次数：{insert_move}")
    print("Top 结果：")
    for node in insert_res[:top_n]:
        print(node)

    # 快速排序
    quick_res, quick_cmp = sorter.quick_sort(nodes)
    print("\n【快速排序】")
    print(f"比较次数：{quick_cmp}")
    print("Top 结果：")
    for node in quick_res[:top_n]:
        print(node)

    # 三色旗快速排序
    dutch_res, dutch_cmp = sorter.quick_sort_dutch_flag(nodes)
    print("\n【三色旗快速排序】")
    print(f"比较次数：{dutch_cmp}")
    print("Top 结果：")
    for node in dutch_res[:top_n]:
        print(node)

    print("\n====== 排序算法对比结束 ======\n")


def sort_by_rule(nodes):
    """
    根据用户选择的排序规则进行最终排序
    """
    print("\n请选择排序规则：")
    print("1. 按词语长度排序")
    print("2. 按词频 + 词语长度排序")
    print("3. 按词频 + 英文首字母排序")
    print("4. 按词频 + 中文拼音首字母排序")

    choice = input("请输入选项（1-4）：").strip()

    if choice == "1":
        order = input("排序方式：1-从长到短  2-从短到长：").strip()
        reverse = True if order != "2" else False
        sorted_nodes = sorter.sort_by_word_length(nodes, reverse=reverse)

    elif choice == "2":
        sorted_nodes = sorter.sort_by_freq_then_length(nodes)

    elif choice == "3":
        sorted_nodes = sorter.sort_by_freq_then_alpha(nodes)

    elif choice == "4":
        sorted_nodes = sorter.sort_by_freq_then_pinyin(nodes)

    else:
        print("输入无效，默认按词频排序")
        sorted_nodes, _ = sorter.quick_sort(nodes)

    return sorted_nodes
