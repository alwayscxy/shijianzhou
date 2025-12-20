# app_cli.py
from controllers.init_controller import init_system
from controllers.stats_controller import show_basic_statistics
from controllers.search_controller import (
    search_word,
    hash_performance_analysis
)
from controllers.sort_controller import compare_sort_algorithms, sort_by_rule
from controllers.visualize_controller import visualize_top_words
from controllers.hp_controller import (
    analyze_min_word_book,
    analyze_top_words_of_book
)

import os
import matplotlib.pyplot as plt


def choose_text_file_cli():
    data_dir = "data"
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

    if not files:
        print("data 目录下没有 txt 文件")
        return None

    print("\n可用文本文件：")
    for idx, name in enumerate(files, start=1):
        print(f"{idx}. {name}")

    choice = input("请选择文件编号：").strip()
    if not choice.isdigit():
        return None

    idx = int(choice)
    if idx < 1 or idx > len(files):
        return None

    return os.path.join(data_dir, files[idx - 1])


def main():
    print("======= 文本词频统计系统（CLI） =======")

    filepath = choose_text_file_cli()
    if not filepath:
        print("文件选择失败，程序退出")
        return

    context = init_system(filepath)

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
        print("1. 基本统计信息")
        print("2. 查找方法对比")
        print("3. 排序方法对比与排序")
        print("4. 可视化与结果导出")
        print("5. Harry Potter 系列分析")
        print("0. 退出")

        choice = input("请选择功能：").strip()

        # ---------- 1 ----------
        if choice == "1":
            show_basic_statistics(context)

        # ---------- 2 ----------
        elif choice == "2":
            word = input("请输入要查询的单词：").strip().lower()
            result = search_word(word, array_nodes, hash_chain, hash_linear)

            print("\n====== 查找结果（当前单词） ======")
            for name, res in result.items():
                print(f"[{name}]")
                print(f"  是否找到：{res['found']}")
                print(f"  出现次数：{res['count']}")
                print(f"  比较次数：{res['comparisons']}")

            # ⭐ 新增：当前单词的哈希查找性能细节
            print("\n====== 当前单词的哈希查找细节 ======")

            hc = result["hash_chain"]["detail"]
            print(
                f"[拉链法] 哈希地址={hc['hash_index']} "
                f"链长={hc['chain_length']} "
                f"比较次数={hc['comparisons']} "
                f"成功={hc['success']}"
            )

            hl = result["hash_linear"]["detail"]
            print(
                f"[线性探测] 初始地址={hl['hash_index']} "
                f"命中地址={hl['hit_index']} "
                f"探测步数={hl['probe_steps']} "
                f"成功={hl['success']}"
            )

            show_perf = input("\n是否查看【哈希表整体性能】？(y/n)：").strip().lower()
            if show_perf == "y":
                perf = hash_performance_analysis(
                    current_nodes, hash_chain, hash_linear
                )
                print("\n====== 哈希表整体性能（与具体单词无关） ======")
                for k, v in perf.items():
                    print(
                        f"[{k}] "
                        f"装载因子={v['alpha']:.5f} "
                        f"冲突={v['conflicts']} "
                        f"ASL={v['asl']:.3f}"
                    )

        # ---------- 3 ----------
        elif choice == "3":
            n = input("请输入 Top-N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            report = compare_sort_algorithms(current_nodes, top_n=n)
            print("\n====== 排序算法性能对比 ======")
            for name, info in report.items():
                print(f"{name}: {info['time']:.2f}ms, 比较次数={info['comparisons']}")

            print("\n可选排序规则：")
            print("1. freq（词频）")
            print("2. freq_alpha（词频 + 字母）")
            print("3. freq_length（词频 + 单词长度）")

            rule_map = {"1": "freq", "2": "freq_alpha", "3": "freq_length"}
            r = input("请选择排序规则：").strip()

            if r in rule_map:
                sorted_nodes = sort_by_rule(current_nodes, rule_map[r])
                print(f"\n====== Top {n} 排序结果 ======")
                for i, node in enumerate(sorted_nodes[:n], start=1):
                    print(f"{i:02d}. {node.word} -> {node.count}")

        # ---------- 4 ----------
        elif choice == "4":
            n = input("请输入 Top-N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            top_nodes = visualize_top_words(
                current_nodes,
                top_n=n,
                export=True,
                draw=True,
                show=True      # ⭐ 关键：明确要求显示
            )

            print(f"\n====== Top {n} 高频词 ======")
            for i, node in enumerate(top_nodes, start=1):
                print(f"{i:02d}. {node.word} -> {node.count}")

        # ---------- 5 ----------
        elif choice == "5":
            print("\n1. 统计单词量最少的一部")
            print("2. 查看某一部的高频词")
            sub = input("请选择：").strip()

            if sub == "1":
                result = analyze_min_word_book(harry_books)
                print("\n====== 各书词数 ======")
                for i, name, cnt in result["details"]:
                    print(f"{i}. {name} -> {cnt}")
                idx, name, cnt = result["min_book"]
                print(f"\n最少的一部：{name}（{cnt}）")
                print(f"结果已导出：{result['export_path']}")

            elif sub == "2":
                for idx, name in harry_books.items():
                    print(f"{idx}. {name}")

                book_idx = input("请输入书号：").strip()
                if not book_idx.isdigit():
                    continue

                n = input("请输入 Top-N（默认 10）：").strip()
                n = int(n) if n.isdigit() else 10

                result = analyze_top_words_of_book(
                    harry_books, int(book_idx), n
                )
                print(f"\n======《{result['book']}》Top {n} ======")
                for i, (w, c) in enumerate(result["top_words"], start=1):
                    print(f"{i:02d}. {w} -> {c}")
                print(f"结果已导出：{result['export_path']}")

        elif choice == "0":
            print("系统已退出。")
            break

        else:
            print("无效选择，请重试。")
