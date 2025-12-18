# 负责文本文件的读取和预处理，全部转为小写，去除非字母
import re


# def load_text(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         text = f.read()
#     text = text.lower()  # 转为小写
#     text = re.sub(r'[^a-z\s]', ' ', text)  # 正则表达式，非字母的转为空格
#     return text
# 负责文本文件的读取（不做语言相关清洗）
def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text
