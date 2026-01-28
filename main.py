import os
from controllers.init_controller import init_system


def choose_file_cli(data_dir="data"):
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在：{data_dir}")
        return None

    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

    if not files:
        print("❌ data 目录下没有 txt 文件")
        return None

    print("\n可分析的文本文件：")
    for idx, name in enumerate(files, start=1):
        print(f"{idx}. {name}")

    choice = input("请选择文件编号：").strip()

    if not choice.isdigit():
        print("❌ 输入非法")
        return None

    idx = int(choice) - 1
    if idx < 0 or idx >= len(files):
        print("❌ 编号超出范围")
        return None

    return os.path.join(data_dir, files[idx])


def main():
    print("文本分析系统")
    print("请选择展示方式：")
    print("1. 命令行界面（CLI）")
    print("2. 图形界面（GUI）")

    choice = input("请输入选项（1/2）：").strip()

    # ========== CLI ==========
    if choice == "1":
        import app_cli
        app_cli.main()


    # ========== GUI ==========
    elif choice == "2":
        from gui.app import main as gui_main
        gui_main()   # ⚠️ GUI 自己负责文件选择

    else:
        print("输入无效，程序退出")


if __name__ == "__main__":
    main()
