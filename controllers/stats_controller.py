def show_basic_statistics(context):
    """
    显示文本的基础统计信息
    """
    words = context["words"]
    current_nodes = context["current_nodes"]
    mode = context["mode"]
    zh_method = context["zh_method"]

    print("\n====== 文本基础统计信息 ======")
    print(f"分词模式：{mode}")
    print(f"中文分词方式：{zh_method}")
    print(f"文本总词数：{len(words)}")
    print(f"不同单词数量：{len(current_nodes)}")
    print("==============================\n")
