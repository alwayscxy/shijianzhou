import tkinter as tk
from tkinter import messagebox

from controllers.hp_controller import (
    analyze_min_word_book,
    analyze_top_words_of_book
)

HARRY_BOOKS = {
    1: "Harry Potter 1 - Harry Potter and the Philosophers Stone.txt",
    2: "Harry Potter 2 - Harry Potter and the Chamber of Secrets.txt",
    3: "Harry Potter 3 - Harry Potter and the Prisoner of Azkaban.txt",
    4: "Harry Potter 4 - Harry Potter and the Goblet of Fire.txt",
    5: "Harry Potter 5 - Harry Potter and the Order of the Phoenix.txt",
    6: "Harry Potter 6 - Harry Potter and the Half-Blood Prince.txt",
    7: "Harry Potter 7 - Harry Potter and the Deathly Hallows.txt",
}


class HarryPotterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self,
            text="Harry Potter 系列文本分析",
            font=("微软雅黑", 16, "bold")
        ).pack(pady=15)

        self._build_min_section()
        tk.Frame(self, height=2, bd=1, relief="sunken").pack(fill="x", pady=20)
        self._build_top_section()

    # ========= 功能一 =========
    def _build_min_section(self):
        frame = tk.Frame(self)
        frame.pack()

        tk.Label(frame, text="① 单词量最少的一部", font=("微软雅黑", 12, "bold")).pack(anchor="w")  # 左对齐

        tk.Button(
            frame,
            text="开始统计",
            width=20,
            command=self.run_min_analysis
        ).pack(pady=10)

        self.min_text = tk.Text(frame, height=8, width=100)
        self.min_text.pack()

    def run_min_analysis(self):
        try:
            result = analyze_min_word_book(HARRY_BOOKS)
            self.min_text.delete("1.0", tk.END)

            self.min_text.insert(tk.END, "各部单词总数：\n")
            for idx, name, cnt in result["details"]:
                self.min_text.insert(
                    tk.END, f"  第 {idx} 部：{cnt} 词\n"
                )

            idx, name, cnt = result["min_book"]
            self.min_text.insert(
                tk.END,
                f"\n结论：单词量最少的是：第 {idx} 部\n{name}\n共 {cnt} 个单词\n"
            )
            self.min_text.insert(
                tk.END,
                f"\n结果已导出到：\n{result['export_path']}"
            )

        except Exception as e:
            messagebox.showerror("分析失败", str(e))

    # 功能二
    def _build_top_section(self):
        frame = tk.Frame(self)
        frame.pack()

        tk.Label(frame, text="② 查看某一部的高频词", font=("微软雅黑", 12, "bold")).pack(anchor="w")

        control = tk.Frame(frame)
        control.pack(pady=5)

        self.book_var = tk.IntVar(value=1)
        tk.OptionMenu(control, self.book_var, *HARRY_BOOKS.keys()).pack(side="left")

        self.n_entry = tk.Entry(control, width=6)
        self.n_entry.insert(0, "10")
        self.n_entry.pack(side="left", padx=10)

        tk.Button(
            frame,
            text="分析高频词",
            width=20,
            command=self.run_top_analysis
        ).pack(pady=10)

        self.top_text = tk.Text(frame, height=10, width=100)
        self.top_text.pack()

    def run_top_analysis(self):
        book_idx = self.book_var.get()
        n = int(self.n_entry.get()) if self.n_entry.get().isdigit() else 10

        try:
            result = analyze_top_words_of_book(HARRY_BOOKS, book_idx, n)
            self.top_text.delete("1.0", tk.END)

            self.top_text.insert(
                tk.END,
                f"{result['book']} 高频词分析（已过滤停用词）\n\n"
            )

            self.top_text.insert(
                tk.END,
                f"总词数：{result['total_words']}\n"
                f"不同词数：{result['unique_words']}\n"
                f"不同词占比：{result['ratio']:.2%}\n\n"
            )

            for i, (word, count) in enumerate(result["top_words"], 1):
                self.top_text.insert(
                    tk.END, f"{i:02d}. {word:<15} {count}\n"
                )

            self.top_text.insert(
                tk.END,
                f"\n结果已导出到：\n{result['export_path']}"
            )

        except Exception as e:
            messagebox.showerror("分析失败", str(e))
