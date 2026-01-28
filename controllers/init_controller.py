from loader import load_text  # 读取文本
from splitter import split_text  # 分词
from array_counter import count_words_array  # 数组词频统计
from hash_chaining import HashTableChaining  # 拉链法哈希表实现词频统计等
from hash_linear import HashTableLinear  # 线性探测哈希表实现词频统计等

def choose_tokenizer():
    # CLI分词方式选择
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


def init_system(file_path, mode=None, zh_method=None):
    # 读取文本
    text = load_text(file_path)

    # 确定分词方式
    if mode is None or zh_method is None:
        # CLI 模式
        mode, zh_method = choose_tokenizer()

    # 分词
    words = split_text(text, mode=mode, zh_method=zh_method)

    print(f"\n分词完成：模式={mode}，中文方式={zh_method}")
    print(f"共得到 {len(words)} 个词语。\n")

    # 数组统计
    array_nodes = count_words_array(words)

    # 拉链法哈希表
    hash_chain = HashTableChaining()
    hash_chain.build(words)

    # 线性探测哈希表
    hash_linear = HashTableLinear()
    hash_linear.build(words)

    # 所有结点（用于排序）
    current_nodes = hash_chain.get_all_nodes()

    # 上下文打包（核心）
    context = {
        "file_path": file_path,
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
