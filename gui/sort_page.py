import tkinter as tk
from tkinter import messagebox

from controllers.sort_controller import (
    compare_sort_algorithms,
    sort_by_rule
)


class SortPage(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="排序算法分析", font=("微软雅黑", 16, "bold")).pack(pady=10)

        ctrl = tk.Frame(self)
        ctrl.pack(pady=5)

        tk.Label(ctrl, text="Top-N：").pack(side="left")
        self.n_entry = tk.Entry(ctrl, width=6)
        self.n_entry.insert(0, "20")  # 默认值20
        self.n_entry.pack(side="left", padx=5)

        self.rule_var = tk.StringVar(value="freq")  # 字符串盒子，用于保存选项，默认为词频
        tk.OptionMenu(
            ctrl,
            self.rule_var,
            "freq",
            "freq_alpha",
            "freq_length"
        ).pack(side="left", padx=10)

        tk.Button(ctrl, text="开始分析", command=self.run).pack(side="left")

        self.output = tk.Text(self, width=100, height=20)
        self.output.pack(pady=10)

    def run(self):
        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "Top-N 必须是整数")
            return

        self.output.delete("1.0", tk.END)

        report = compare_sort_algorithms(self.context["current_nodes"], n)

        self.output.insert(tk.END, "算法性能对比：\n")
        for name, info in report.items():
            self.output.insert(
                tk.END,
                f"{name}: {info['time']:.2f} ms，比较次数={info['comparisons']}\n"
            )

        self.output.insert(tk.END, "\n排序结果：\n")

        final = sort_by_rule(self.context["current_nodes"], self.rule_var.get())
        for i, node in enumerate(final[:n], 1):
            self.output.insert(tk.END, f"{i:02d}. {node.word} ：{node.count}次\n")
