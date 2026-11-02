import sys
import os
import subprocess

def get_maxcso_path():
    """
    获取 maxcso.exe 的路径。
    核心逻辑：判断当前是直接运行 Python 脚本，还是运行打包后的 EXE。
    """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe，外部文件会被解压到临时目录 (sys._MEIPASS)
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行 python 脚本，文件就在脚本所在的目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, "maxcso.exe")

def main():
    print("="*40)
    print(" PSP ISO/CSO 快速处理工具 (by heartnn)")
    print("="*40)

    # 1. 获取输入文件路径（支持拖拽或手动输入）
    if len(sys.argv) > 1:
        # 拖拽文件到脚本上时，路径会作为参数传入。strip('"') 用于去除 Windows 自动加的双引号
        input_file = sys.argv[1].strip('"')
    else:
        # 双击运行脚本时，提示手动输入
        input_file = input("请拖入文件到本窗口，或手动输入文件路径后回车：\n> ").strip('"')

    # 检查输入的文件是否存在
    if not os.path.isfile(input_file):
        print(f"\n[错误] 找不到文件: {input_file}")
        input("\n按回车键退出...")
        return

    # 2. 定位 maxcso.exe
    maxcso_path = get_maxcso_path()
    if not os.path.isfile(maxcso_path):
        print(f"\n[错误] 找不到 maxcso.exe！")
        print("请确保 maxcso.exe 和当前脚本（或 EXE）在同一个目录下。")
        input("\n按回车键退出...")
        return

    # 3. 判断文件后缀，构建对应的命令
    file_name, file_ext = os.path.splitext(input_file)
    file_ext = file_ext.lower()

    if file_ext == ".iso":
        output_file = file_name + ".cso"
        print(f"\n[任务] 开始压缩: {os.path.basename(input_file)}")
        # 使用你要求的 --fast 和 --block=2048
        cmd = [maxcso_path, "--fast", "--block=2048", input_file, "-o", output_file]
        
    elif file_ext == ".cso":
        output_file = file_name + ".iso"
        print(f"\n[任务] 开始解压: {os.path.basename(input_file)}")
        cmd = [maxcso_path, "--decompress", input_file, "-o", output_file]
        
    else:
        print(f"\n[错误] 不支持的格式: {file_ext}，请拖入 .iso 或 .cso 文件！")
        input("\n按回车键退出...")
        return

    # 4. 执行命令并实时显示进度
    try:
        print("-" * 40)
        # subprocess.run 会实时打印 maxcso 的进度条
        subprocess.run(cmd, check=True)
        print("-" * 40)
        print(f"\n[成功] 处理完成！输出文件: {os.path.basename(output_file)}")
    except subprocess.CalledProcessError as e:
        print(f"\n[错误] maxcso 运行失败，错误代码: {e.returncode}")
    except Exception as e:
        print(f"\n[错误] 发生未知错误: {e}")

    # 5. 防止窗口一闪而过
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()