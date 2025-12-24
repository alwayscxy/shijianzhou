import tkinter as tk
from tkinter import filedialog, messagebox  # 文本选择对话框和弹窗
import os

from controllers.init_controller import init_system
from gui.layout import MainLayout


# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 选择文本文件
def choose_text_file():
    return filedialog.askopenfilename(  # 选择文件对话框
        title="请选择要分析的文本文件",
        initialdir=os.path.join(BASE_DIR, "data"),
        filetypes=[("Text Files", "*.txt")]  # 只允许选择txt文件，防止出错。返回文件完整路径（字符串）
    )


# 选择分词方式
def choose_token_mode(root):
    win = tk.Toplevel(root)  # 子窗口，弹窗，不会关闭主窗口
    win.title("请选择分词方式")
    win.geometry("400x300")

    mode_var = tk.StringVar(value="mixed_rule")  # 默认中英混合规则。

    options = [
        ("仅英文分词", "english"),
        ("仅中文分词（规则）", "chinese_rule"),
        ("仅中文分词（jieba）", "chinese_jieba"),
        ("中英混合（规则）", "mixed_rule"),
        ("中英混合（jieba）", "mixed_jieba"),
    ]

    for text, value in options:
        tk.Radiobutton(
            win, text=text, variable=mode_var, value=value
        ).pack(anchor="w", padx=20, pady=5)  # 把值存入了mode_var变量

    result = {}

    def confirm():
        result["mode"] = mode_var.get()  # 把用户选择的规则存入result字典
        win.destroy()

    tk.Button(win, text="确认", command=confirm).pack(pady=20)

    win.grab_set()  # 必须让用户操作这个窗口，不能操作别的
    win.wait_window()  # 阻塞程序，等待窗口关闭

    return result.get("mode")


# 主程序入口
def main():
    root = tk.Tk()  # 创建主窗口
    root.withdraw()  # 初始化阶段隐藏窗口

    #  选择文件
    file_path = choose_text_file()
    if not file_path:
        messagebox.showerror("错误", "未选择文件，程序退出")
        return

    # 选择分词方式
    token_choice = choose_token_mode(root)
    if not token_choice:
        messagebox.showerror("错误", "未选择分词方式")
        return

    # 解析分词参数
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

    #  初始化系统
    try:
        context = init_system(
            file_path=file_path,
            mode=mode,
            zh_method=zh_method
        )
    except Exception as e:
        messagebox.showerror("初始化失败", str(e))
        return

    # 显示主界面 + 交给 Layout
    root.deiconify()  # 显示刚刚隐藏的窗口
    root.title("文本词频统计系统")
    root.geometry("1100x650")

    MainLayout(root, context)

    root.mainloop()  # 启动主事件循环，不然窗口一闪就没了


if __name__ == "__main__":
    main()
