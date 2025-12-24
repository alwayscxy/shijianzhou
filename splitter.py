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


def split_chinese_rule(text):  # 基于简单规则的中文分词：连续汉字作为一个词
    words = []
    current = ""

    for ch in text:
        if is_chinese_char(ch):
            current += ch
        else:
            if current:
                words.append(current)
                current = ""

    if current:
        words.append(current)
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
