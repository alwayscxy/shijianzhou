import tkinter as tk
from tkinter import filedialog, messagebox
import os

from controllers.init_controller import init_system

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class InitPage(tk.Frame):
    """
    初始化页面：
    - 选择文本文件
    - 选择分词方式
    - 点击开始 → 初始化系统 → 切换到主功能页面
    """

    def __init__(self, parent, on_init_success):
        super().__init__(parent)
        self.on_init_success = on_init_success  # 回调函数
        self.file_path = None
        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self,
            text="文本词频统计系统",
            font=("微软雅黑", 18, "bold")
        ).pack(pady=30)

        # ===== 文件选择 =====
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10)

        tk.Label(file_frame, text="选择文本文件：").pack(side="left")
        self.file_label = tk.Label(file_frame, text="未选择", width=50, anchor="w")
        self.file_label.pack(side="left", padx=10)

        tk.Button(
            file_frame,
            text="浏览...",
            command=self.choose_file
        ).pack(side="left")

        # ===== 分词方式 =====
        tk.Label(self, text="选择分词方式：", font=("微软雅黑", 12)).pack(pady=15)

        self.mode_var = tk.StringVar(value="mixed_rule")

        options = [
            ("仅英文分词", "english"),
            ("仅中文分词（规则）", "chinese_rule"),
            ("仅中文分词（jieba）", "chinese_jieba"),
            ("中英混合（规则）", "mixed_rule"),
            ("中英混合（jieba）", "mixed_jieba"),
        ]

        for text, value in options:
            tk.Radiobutton(
                self,
                text=text,
                variable=self.mode_var,
                value=value
            ).pack(anchor="w", padx=300)

        # ===== 开始按钮 =====
        tk.Button(
            self,
            text="开始分析",
            font=("微软雅黑", 12, "bold"),
            width=20,
            command=self.start_init
        ).pack(pady=30)

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="请选择要分析的文本文件",
            initialdir=os.path.join(BASE_DIR, "data"),
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            self.file_path = path
            self.file_label.config(text=os.path.basename(path))

    def start_init(self):
        if not self.file_path:
            messagebox.showerror("错误", "请先选择文本文件")
            return

        token_choice = self.mode_var.get()

        if token_choice == "english":
            mode, zh_method = "english", "rule"
        elif token_choice == "chinese_rule":
            mode, zh_method = "chinese", "rule"
        elif token_choice == "chinese_jieba":
            mode, zh_method = "chinese", "jieba"
        elif token_choice == "mixed_jieba":
            mode, zh_method = "mixed", "jieba"
        else:
            mode, zh_method = "mixed", "rule"

        try:
            context = init_system(
                file_path=self.file_path,
                mode=mode,
                zh_method=zh_method
            )
        except Exception as e:
            messagebox.showerror("初始化失败", str(e))
            return

        # 初始化成功，交给主界面
        self.on_init_success(context)
