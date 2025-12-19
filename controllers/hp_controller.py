from loader import load_text
from splitter import split_text
from array_counter import count_words_array
import sorter
from exporter import (
    export_hp_word_count,
    export_hp_top_words,
    get_next_hp_export_path
)


def analyze_min_word_book(harry_books):
    print("\n====== Harry Potter 单词量统计 ======")

    min_count = None
    min_book = None
    summary_lines = []

    for idx, filename in harry_books.items():
        path = f"data/{filename}"

        text = load_text(path)
        words = split_text(
            text,
            mode="english",
            zh_method="rule"
        )

        count = len(words)
        line = f"{idx}. {filename} : {count}"
        print(line)
        summary_lines.append(line)

        if min_count is None or count < min_count:
            min_count = count
            min_book = filename

    print("\n单词量最少的一部是：")
    print(f"{min_book}（共 {min_count} 个单词）")

    export_path = get_next_hp_export_path("hp_word_count_summary")
    export_hp_word_count(summary_lines, min_book, min_count, export_path)

    print(f"\n统计结果已导出到文件：{export_path}")
    print("====== 统计完成 ======\n")


def analyze_top_words_of_book(harry_books, book_index, top_n=10):
    filename = harry_books[book_index]
    path = f"data/{filename}"

    print(f"\n====== 《{filename}》高频词分析 ======")

    text = load_text(path)
    words = split_text(
        text,
        mode="english",
        zh_method="rule"
    )

    nodes = count_words_array(words)

    # sorted_nodes, cmp = sorter.quick_sort(nodes)
    sorted_nodes, cmp = sorter.quick_sort_dutch_flag(nodes)
    print(f"排序完成（快速排序），比较次数：{cmp}")
    print(f"Top-{top_n} 高频单词如下：\n")

    for node in sorted_nodes[:top_n]:
        print(f"{node.word} : {node.count}")

    export_path = get_next_hp_export_path(
        f"hp_top_words_book{book_index}_top{top_n}"
    )
    export_hp_top_words(filename, sorted_nodes, top_n, export_path)

    print(f"\n高频词结果已导出到文件：{export_path}")
    print("====== 分析完成 ======\n")
