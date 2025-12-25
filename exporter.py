import os


def export_words(nodes, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for node in nodes:
            f.write(f"{node.word}\t{node.count}\n")


def get_next_export_path():
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    index = 1
    while True:
        path = os.path.join(output_dir, f"top_words_{index}.txt")
        if not os.path.exists(path):
            return path
        index += 1


def get_next_hp_export_path(prefix, ext="txt"):  # 自动生成文件名(hp)
    idx = 1
    while True:
        path = f"output/{prefix}_{idx:03d}.{ext}"  # 0填充，3位，d：整数
        if not os.path.exists(path):
            return path
        idx += 1


def export_hp_word_count(summary, min_book, min_count, path):  # 导出哈利波特中单词量统计结果
    with open(path, "w", encoding="utf-8") as f:
        f.write("Harry Potter 系列 1-7 单词总量统计\n\n")
        for line in summary:
            f.write(line + "\n")

        f.write("\n单词量最少的一部：\n")
        f.write(f"{min_book} （{min_count} 个单词）\n")


def export_hp_top_words(book_name, nodes, top_n, path, removed_words=None):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{book_name}\n")
        f.write(f"高频词 Top-{top_n}\n\n")

        if removed_words:
            f.write("【说明】统计前已去除以下停用词（部分或全部）：\n")
            f.write(", ".join(removed_words) + "\n\n")

        for i, node in enumerate(nodes[:top_n], start=1):
            f.write(f"{i}. {node.word} : {node.count}\n")

