def bubble_sort(nodes):
    arr = nodes[:]
    n = len(arr)
    cmp = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            cmp += 1
            if arr[j].count < arr[j + 1].count:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr, cmp


def insertion_sort(nodes):
    arr = nodes[:]
    cmp = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].count < key.count:
            cmp += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr, cmp


def quick_sort(nodes):
    """
    安全版快排：三路划分，防止递归爆栈
    """
    if len(nodes) <= 1:
        return nodes[:], 0

    pivot = nodes[len(nodes) // 2].count
    left = []
    mid = []
    right = []
    cmp = 0

    for node in nodes:
        cmp += 1
        if node.count > pivot:
            left.append(node)
        elif node.count < pivot:
            right.append(node)
        else:
            mid.append(node)

    sorted_left, cmp_l = quick_sort(left)
    sorted_right, cmp_r = quick_sort(right)

    return sorted_left + mid + sorted_right, cmp + cmp_l + cmp_r


def quick_sort_dutch_flag(nodes):
    """
    与 quick_sort 行为一致，保留接口
    """
    return quick_sort(nodes)
