from loader import load_text  # 格式化，都转为小写，非字母转为空格
from splitter import split_text  # 英文分词和中文分词
from array_counter import count_words_array  # 统计词频
from hash_chaining import HashTableChaining  # 拉链法解决冲突的哈希表
from hash_linear import HashTableLinear  # 线性探测法解决冲突的哈希表
# from sorter import bubble_sort, quick_sort, insertion_sort, sort_by_word_length, sort_by_freq_then_length, sort_by_freq_then_alpha
import sorter
from searcher import (
    search_in_array,
    search_in_hash_linear,
    search_in_hash_chaining,
)
from visualize import draw_top_words, get_next_image_path
from exporter import export_words, get_next_export_path, export_hp_word_count, export_hp_top_words, \
    get_next_hp_export_path


def main():
    print("======= 文本词频统计系统 =======")
    harry_books = {
        1: "Harry Potter 1 - Harry Potter and the Philosophers Stone.txt",
        2: "Harry Potter 2 - Harry Potter and the Chamber of Secrets.txt",
        3: "Harry Potter 3 - Harry Potter and the Prisoner of Azkaban.txt",
        4: "Harry Potter 4 - Harry Potter and the Goblet of Fire.txt",
        5: "Harry Potter 5 - Harry Potter and the Order of the Phoenix.txt",
        6: "Harry Potter 6 - Harry Potter and the Half-Blood Prince.txt",
        7: "Harry Potter 7 - Harry Potter and the Deathly Hallows.txt",
    }
    filepath = "data/input.txt"  # 读取+预处理
    text = load_text(filepath)
    print("\n请选择分词方式：")
    print("1. 仅英文分词")
    print("2. 仅中文分词（规则）")
    print("3. 仅中文分词（jieba）")
    print("4. 中英混合（规则）")
    print("5. 中英混合（jieba）")

    token_choice = input("请输入选项（1-5）：").strip()
    if token_choice == "1":
        mode = "english"
        zh_method = "rule"  # 无所谓，但必须给
    elif token_choice == "2":
        mode = "chinese"
        zh_method = "rule"
    elif token_choice == "3":
        mode = "chinese"
        zh_method = "jieba"
    elif token_choice == "4":
        mode = "mixed"
        zh_method = "rule"
    elif token_choice == "5":
        mode = "mixed"
        zh_method = "jieba"
    else:
        print("输入无效，默认使用 中英混合 + 规则分词")
        mode = "mixed"
        zh_method = "rule"

    words = split_text(text, mode=mode, zh_method=zh_method)

    print(f"\n分词完成：模式={mode}，中文方式={zh_method}")
    print(f"共得到 {len(words)} 个词语。\n")

    # print(f"文本加载完成，共读取 {len(words)}个单词。\n")

    array_nodes = count_words_array(words)  # 统计词频

    hash_chain = HashTableChaining()  # 拉链法
    hash_chain.build(words)  # 构建哈希表

    hash_linear = HashTableLinear()  # 线性探测法
    hash_linear.build(words)

    current_nodes = hash_chain.get_all_nodes()  # 获取所有结点，用于排序

    while True:
        print("\n=========功能菜单=========")
        print("1.显示不同单词总数")
        print("2.查询单词（数组/哈希）")
        print("3.按词频排序显示前N个单词")
        print("4.生成词频柱状图")
        print("5.哈希表性能分析")
        print("6.按词语长度排序显示")
        print("7.按词频和长度排序显示")
        print("8.按词频 + 英文首字母排序")
        print("9.按词频 + 中文拼音首字母排序")
        print("10.Harry Potter 系列文本分析")
        print("0.退出")
        print("==========================")

        choice = input("请选择功能：").strip()  # 移除空白字符
        if choice == '1':
            print("不同单词数量：", len(current_nodes))

        elif choice == '2':  # 查找次数要对比一下
            target = input("请输入要查询的单词：").strip().lower()
            res_array, cmp_array = search_in_array(array_nodes, target)
            res_chain, cmp_chain = search_in_hash_chaining(hash_chain, target)
            res_linear, cmp_linear = search_in_hash_linear(hash_linear, target)
            print("\n-----查询结果-----")
            if res_array:
                print(f"数组:次数={res_array.count},首次位置={res_array.first_pos},比较次数={cmp_array}")
            else:
                print(f"数组:未找到,比较次数={cmp_array}")

            if res_chain:
                print(f"拉链哈希:次数={res_chain.count},首次位置={res_chain.first_pos},比较次数={cmp_chain}")
            else:
                print(f"拉链:未找到,比较次数={cmp_chain}")

            if res_linear:
                print(f"线性:次数={res_linear.count},首次位置={res_linear.first_pos},比较次数={cmp_linear}")
            else:
                print(f"线性:未找到,比较次数={cmp_linear}")

        elif choice == "3":  # 排序趟数也要对比一下
            n = input("请输入要查询的单词数量:").strip()
            n = int(n) if n.isdigit() else 10  # 如果输入非法数字就默认10个

            print("\n冒泡排序：")
            bubble_res, bubble_cmp, bubble_swap = sorter.bubble_sort(current_nodes)
            print(f"比较次数：{bubble_cmp}")
            print(f"交换次数：{bubble_swap}")
            print(f"词频前 {n} 个单词：")
            for node in bubble_res[:n]:
                print(node)

            print("\n插入排序：")
            insert_res, insert_cmp, insert_move = sorter.insertion_sort(current_nodes)
            print(f"比较次数：{insert_cmp}")
            print(f"移动次数：{insert_move}")
            # print(f"词频前 {n} 个单词：")
            # for node in insert_res[:n]:
            #     print(node)

            print("\n快速排序：")
            quick_res, quick_cmp = sorter.quick_sort(current_nodes)
            print(f"比较次数：{quick_cmp}")
            # print(f"词频前{n}个单词：")
            # for node in quick_res[:n]:
            #     print(node)

            print("\n三色旗快速排序：")
            sorted_nodes, cmp = sorter.quick_sort_dutch_flag(current_nodes)
            print(f"三色旗快速排序比较次数：{cmp}")

        elif choice == "4":  # 人如果想自己确定输出路径

            k = input("请输入要可视化的高频单词数量 N（默认 10）：").strip()
            k = int(k) if k.isdigit() else 10

            sorted_nodes, _ = sorter.quick_sort(current_nodes)

            image_path = get_next_image_path()
            draw_top_words(sorted_nodes, top_n=k, save_path=image_path)
            print(f"词频柱状图已保存为：{image_path}")

            # export_path = f"output/top_{k}_words.txt"
            # export_words(sorted_nodes[:k], export_path)
            # 自动生成高频词导出文件名
            export_path = get_next_export_path()
            export_words(sorted_nodes[:k], export_path)

            print(f"高频词已导出到文件：{export_path}")

        elif choice == "5":
            print("\n====== 哈希表性能分析 ======")

            total_cmp_chain = 0
            total_cmp_linear = 0
            total_searches = len(current_nodes)

            for node in current_nodes:
                _, cmp_chain = search_in_hash_chaining(hash_chain, node.word)
                _, cmp_linear = search_in_hash_linear(hash_linear, node.word)

                total_cmp_chain += cmp_chain
                total_cmp_linear += cmp_linear

            asl_chain = total_cmp_chain / total_searches
            asl_linear = total_cmp_linear / total_searches

            alpha_chain = total_searches / hash_chain.size
            alpha_linear = total_searches / hash_linear.size

            print("\n拉链法哈希表：")
            print(f"哈希表容量：{hash_chain.size}")
            print(f"装载因子 α：{alpha_chain:.2f}")
            print(f"冲突次数：{hash_chain.conflicts}")
            print(f"平均查找长度ASL：{asl_chain:.2f}")

            print("\n线性探测哈希表：")
            print(f"哈希表容量：{hash_linear.size}")
            print(f"装载因子 α：{alpha_linear:.2f}")
            print(f"冲突次数：{hash_linear.conflicts}")
            print(f"平均查找长度ASL：{asl_linear:.2f}")

        elif choice == "6":
            n = input("请输入要显示的词语数量 N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            order = input("请选择排序方式：1-从长到短  2-从短到长：").strip()
            reverse = True if order != "2" else False

            sorted_len = sorter.sort_by_word_length(current_nodes, reverse=reverse)

            print("\n按词语长度排序结果：")
            for node in sorted_len[:n]:
                print(f"{node.word} (长度={len(node.word)}, 次数={node.count})")

        elif choice == "7":
            n = input("请输入要显示的单词数量 N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            sorted_nodes = sorter.sort_by_freq_then_length(current_nodes)

            print("\n按“词频 + 词语长度”二级排序结果：")
            for node in sorted_nodes[:n]:
                print(f"{node.word} | 次数={node.count} | 长度={len(node.word)}")

        elif choice == "8":
            n = input("请输入要显示的单词数量 N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            sorted_nodes = sorter.sort_by_freq_then_alpha(current_nodes)

            print("\n按【词频 + 英文首字母】排序结果：")
            for node in sorted_nodes[:n]:
                print(f"{node.word} | 次数={node.count}")

        elif choice == "9":
            n = input("请输入要显示的词语数量 N（默认 10）：").strip()
            n = int(n) if n.isdigit() else 10

            sorted_nodes = sorter.sort_by_freq_then_pinyin(current_nodes)

            print("\n按【词频 + 中文拼音首字母】排序结果：")
            for node in sorted_nodes[:n]:
                print(f"{node.word} | 次数={node.count}")

        elif choice == "10":
            print("\n====== Harry Potter 系列分析 ======")
            print("1.统计 1-7 中单词量最少的一部")
            print("2.查看某一部的高频单词（Top-N）")
            sub_choice = input("请选择功能：").strip()
            if sub_choice == "1":
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

                    word_count = len(words)
                    # print(f"第 {idx} 部：《{filename}》 单词总数：{word_count}")

                    line = f"{idx}. {filename} : {word_count}"
                    print(line)
                    summary_lines.append(line)

                    if min_count is None or word_count < min_count:
                        min_count = word_count
                        min_book = filename

                print("\n单词量最少的一部是：")
                print(f"{min_book}（共 {min_count} 个单词）")
                export_path = get_next_hp_export_path("hp_word_count_summary")
                export_hp_word_count(summary_lines, min_book, min_count, export_path)

                print(f"\n统计结果已导出到文件：{export_path}")

            elif sub_choice == "2":
                print("\n请选择要分析的书籍：")
                for idx, name in harry_books.items():
                    print(f"{idx}. {name}")

                book_choice = input("请输入书号（1-7）：").strip()
                if not book_choice.isdigit() or int(book_choice) not in harry_books:
                    print("输入无效。")
                    return

                book_choice = int(book_choice)
                filename = harry_books[book_choice]
                path = f"data/{filename}"

                n = input("请输入要查看的高频单词数量（默认 10）：").strip()
                n = int(n) if n.isdigit() else 10
                text = load_text(path)

                words = split_text(
                    text,
                    mode="english",
                    zh_method="rule"
                )

                nodes = count_words_array(words)

                sorted_nodes, _ = sorter.quick_sort(nodes)

                print(f"\n《{filename}》中出现频率前 {n} 的单词：")
                for node in sorted_nodes[:n]:
                    print(f"{node.word} : {node.count}")
                export_path = get_next_hp_export_path(
                    f"hp_top_words_book{book_choice}_top{n}"
                )
                export_hp_top_words(filename, sorted_nodes, n, export_path)

                print(f"\n高频词结果已导出到文件：{export_path}")

        elif choice == "0":
            print("已退出系统 。")
            break

        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()
