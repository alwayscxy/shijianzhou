import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # 把matplotlib图嵌入Tkinter
from matplotlib.figure import Figure

from controllers.visualize_controller import visualize_top_words


class VisualizePage(tk.Frame):
    def __init__(self, master, context):
        super().__init__(master)
        self.context = context
        self.nodes = context["current_nodes"]
        self._build_ui()

    def _build_ui(self):
        # 顶部控制区
        ctrl = tk.Frame(self)
        ctrl.pack(fill="x", padx=10, pady=5)  # 水平方向拉满，左右留空，上下留空

        tk.Label(ctrl, text="Top-N：").pack(side="left")
        self.n_var = tk.StringVar(value="10")
        tk.Entry(ctrl, textvariable=self.n_var, width=6).pack(side="left")

        tk.Button(
            ctrl, text="生成可视化", command=self.visualize
        ).pack(side="left", padx=10)

        # 主内容区
        content = tk.Frame(self)
        content.pack(fill="both", expand=True)  # 拉满并扩展

        # 左：图像区
        self.fig_frame = tk.Frame(content)
        self.fig_frame.pack(
            side="left", fill="both", expand=True, padx=10, pady=5
        )

        # 右：文本区
        self.text = tk.Text(content, width=35)
        self.text.pack(side="right", fill="y", padx=10, pady=5)

    def visualize(self):
        try:
            n = int(self.n_var.get())
        except ValueError:
            messagebox.showerror("错误", "Top-N 必须是整数")
            return

        if n <= 0:
            messagebox.showerror("错误", "Top-N 必须大于 0")
            return

        # 调用 controller
        top_nodes = visualize_top_words(
            self.nodes,
            top_n=n,
            export=False,
            draw=False
        )

        # 更新右侧文本
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"Top {n} 高频词\n\n")

        for i, node in enumerate(top_nodes, start=1):
            self.text.insert(
                tk.END, f"{i:02d}. {node.word} ： {node.count}次\n"
            )

        # 更新左侧图像
        for w in self.fig_frame.winfo_children():
            w.destroy()

        fig = Figure(figsize=(6.5, 4.5))
        ax = fig.add_subplot(111)  # 创建子图，1行1列第1个

        words = [node.word for node in top_nodes]
        counts = [node.count for node in top_nodes]

        bars = ax.bar(words, counts)

        # 标题与坐标轴
        ax.set_title(f"Top {n} 高频词统计", fontsize=12)
        ax.set_xlabel("单词")
        ax.set_ylabel("出现次数")

        ax.tick_params(axis="x", rotation=45)  # X轴标签旋转45度

        # 柱顶显示数值
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        fig.tight_layout()  # 自动调整布局

        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)  # 将图嵌入Tkinter
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)  # 把图放入框架中，并填充
