from searcher import (
    search_in_array,
    search_in_hash_chaining,
    search_in_hash_linear,
)
from stopwords import STOP_WORDS
from collections import defaultdict

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



def analyze_word_context(word, words, window_size=100, top_n=20):
    """
    词语上下文关联分析
    :param word: 查询词
    :param words: 原始分词列表（有顺序）
    :param window_size: 左右窗口大小
    :param top_n: 输出前 N 个高频上下文词
    """

    positions = [i for i, w in enumerate(words) if w == word]

    context_freq = defaultdict(int)

    for pos in positions:
        left = max(0, pos - window_size)
        right = min(len(words), pos + window_size + 1)

        for i in range(left, right):
            if i == pos:
                continue
            w = words[i]
            if w in STOP_WORDS or len(w) <= 2:
                continue
            context_freq[w] += 1

    sorted_context = sorted(
        context_freq.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "word": word,
        "total_occurrences": len(positions),
        "window_size": window_size,
        "context_words": sorted_context[:top_n],
        "removed_stopwords": sorted(STOP_WORDS)
    }
