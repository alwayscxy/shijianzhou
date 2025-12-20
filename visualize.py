# visualize.py
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

# =============================
# 中文字体设置（Windows 优先）
# =============================
def _set_chinese_font():
    try:
        font_path = "C:/Windows/Fonts/simhei.ttf"
        if os.path.exists(font_path):
            font = font_manager.FontProperties(fname=font_path)
            plt.rcParams["font.family"] = font.get_name()
        else:
            # 兜底方案
            plt.rcParams["font.family"] = "Microsoft YaHei"
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        pass


_set_chinese_font()


# =============================
# 路径生成
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
IMG_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(IMG_DIR, exist_ok=True)


def get_next_image_path():
    idx = 1
    while True:
        path = os.path.join(IMG_DIR, f"top_words_{idx}.png")
        if not os.path.exists(path):
            return path
        idx += 1


# =============================
# 绘图函数（核心）
# =============================
def draw_top_words(nodes, top_n=10, save_path=None, show=False):
    words = [n.word for n in nodes]
    counts = [n.count for n in nodes]

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)

    plt.title(f"Top {top_n} 高频词统计", fontsize=14)
    plt.xlabel("单词")
    plt.ylabel("出现次数")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)

    if show:
        plt.show()

    plt.close()
