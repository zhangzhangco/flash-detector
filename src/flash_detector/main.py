import sys
from .interface.cli import run_cli
from .interface.gui import create_gradio_interface

def main():
    """主程序入口"""
    if len(sys.argv) > 1:
        # 命令行模式
        run_cli()
    else:
        # GUI模式
        demo = create_gradio_interface()
        demo.launch()

if __name__ == "__main__":
    main()
