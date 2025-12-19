from loader import load_text
from splitter import split_text
from array_counter import count_words_array
from hash_chaining import HashTableChaining
from hash_linear import HashTableLinear


def choose_tokenizer():
    print("\n请选择分词方式：")
    print("1. 仅英文分词")
    print("2. 仅中文分词（规则）")
    print("3. 仅中文分词（jieba）")
    print("4. 中英混合（规则）")
    print("5. 中英混合（jieba）")

    choice = input("请输入选项（1-5）：").strip()

    if choice == "1":
        return "english", "rule"
    elif choice == "2":
        return "chinese", "rule"
    elif choice == "3":
        return "chinese", "jieba"
    elif choice == "4":
        return "mixed", "rule"
    elif choice == "5":
        return "mixed", "jieba"
    else:
        print("输入无效，默认使用：中英混合 + 规则分词")
        return "mixed", "rule"


def init_system(filepath):
    text = load_text(filepath)  # 读取文本

    mode, zh_method = choose_tokenizer()  # 用户选择分词方式

    words = split_text(text, mode=mode, zh_method=zh_method)  # 分词

    print(f"\n分词完成：模式={mode}，中文方式={zh_method}")
    print(f"共得到 {len(words)} 个词语。\n")

    array_nodes = count_words_array(words)  # 数组方式统计词频

    hash_chain = HashTableChaining()  # 构建拉链法哈希表
    hash_chain.build(words)

    hash_linear = HashTableLinear()  # 构建线性探测哈希表
    hash_linear.build(words)

    current_nodes = hash_chain.get_all_nodes()  # 获取所有词频结点（用于排序）

    context = {  # 打包系统上下文
        "text": text,
        "words": words,
        "array_nodes": array_nodes,
        "hash_chain": hash_chain,
        "hash_linear": hash_linear,
        "current_nodes": current_nodes,
        "mode": mode,
        "zh_method": zh_method,
    }

    return context
