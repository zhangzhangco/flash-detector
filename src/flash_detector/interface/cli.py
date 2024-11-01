import argparse
import cv2
import time
from ..core.detector import detect_flash
from ..core.utils import time_str_to_seconds, format_time

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='视频闪光检测工具')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('--abs_threshold', type=float, default=20,
                      help='绝对差异阈值 (默认: 20)')
    parser.add_argument('--rel_threshold', type=float, default=0.3,
                      help='相对变化阈值 (默认: 0.3，表示30%%的变化)')
    parser.add_argument('--region_size', type=int, default=20,
                      help='检测区域大小')
    parser.add_argument('--frame_step', type=int, default=1,
                      help='帧比较步长')
    parser.add_argument('--start_time', type=str, default="0:00",
                      help='开始分析的时间点(分:秒格式，如 1:30)')
    parser.add_argument('--circularity_threshold', type=float, default=0.5,
                      help='圆形度阈值 (默认: 0.5)')

    return parser.parse_args()

def run_cli():
    """运行命令行界面"""
    args = parse_arguments()
    print(f"开始处理视频: {args.video_path}")

    try:
        # 获取视频信息
        cap = cv2.VideoCapture(args.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        cap.release()

        print(f"视频信息:")
        print(f"- 总帧数: {total_frames}")
        print(f"- FPS: {fps:.2f}")
        print(f"- 时长: {format_time(duration)}")
        print(f"- 开始时间: {args.start_time}")
        print("\n检测参数:")
        print(f"- 绝对差异阈值: {args.abs_threshold}")
        print(f"- 相对变化阈值: {args.rel_threshold}")
        print(f"- 圆形度阈值: {args.circularity_threshold}")
        print(f"- 检测区域大小: {args.region_size}")
        print(f"- 帧比较步长: {args.frame_step}")

        # 开始检测
        start_time = time.time()
        results = detect_flash(
            args.video_path,
            args.abs_threshold,
            args.rel_threshold,
            args.region_size,
            args.frame_step,
            args.start_time,
            args.circularity_threshold
        )
        process_time = time.time() - start_time

        # 输出结果
        if results and isinstance(results, list):
            print("\n检测到闪光:")
            if len(results) >= 1:
                flash_info = results[0]
                if isinstance(flash_info, tuple) and len(flash_info) == 3:
                    frame_num, intensity, position = flash_info
                    time_point = frame_num / fps
                    print(f"- 帧号: {frame_num}")
                    print(f"- 时间点: {format_time(time_point)}")
                    print(f"- 强度: {intensity:.2f}")
                    print(f"- 位置: ({position[0]}, {position[1]})")
                else:
                    print("闪光信息格式不正确")

            print(f"\n处理用时: {process_time:.2f}秒")
            print(f"处理速度: {total_frames/process_time:.2f} 帧/秒")
        else:
            print("\n未检测到闪光")

    except Exception as e:
        print(f"处理失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
