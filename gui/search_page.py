import tkinter as tk
from tkinter import messagebox

from controllers.search_controller import (
    search_word,
    hash_performance_analysis,
    analyze_word_context
)

from controllers.visualize_controller import (
    visualize_search_performance,
    visualize_hash_asl,
    visualize_context_words      # ⭐ 新增：上下文分析可视化
)


class SearchPage(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context

        # ⭐ 新增：缓存最近一次上下文分析结果
        self._last_context_result = None
        self._last_context_word = None

        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self,
            text="单词查找方法与词频对比分析",
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

        tk.Button(
            input_frame,
            text="上下文分析",
            command=self.do_context_analysis
        ).pack(side="left", padx=10)

        # ⭐ 新增：上下文分析柱状图按钮
        tk.Button(
            input_frame,
            text="上下文柱状图",
            command=self.show_context_visual
        ).pack(side="left", padx=10)

        self.result_text = tk.Text(self, width=90, height=20)
        self.result_text.pack(pady=10)

        tk.Button(
            self,
            text="查看哈希表性能分析",
            command=self.show_hash_performance
        ).pack(pady=10)

        tk.Button(
            self,
            text="可视化当前查找性能",
            command=self.show_search_visual
        ).pack(pady=5)

        tk.Button(
            self,
            text="可视化哈希表 ASL 对比",
            command=self.show_asl_visual
        ).pack(pady=5)

    # =====================================================
    # 单词查找
    # =====================================================
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
        self.result_text.insert(tk.END, "【说明】出现次数即该单词在全文中的词频\n\n")
        self.result_text.insert(tk.END, f"查询单词：{word}\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n")

        for method, info in result.items():
            self.result_text.insert(tk.END, f"{method}：\n")

            if info["found"]:
                self.result_text.insert(
                    tk.END,
                    f"  是否找到：是\n"
                    f"  出现次数（词频）：{info['count']}\n"
                    f"  首次出现位置：{info['first_pos']}\n"
                )
            else:
                self.result_text.insert(
                    tk.END,
                    "  是否找到：否\n"
                    "  出现次数（词频）：0\n"
                )

            self.result_text.insert(
                tk.END,
                f"  比较次数：{info['comparisons']}\n\n"
            )

        self.result_text.insert(tk.END, "【哈希查找细节】\n")

        hc = result["hash_chain"]["detail"]
        self.result_text.insert(
            tk.END,
            f"拉链法：哈希地址={hc['hash_index']}，"
            f"链长={hc['chain_length']}，"
            f"比较次数={hc['comparisons']}\n"
        )

        hl = result["hash_linear"]["detail"]
        self.result_text.insert(
            tk.END,
            f"线性探测：初始地址={hl['hash_index']}，"
            f"命中地址={hl['hit_index']}，"
            f"探测步数={hl['probe_steps']}\n"
        )

    # =====================================================
    # 哈希表性能（文本）
    # =====================================================
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

    # =====================================================
    # 上下文分析（文本）
    # =====================================================
    def do_context_analysis(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            messagebox.showwarning("提示", "请输入单词")
            return

        try:
            result = analyze_word_context(
                word,
                self.context["words"],
                window_size=100,
                top_n=20
            )
        except Exception as e:
            messagebox.showerror("分析失败", str(e))
            return

        # ⭐ 缓存结果，供可视化使用
        self._last_context_result = result
        self._last_context_word = word

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "【词语关联性分析（上下文分析）】\n\n")
        self.result_text.insert(tk.END, f"目标词：{word}\n")
        self.result_text.insert(
            tk.END,
            f"出现次数：{result['total_occurrences']}\n"
            f"上下文窗口：±{result['window_size']} 词\n"
        )
        self.result_text.insert(
            tk.END,
            "已过滤停用词（部分）："
            + ", ".join(result["removed_stopwords"][:10])
            + "\n"
        )
        self.result_text.insert(tk.END, "-" * 70 + "\n")

        for w, cnt in result["context_words"]:
            self.result_text.insert(
                tk.END,
                f"{w:<15} {cnt}\n"
            )

    # =====================================================
    # ⭐ 上下文分析结果可视化
    # =====================================================
    def show_context_visual(self):
        if not self._last_context_result:
            messagebox.showwarning(
                "提示",
                "请先执行一次“上下文分析”"
            )
            return

        visualize_context_words(
            self._last_context_result["context_words"],
            self._last_context_word,
            show=True
        )

    # =====================================================
    # 查找性能可视化
    # =====================================================
    def show_search_visual(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            messagebox.showwarning("提示", "请先输入要查找的单词")
            return

        result = search_word(
            word,
            self.context["array_nodes"],
            self.context["hash_chain"],
            self.context["hash_linear"]
        )

        visualize_search_performance(result, show=True)

    # =====================================================
    # 哈希 ASL 可视化
    # =====================================================
    def show_asl_visual(self):
        perf = hash_performance_analysis(
            self.context["current_nodes"],
            self.context["hash_chain"],
            self.context["hash_linear"]
        )

        visualize_hash_asl(perf, show=True)
