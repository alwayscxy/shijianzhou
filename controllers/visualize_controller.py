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
