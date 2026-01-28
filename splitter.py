import re
import jieba


# 负责将清洗后的文本切分为单词列表
# def split_words(text):
#     words = text.split()  # 字符串来自loader
#     return words  # 单词列表
def split_english(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text.split()


def is_chinese_char(ch):
    return '\u4e00' <= ch <= '\u9fff'  # Unicode范围：\u4e00-\u9fff 是中文字符范围


def split_chinese_rule(text):
    """
    改进版中文规则分词（不依赖词典）

    改进点：
    1. 连续中文字符分段（保留原规则优点）
    2. 引入常见虚词作为切分点
    3. 对长中文段进行固定窗口切分（2-3 字优先）
    4. 保证时间复杂度为 O(n)

    输入 / 输出与原函数完全一致
    """

    def is_chinese_char(ch):
        return '\u4e00' <= ch <= '\u9fff'

    # 常见功能词（可解释）
    FUNCTION_WORDS = {
        "的", "了", "着", "过",
        "是", "在", "有",
        "和", "与", "或", "及",
        "而", "但", "却"
    }

    words = []
    segment = ""

    def split_long_segment(seg):
        """
        对较长中文段进行规则切分：
        优先 2 字，其次 3 字，最后 1 字
        """
        result = []
        i = 0
        while i < len(seg):
            # 2 字优先（中文中最常见）
            if i + 2 <= len(seg):
                result.append(seg[i:i+2])
                i += 2
            else:
                result.append(seg[i])
                i += 1
        return result

    for ch in text:
        if is_chinese_char(ch):
            segment += ch
        else:
            if segment:
                # 对连续中文段进行处理
                temp = ""
                for c in segment:
                    if c in FUNCTION_WORDS:
                        if temp:
                            words.extend(
                                split_long_segment(temp)
                                if len(temp) > 3 else [temp]
                            )
                            temp = ""
                        words.append(c)
                    else:
                        temp += c

                if temp:
                    words.extend(
                        split_long_segment(temp)
                        if len(temp) > 3 else [temp]
                    )

                segment = ""

    # 处理结尾残留
    if segment:
        words.extend(
            split_long_segment(segment)
            if len(segment) > 3 else [segment]
        )

    return words



def split_chinese_jieba(text):  # 基于jieba的分词
    words = []
    for w in jieba.cut(text):
        w = w.strip()
        if len(w) >= 2 and any(is_chinese_char(ch) for ch in w):
            words.append(w)
    return words


def split_text(text, mode="english", zh_method="rule"):
    words = []

    if mode == "english":
        words.extend(split_english(text))

    elif mode == "chinese":
        if zh_method == "rule":
            words.extend(split_chinese_rule(text))
        else:
            words.extend(split_chinese_jieba(text))

    elif mode == "mixed":
        words.extend(split_english(text))
        if zh_method == "rule":
            words.extend(split_chinese_rule(text))
        else:
            words.extend(split_chinese_jieba(text))

    return words
