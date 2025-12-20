import tkinter as tk

from gui.stats_page import StatsPage
from gui.search_page import SearchPage
from gui.sort_page import SortPage
from gui.visualize_page import VisualizePage
from gui.hp_page import HarryPotterPage


class MainLayout(tk.Frame):
    """
    主界面布局 + 页面切换控制
    """

    def __init__(self, root, context):
        super().__init__(root)
        self.root = root
        self.context = context
        self.pages = {}

        self._build_layout()
        self._create_pages()
        self.show_page("stats")

    # =========================
    # 页面整体布局
    # =========================
    def _build_layout(self):
        self.pack(fill="both", expand=True)

        # 左侧菜单
        self.menu_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        self.menu_frame.pack(side="left", fill="y")

        # 右侧内容区
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self._build_menu()

    # =========================
    # 左侧菜单
    # =========================
    def _build_menu(self):
        tk.Label(
            self.menu_frame,
            text="功能菜单",
            font=("微软雅黑", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=15)

        buttons = [
            ("基本统计", "stats"),
            ("查找对比", "search"),
            ("排序分析", "sort"),
            ("可视化 / 导出", "visualize"),
            ("Harry Potter 分析", "hp"),
        ]

        for text, key in buttons:
            tk.Button(
                self.menu_frame,
                text=text,
                width=18,
                command=lambda k=key: self.show_page(k)
            ).pack(pady=5)

    # =========================
    # 创建所有页面
    # =========================
    def _create_pages(self):
        self.pages["stats"] = StatsPage(
            self.content_frame, self.context
        )
        self.pages["search"] = SearchPage(
            self.content_frame, self.context
        )
        self.pages["sort"] = SortPage(
            self.content_frame, self.context
        )
        self.pages["visualize"] = VisualizePage(
            self.content_frame, self.context
        )
        self.pages["hp"] = HarryPotterPage(
            self.content_frame
        )

        for page in self.pages.values():
            page.place(
                relx=0, rely=0, relwidth=1, relheight=1
            )

    # =========================
    # 页面切换
    # =========================
    def show_page(self, key):
        page = self.pages.get(key)
        if page:
            page.tkraise()
