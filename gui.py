import tkinter as tk


def main():
    root = tk.Tk()
    root.title("文本词频统计系统")
    root.geometry("800x600")

    label = tk.Label(root, text="欢迎使用文本词频统计系统", font=("微软雅黑", 16))
    label.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
