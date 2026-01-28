import tkinter as tk
from tkinter import messagebox

from controllers.sort_controller import (
    compare_sort_algorithms,
    sort_by_rule,
    analyze_sort_performance_by_scale   # ⭐ 新增（B 用）
)

from controllers.visualize_controller import (
    visualize_sort_performance_curve    # ⭐ 新增（B 用）
)


class SortPage(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self._build_ui()

    def _build_ui(self):
        # ===== 标题 =====
        tk.Label(
            self,
            text="排序算法分析",
            font=("微软雅黑", 16, "bold")
        ).pack(pady=10)

        # ===== 控制区 =====
        ctrl = tk.Frame(self)
        ctrl.pack(pady=5)

        tk.Label(ctrl, text="Top-N：").pack(side="left")
        self.n_entry = tk.Entry(ctrl, width=6)
        self.n_entry.insert(0, "20")
        self.n_entry.pack(side="left", padx=5)

        self.rule_var = tk.StringVar(value="freq")
        tk.OptionMenu(
            ctrl,
            self.rule_var,
            "freq",
            "freq_alpha",
            "freq_length"
        ).pack(side="left", padx=10)

        tk.Button(
            ctrl,
            text="开始分析",
            command=self.run
        ).pack(side="left")

        # ===== 输出区 =====
        self.output = tk.Text(self, width=100, height=20)
        self.output.pack(pady=10)

        # ======================================================
        # ⭐ 新增：排序算法「规模 - 性能」分析（B）
        # ======================================================
        tk.Label(
            self,
            text="排序算法规模-性能分析（B）",
            font=("微软雅黑", 12, "bold")
        ).pack(pady=6)

        scale_frame = tk.Frame(self)
        scale_frame.pack(pady=5)

        tk.Button(
            scale_frame,
            text="规模 vs 时间（折线图）",
            command=lambda: self.show_sort_scale_curve("time")
        ).pack(side="left", padx=10)

        tk.Button(
            scale_frame,
            text="规模 vs 比较次数（折线图）",
            command=lambda: self.show_sort_scale_curve("comparisons")
        ).pack(side="left", padx=10)

    # ======================================================
    # 原有功能：排序算法对比 + 规则排序
    # ======================================================
    def run(self):
        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "Top-N 必须是整数")
            return

        self.output.delete("1.0", tk.END)

        report = compare_sort_algorithms(
            self.context["current_nodes"],
            n
        )

        self.output.insert(tk.END, "算法性能对比：\n")
        for name, info in report.items():
            self.output.insert(
                tk.END,
                f"{name}: {info['time']:.2f} ms，比较次数={info['comparisons']}\n"
            )

        self.output.insert(tk.END, "\n排序结果：\n")

        final = sort_by_rule(
            self.context["current_nodes"],
            self.rule_var.get()
        )

        for i, node in enumerate(final[:n], 1):
            self.output.insert(
                tk.END,
                f"{i:02d}. {node.word} ：{node.count}次\n"
            )

    # ======================================================
    # ⭐ 新增功能 B：排序算法随规模变化的性能曲线
    # ======================================================
    def show_sort_scale_curve(self, metric):
        """
        metric: 'time' or 'comparisons'
        """
        try:
            nodes = self.context["current_nodes"]

            perf_data = analyze_sort_performance_by_scale(nodes)

            visualize_sort_performance_curve(
                perf_data,
                metric=metric,
                show=True
            )

        except Exception as e:
            messagebox.showerror("排序规模分析失败", str(e))
