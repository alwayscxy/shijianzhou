import sorter
from visualize import draw_top_words, get_next_image_path
from exporter import export_words, get_next_export_path


def visualize_top_words(nodes, top_n=10):

    print("\n====== 高频词可视化 ======")

    # 使用快速排序
    sorted_nodes, cmp = sorter.quick_sort(nodes)

    print(f"排序完成（快速排序），比较次数：{cmp}")
    print(f"展示 Top-{top_n} 高频词\n")

    # 生成图像
    image_path = get_next_image_path()
    draw_top_words(sorted_nodes, top_n=top_n, save_path=image_path)

    print(f"词频柱状图已保存为：{image_path}")

    # 导出文本
    export_path = get_next_export_path()
    export_words(sorted_nodes[:top_n], export_path)

    print(f"高频词文本已导出到文件：{export_path}")
    print("\n====== 可视化完成 ======\n")


def preview_top_words(nodes, top_n=10):

    print("\n====== 高频词预览 ======")

    sorted_nodes, cmp = sorter.quick_sort(nodes)

    print(f"排序完成（快速排序），比较次数：{cmp}")
    print(f"Top-{top_n} 高频词如下：\n")

    for node in sorted_nodes[:top_n]:
        print(f"{node.word} : {node.count}")

    print("\n====== 预览结束 ======\n")
