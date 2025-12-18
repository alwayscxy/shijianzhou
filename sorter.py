from pypinyin import lazy_pinyin


def bubble_sort(nodes):  # 冒泡排序,可以优化
    n = len(nodes)
    result = nodes[:]

    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(n - i - 1):
            comparisons += 1
            if result[j].count < result[j + 1].count:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1
    return result, comparisons, swaps


def insertion_sort(nodes):
    arr = nodes[:]
    n = len(arr)
    comparisons = 0
    moves = 0
    for i in range(1, n):
        current = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j].count < current.count:
                arr[j + 1] = arr[j]
                j -= 1
                moves += 1
            else:
                break
        arr[j + 1] = current
        moves += 1
    return arr, comparisons, moves


def quick_sort(nodes):  # 快速排序
    if len(nodes) <= 1:
        return nodes, 0
    pivot = nodes[0]  # 基准
    comparisons = 0
    left = []
    right = []

    for x in nodes[1:]:
        comparisons += 1
        if x.count > pivot.count:
            left.append(x)
        else:
            right.append(x)
    sorted_left, left_cmp = quick_sort(left)
    sorted_right, right_cmp = quick_sort(right)
    total_cmp = comparisons + left_cmp + right_cmp
    return sorted_left + [pivot] + sorted_right, total_cmp


def quick_sort_dutch_flag(nodes):  # 快速排序（三色旗）
    if len(nodes) <= 1:
        return nodes, 0

    pivot = nodes[0]
    high = []  # count > pivot
    equal = []  # count == pivot
    low = []  # count < pivot

    comparisons = 0

    for node in nodes:
        comparisons += 1
        if node.count > pivot.count:
            high.append(node)
        elif node.count < pivot.count:
            low.append(node)
        else:
            equal.append(node)

    sorted_high, cmp_high = quick_sort_dutch_flag(high)
    sorted_low, cmp_low = quick_sort_dutch_flag(low)

    total_cmp = comparisons + cmp_high + cmp_low

    return sorted_high + equal + sorted_low, total_cmp


def sort_by_word_length(nodes, reverse=True):  # 按单词长度排序
    sorted_nodes = sorted(
        nodes,
        key=lambda node: len(node.word),
        reverse=reverse
    )
    return sorted_nodes


def sort_by_freq_then_length(nodes):  # 按词频和长度排序
    return sorted(
        nodes,
        key=lambda node: (node.count, len(node.word)),
        reverse=True
    )


def sort_by_freq_then_alpha(nodes):
    """
    按词频（降序） + 英文单词字典序（升序）进行二级排序
    非英文单词统一排在后面
    """

    def is_english_word(word):
        # 严格判断：所有字符都是 a-z
        return word.isascii() and word.isalpha()

    def sort_key(node):
        if is_english_word(node.word):
            return (-node.count, 0, node.word)
        else:
            # 非英文词统一排后
            return (-node.count, 1, node.word)

    return sorted(nodes, key=sort_key)


def sort_by_freq_then_pinyin(nodes):  # 按词频和拼音首字母排序
    def is_chinese_word(word):
        return any('\u4e00' <= ch <= '\u9fff' for ch in word)

    def get_pinyin_initial(word):
        # 取第一个汉字的拼音首字母
        py = lazy_pinyin(word[0])
        return py[0][0] if py else '{'

    def sort_key(node):
        if is_chinese_word(node.word):
            return (-node.count, 0, get_pinyin_initial(node.word))
        else:
            # 非中文词排后
            return (-node.count, 1, node.word)

    return sorted(nodes, key=sort_key)
