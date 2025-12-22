def main():
    print("====== 文本分析系统 ======")
    print("请选择展示方式：")
    print("1. 命令行界面（CLI）")
    print("2. 图形界面（GUI）")

    choice = input("请输入选项（1/2）：").strip()

    if choice == "1":
        import app_cli
        app_cli.main()
    elif choice == "2":
        from gui.app import main as gui_main
        gui_main()
    else:
        print("输入无效，程序退出")


if __name__ == "__main__":
    main()
