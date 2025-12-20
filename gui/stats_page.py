import tkinter as tk
from tkinter import ttk


class StatsPage(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context

        self.build_ui()

    def build_ui(self):
        # ===== 标题 =====
        title = tk.Label(
            self,
            text="基本统计信息",
            font=("微软雅黑", 16, "bold")
        )
        title.pack(pady=20)

        # ===== 信息区域 =====
        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)

        # 从 context 取数据
        total_words = len(self.context["words"])
        unique_words = len(self.context["current_nodes"])
        mode = self.context["mode"]
        zh_method = self.context["zh_method"]

        stats = [
            ("总词数", total_words),
            ("不同词数", unique_words),
            ("分词模式", mode),
            ("中文分词方式", zh_method),
        ]

        for label, value in stats:
            row = tk.Frame(info_frame)
            row.pack(anchor="w", pady=5)

            tk.Label(
                row,
                text=f"{label}：",
                width=15,
                anchor="w",
                font=("微软雅黑", 11)
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("微软雅黑", 11, "bold")
            ).pack(side="left")

        # ===== 提示说明 =====
        tip = tk.Label(
            self,
            text="提示：这些数据来自初始化阶段的分词与统计结果",
            fg="gray"
        )
        tip.pack(pady=20)
