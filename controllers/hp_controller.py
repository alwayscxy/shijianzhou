import os
from stopwords import STOP_WORDS
from loader import load_text
from splitter import split_text
from array_counter import count_words_array
import sorter
from exporter import (
    export_hp_word_count,
    export_hp_top_words,
    get_next_hp_export_path
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 根目录，abspath绝对路径，dirname获取父目录
DATA_DIR = os.path.join(BASE_DIR, "data")  # 数据目录


def analyze_min_word_book(harry_books):
    results = []
    min_item = None

    for idx, filename in harry_books.items():
        path = os.path.join(DATA_DIR, filename)
        text = load_text(path)

        words = split_text(text, mode="english", zh_method="rule")
        count = len(words)

        item = (idx, filename, count)
        results.append(item)

        if min_item is None or count < min_item[2]:
            min_item = item

    export_path = get_next_hp_export_path("hp_word_count_summary")
    export_hp_word_count(
        [f"{i}. {name} : {cnt}" for i, name, cnt in results],
        min_item[1],
        min_item[2],
        export_path
    )

    return {
        "details": results,
        "min_book": min_item,
        "export_path": export_path
    }


def analyze_top_words_of_book(harry_books, book_index, top_n=10):
    filename = harry_books[book_index]
    path = os.path.join(DATA_DIR, filename)

    text = load_text(path)
    words = split_text(text, mode="english", zh_method="rule")
    total_cnt = len(words)

    # 不同词（未过滤，用于词汇丰富度）
    all_nodes = count_words_array(words)
    unique_cnt = len(all_nodes)
    ratio = unique_cnt / total_cnt if total_cnt > 0 else 0

    # ⭐ 高频词统计用过滤后的
    filtered_words = [
        w for w in words
        if w not in STOP_WORDS and len(w) > 2
    ]

    nodes = count_words_array(filtered_words)

    sorted_nodes, _ = sorter.quick_sort_dutch_flag(nodes)
    top_nodes = sorted_nodes[:top_n]

    export_path = get_next_hp_export_path(
        f"hp_top_words_book{book_index}_top{top_n}_filtered"
    )

    export_hp_top_words(
        filename,
        sorted_nodes,
        top_n,
        export_path,
        removed_words=sorted(STOP_WORDS)
    )

    return {
        "book": filename,
        "top_words": [(n.word, n.count) for n in top_nodes],
        "export_path": export_path,
        "removed": sorted(STOP_WORDS),

        # ⭐ 新增
        "total_words": total_cnt,
        "unique_words": unique_cnt,
        "ratio": ratio
    }
