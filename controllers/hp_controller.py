import os
from loader import load_text
from splitter import split_text
from array_counter import count_words_array
import sorter
from exporter import (
    export_hp_word_count,
    export_hp_top_words,
    get_next_hp_export_path
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def analyze_min_word_book(harry_books):
    """
    返回：
    {
        "details": [(idx, filename, count), ...],
        "min_book": (idx, filename, count),
        "export_path": "xxx.txt"
    }
    """
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
    """
    返回：
    {
        "book": filename,
        "top_words": [(word, count), ...],
        "export_path": "xxx.txt"
    }
    """
    filename = harry_books[book_index]
    path = os.path.join(DATA_DIR, filename)

    text = load_text(path)
    words = split_text(text, mode="english", zh_method="rule")
    nodes = count_words_array(words)

    sorted_nodes, _ = sorter.quick_sort_dutch_flag(nodes)
    top_nodes = sorted_nodes[:top_n]

    export_path = get_next_hp_export_path(
        f"hp_top_words_book{book_index}_top{top_n}"
    )
    export_hp_top_words(filename, sorted_nodes, top_n, export_path)

    return {
        "book": filename,
        "top_words": [(n.word, n.count) for n in top_nodes],
        "export_path": export_path
    }
