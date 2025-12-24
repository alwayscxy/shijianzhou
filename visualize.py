# visualize.py
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager  # 用于设置中文字体


def _set_chinese_font():
    try:
        font_path = "C:/Windows/Fonts/simhei.ttf"  # 黑体字体路径
        if os.path.exists(font_path):
            font = font_manager.FontProperties(fname=font_path) # 创建字体对象，frame指定字体文件路径
            plt.rcParams["font.family"] = font.get_name()  # 设置全局字体
        else:
            plt.rcParams["font.family"] = "Microsoft YaHei"  # 微软雅黑（作为备选）plt.rcParams是Matplotlib的配置参数字典，"font.family" 键控制使用哪个字体族
        plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题，设置为False使用ASCII字符的负号
    except Exception:
        pass


_set_chinese_font()

# 输出路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前文件目录
OUTPUT_DIR = os.path.join(BASE_DIR, "output")  # 输出目录
IMG_DIR = os.path.join(OUTPUT_DIR, "images")  # 图片目录

os.makedirs(IMG_DIR, exist_ok=True)  # 创建图片目录（如果不存在）


def get_next_image_path(prefix="img"):  # 获取下一个可用的图片保存路径
    idx = 1
    while True:
        path = os.path.join(IMG_DIR, f"{prefix}_{idx}.png")
        if not os.path.exists(path):
            return path
        idx += 1


# 柱顶标注

def _label_bar_values(bars):
    for bar in bars:
        h = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x 坐标
            h,  # y 坐标
            f"{h:.2f}" if isinstance(h, float) else f"{int(h)}",# isinstance() 函数用于检查h是否为浮点数
            ha="center",  # 水平居中
            va="bottom",  # 垂直底部对齐
            fontsize=10  # 字体大小
        )


# 高频词柱状图

def draw_top_words(nodes, top_n=10, save_path=None, show=False):
    words = [n.word for n in nodes]
    counts = [n.count for n in nodes]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(words, counts)

    plt.title(f"Top {top_n} 高频词统计")
    plt.xlabel("单词")
    plt.ylabel("出现次数")
    plt.xticks(rotation=45, ha="right")  # x 轴标签旋转45度，右对齐

    _label_bar_values(bars)

    plt.tight_layout()  # 自动调整布局以防止标签重叠

    if save_path:
        plt.savefig(save_path, dpi=150) # 保存图片，分辨率为150
    if show:
        plt.show()

    plt.close()


# 当前单词：查找性能对比

def draw_search_performance(result, save_path=None, show=False):
    methods = []
    comparisons = []

    for k in ["array", "hash_chain", "hash_linear"]:
        methods.append(k)
        comparisons.append(result[k]["comparisons"])

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, comparisons)

    plt.title("当前单词查找性能对比（比较次数）")
    plt.xlabel("查找方法")
    plt.ylabel("比较次数")

    _label_bar_values(bars)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
    if show:
        plt.show()

    plt.close()


# 哈希表 ASL 对比图

def draw_hash_asl(perf, save_path=None, show=False):
    methods = ["拉链法", "线性探测"]
    asl_values = [
        perf["chain"]["asl"],
        perf["linear"]["asl"]
    ]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, asl_values)

    plt.title("哈希表 ASL 对比")
    plt.xlabel("哈希方法")
    plt.ylabel("平均查找长度（ASL）")

    _label_bar_values(bars)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
    if show:
        plt.show()

    plt.close()
