# main.py
from controllers.init_controller import init_system
from controllers.stats_controller import show_basic_statistics
from controllers.search_controller import (
    search_word,
    hash_performance_analysis
)
from controllers.sort_controller import compare_sort_algorithms, sort_by_rule
from controllers.visual_controller import (
    visualize_top_words,
    preview_top_words
)
from controllers.hp_controller import (
    analyze_min_word_book,
    analyze_top_words_of_book
)


def main():
    print("======= 文本词频统计系统 =======")

    # ① 初始化（加载 + 分词 + 建表）
    context = init_system("data/input.txt")

    # 从context中提取变量，避免未定义错误
    array_nodes = context["array_nodes"]
    hash_chain = context["hash_chain"]
    hash_linear = context["hash_linear"]
    current_nodes = context["current_nodes"]
    harry_books = {
        1: "Harry Potter 1 - Harry Potter and the Philosophers Stone.txt",
        2: "Harry Potter 2 - Harry Potter and the Chamber of Secrets.txt",
        3: "Harry Potter 3 - Harry Potter and the Prisoner of Azkaban.txt",
        4: "Harry Potter 4 - Harry Potter and the Goblet of Fire.txt",
        5: "Harry Potter 5 - Harry Potter and the Order of the Phoenix.txt",
        6: "Harry Potter 6 - Harry Potter and the Half-Blood Prince.txt",
        7: "Harry Potter 7 - Harry Potter and the Deathly Hallows.txt"
    }

    while True:
        print("\n====== 主功能菜单 ======")
        print("1.基本统计信息")
        print("2.查找方法对比")
        print("3.排序方法对比与排序")
        print("4.可视化与结果导出")
        print("5.Harry Potter 系列分析")
        print("0.退出")

        choice = input("请选择功能：").strip()

        if choice == "1":
            show_basic_statistics(context)

        elif choice == "2":
            word = input("请输入要查询的单词：").strip().lower()
            search_word(word, array_nodes, hash_chain, hash_linear)
            show_perf = input("是否查看哈希表性能分析？(y/n)：").strip().lower()
            if show_perf == "y":
                hash_performance_analysis(current_nodes, hash_chain, hash_linear)

        elif choice == "3":
            n = input("请输入要展示的数量 N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10
            compare_sort_algorithms(current_nodes, top_n=n)
            use_sort = input("\n是否选择一种排序规则作为最终结果？(y/n)：").strip().lower()
            if use_sort == "y":
                sorted_nodes = sort_by_rule(current_nodes)
                print("\n最终排序结果：")
                for node in sorted_nodes[:n]:
                    print(node)

        elif choice == "4":
            print("\n1. 控制台预览高频词")
            print("2. 生成柱状图并导出结果")
            sub = input("请选择：").strip()

            n = input("请输入 Top-N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            if sub == "1":
                preview_top_words(current_nodes, n)
            elif sub == "2":
                visualize_top_words(current_nodes, n)

        elif choice == "5":
            print("\n1. 统计 1-7 中单词量最少的一部")
            print("2. 查看某一部的高频单词")
            sub = input("请选择：").strip()

            if sub == "1":
                analyze_min_word_book(harry_books)

            elif sub == "2":
                for idx, name in harry_books.items():
                    print(f"{idx}. {name}")

                book_idx = input("请输入书号（1-7）：").strip()
                if not book_idx.isdigit() or int(book_idx) not in harry_books:
                    print("输入无效")
                    continue

                n = input("请输入 Top-N（默认 10）：").strip()
                n = int(n) if n.isdigit() else 10

                analyze_top_words_of_book(harry_books, int(book_idx), n)

        elif choice == "0":
            print("系统已退出。")
            break

        else:
            print("无效选择，请重试。")


if __name__ == "__main__":
    main()
