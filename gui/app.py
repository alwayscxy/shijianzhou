import tkinter as tk
from gui.layout import MainLayout


def main():
    root = tk.Tk()
    root.title("文本词频统计系统")
    root.geometry("1100x650")

    MainLayout(root)

    root.mainloop()


if __name__ == "__main__":
    main()
