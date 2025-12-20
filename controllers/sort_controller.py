import time
import copy
import sorter


def compare_sort_algorithms(nodes, top_n=20):
    algorithms = {
        "冒泡排序": sorter.bubble_sort,
        "插入排序": sorter.insertion_sort,
        "快速排序": sorter.quick_sort,
        "三路快排": sorter.quick_sort_dutch_flag,
    }

    report = {}

    for name, func in algorithms.items():
        data = copy.deepcopy(nodes)

        start = time.time()
        sorted_nodes, comparisons = func(data)
        elapsed = (time.time() - start) * 1000

        report[name] = {
            "time": elapsed,
            "comparisons": comparisons,
            "top": sorted_nodes[:top_n],
        }

    return report


def sort_by_rule(nodes, rule):
    if rule == "freq":
        return sorted(nodes, key=lambda x: x.count, reverse=True)
    elif rule == "freq_alpha":
        return sorted(nodes, key=lambda x: (-x.count, x.word))
    elif rule == "freq_length":
        return sorted(nodes, key=lambda x: (-x.count, len(x.word)))
    else:
        raise ValueError("未知排序规则")
