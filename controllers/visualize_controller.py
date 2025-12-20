# controllers/visualize_controller.py

from sorter import quick_sort
from visualize import draw_top_words, get_next_image_path
from exporter import export_words, get_next_export_path


def visualize_top_words(nodes, top_n=10, export=True, draw=True, show=False):
    """
    返回 Top-N 高频词
    - export=True  → 导出文本
    - draw=True    → 生成柱状图
    - show=True    → 弹出窗口（CLI 用）
    """

    sorted_nodes, _ = quick_sort(nodes)
    top_nodes = sorted_nodes[:top_n]

    if draw:
        image_path = get_next_image_path()
        draw_top_words(
            top_nodes,
            top_n=top_n,
            save_path=image_path,
            show=show
        )

    if export:
        export_path = get_next_export_path()
        export_words(top_nodes, export_path)

    return top_nodes

from visualize import (
    draw_top_words,
    draw_search_performance,
    draw_hash_asl,
    get_next_image_path
)

def visualize_top_words(nodes, top_n=10, export=True, draw=True, show=False):
    sorted_nodes, _ = quick_sort(nodes)
    top_nodes = sorted_nodes[:top_n]

    if draw:
        img = get_next_image_path("top_words")
        draw_top_words(top_nodes, top_n, img, show)

    if export:
        path = get_next_export_path()
        export_words(top_nodes, path)

    return top_nodes


# ⭐ 当前单词查找性能图
def visualize_search_performance(result, show=True):
    img = get_next_image_path("search_perf")
    draw_search_performance(result, img, show)
    return img


# ⭐ 哈希表 ASL 对比图
def visualize_hash_asl(perf, show=True):
    img = get_next_image_path("hash_asl")
    draw_hash_asl(perf, img, show)
    return img
