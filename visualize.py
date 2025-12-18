import matplotlib.pyplot as plt
import os

def draw_top_words(nodes, top_n=10, save_path=None): # nodes:排好序的wordnode列表，top_n展示几个单词，save_path存放路径
    top_nodes = nodes[:top_n]
    words = [node.word for node in top_nodes]
    counts = [node.count for node in top_nodes]
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel("word")
    plt.ylabel("frequency")
    plt.title(f"Top {top_n} Word Frequencies")
    plt.xticks(rotation=45)  # 让单词斜过来，防止重叠
    plt.tight_layout()  # 自动调整布局
    if save_path:
        plt.savefig(save_path)  # 保存到相应路径
    plt.show()

def get_next_image_path():
    output_dir = "output" #保存的文件夹
    if not os.path.exists(output_dir):#如果不存在这个文件夹，就创建一个新的
        os.mkdir(output_dir)

    index = 1
    while True:
        path = os.path.join(output_dir, f"freq_chart_{index}.png") #跨平台兼容的路径拼接
        if not os.path.exists(path):
            return path
        index += 1
