import tkinter as tk
from tkinter import messagebox

from controllers.search_controller import (
    search_word,
    hash_performance_analysis
)


class SearchPage(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self,
            text="单词查找方法对比",
            font=("微软雅黑", 16, "bold")
        ).pack(pady=15)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="查询单词：").pack(side="left")
        self.word_entry = tk.Entry(input_frame, width=30)
        self.word_entry.pack(side="left", padx=10)

        tk.Button(
            input_frame,
            text="查找",
            command=self.do_search
        ).pack(side="left")

        self.result_text = tk.Text(self, width=90, height=18)
        self.result_text.pack(pady=10)

        tk.Button(
            self,
            text="查看哈希表性能分析",
            command=self.show_hash_performance
        ).pack(pady=10)

    def do_search(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            messagebox.showwarning("提示", "请输入单词")
            return

        ctx = self.context
        result = search_word(
            word,
            ctx["array_nodes"],
            ctx["hash_chain"],
            ctx["hash_linear"]
        )

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"查询单词：{word}\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")

        for method, info in result.items():
            self.result_text.insert(tk.END, f"{method}：\n")
            if info["found"]:
                self.result_text.insert(
                    tk.END,
                    f"  次数：{info['count']}\n"
                    f"  首次位置：{info['first_pos']}\n"
                )
            else:
                self.result_text.insert(tk.END, "  未找到\n")

            self.result_text.insert(
                tk.END,
                f"  比较次数：{info['comparisons']}\n\n"
            )
        self.result_text.insert(tk.END, "\n【哈希查找细节】\n")

        hc = result["hash_chain"]["detail"]
        self.result_text.insert(
            tk.END,
            f"拉链法：哈希地址={hc['hash_index']}，链长={hc['chain_length']}，比较={hc['comparisons']}\n"
        )

        hl = result["hash_linear"]["detail"]
        self.result_text.insert(
            tk.END,
            f"线性探测：初始地址={hl['hash_index']}，命中地址={hl['hit_index']}，探测步数={hl['probe_steps']}\n"
        )

    def show_hash_performance(self):
        ctx = self.context
        perf = hash_performance_analysis(
            ctx["current_nodes"],
            ctx["hash_chain"],
            ctx["hash_linear"]
        )

        msg = (
            "拉链法哈希表：\n"
            f"  装载因子 α：{perf['chain']['alpha']:.2f}\n"
            f"  冲突次数：{perf['chain']['conflicts']}\n"
            f"  ASL：{perf['chain']['asl']:.2f}\n\n"
            "线性探测哈希表：\n"
            f"  装载因子 α：{perf['linear']['alpha']:.2f}\n"
            f"  冲突次数：{perf['linear']['conflicts']}\n"
            f"  ASL：{perf['linear']['asl']:.2f}"
        )

        messagebox.showinfo("哈希表性能分析", msg)
