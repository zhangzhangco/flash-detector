import gradio as gr
import time
import psutil
import os
import cv2
from ..core.detector import detect_flash
from ..core.utils import time_str_to_seconds, format_time
from ..visualization.visualizer import create_diff_map, create_region_detail

def process_video_gradio(
    video_input,
    abs_threshold,
    rel_threshold,
    circularity_threshold,
    region_size,
    frame_step,
    start_time,
    progress=gr.Progress()
):
    """处理Gradio界面的视频输入"""
    try:
        # 性能统计开始
        start_time_proc = time.time()
        process = psutil.Process(os.getpid())
        memory_start = process.memory_info()

        # 获取视频信息
        cap = cv2.VideoCapture(video_input)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        # 检测闪光
        results = detect_flash(
            video_input,
            abs_threshold,
            rel_threshold,
            region_size,
            frame_step,
            start_time,
            circularity_threshold
        )

        # 计算性能统计
        process_time = time.time() - start_time_proc
        memory_end = process.memory_info()
        memory_used = (memory_end.rss - memory_start.rss) / 1024 / 1024  # MB

        # 准备性能报告
        performance_report = f"""
### 性能统计
- 处理时间: {process_time:.2f}秒
- 内存使用: {memory_used:.1f} MB
- CPU使用率: {process.cpu_percent()}%
- 处理速度: {total_frames/process_time:.1f} 帧/秒
"""

        if results and len(results) >= 2:
            flash_info = results[0]
            debug_images = results[1]

            frame_num, intensity, (x, y) = flash_info

            # 基本信息
            basic_info = f"检测到闪光！\n帧号: {frame_num}\n位置: ({x}, {y})"

            # 详细信息
            detailed_info = f"""
### 检测详情
- **时间点**: {frame_num/fps:.3f}秒
- **位置坐标**: ({x}, {y})
- **闪光强度**: {intensity:.2f}
- **相对变化**: {intensity/255:.2f}

{performance_report}
"""

            # 获取图像
            frame_rgb = debug_images.get('curr_frame')
            diff_map = debug_images.get('diff_map')
            region_detail = create_region_detail(frame_rgb, x, y, region_size)

            return (basic_info, detailed_info, frame_rgb, diff_map, region_detail)

        return (
            "未检测到闪光",
            f"### 处理完成\n未发现符合条件的闪光\n\n{performance_report}",
            None, None, None
        )

    except Exception as e:
        import traceback
        error_msg = f"处理失败: {str(e)}\n{traceback.format_exc()}"
        return (error_msg, error_msg, None, None, None)

def create_gradio_interface():
    """创建Gradio界面"""
    with gr.Blocks() as demo:
        gr.Markdown("# 视频闪光检测工具")

        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="上传视频")
                with gr.Accordion("检测参数", open=True):
                    abs_threshold = gr.Slider(
                        minimum=5, maximum=100, value=20, step=5,
                        label="绝对差异阈值",
                        info="灰度值差异阈值(5-100)"
                    )
                    rel_threshold = gr.Slider(
                        minimum=0.1, maximum=2.0, value=0.3, step=0.1,
                        label="相对变化阈值",
                        info="亮度变化比例(0.1-2.0)"
                    )
                    circularity_threshold = gr.Slider(
                        minimum=0.1, maximum=1.0, value=0.5, step=0.1,
                        label="圆形度阈值",
                        info="形状圆度要求(0.1-1.0)"
                    )
                    region_size = gr.Slider(
                        minimum=10, maximum=100, value=20, step=5,
                        label="检测区域大小",
                        info="检测窗口的大小(像素)"
                    )
                    frame_step = gr.Slider(
                        minimum=1, maximum=10, value=1, step=1,
                        label="帧比较步长",
                        info="每隔多少帧进行比较"
                    )
                    start_time = gr.Textbox(
                        value="0:00",
                        label="开始时间",
                        info="从视频的什么时间开始分析"
                    )

            with gr.Column():
                with gr.Accordion("检测结果", open=True):
                    result_text = gr.Textbox(
                        label="基本信息",
                        lines=3
                    )
                    with gr.Accordion("详细信息", open=False):
                        detection_details = gr.Markdown()

                with gr.Accordion("可视化结果", open=True):
                    with gr.Row():
                        result_image = gr.Image(label="检测到的闪光帧")
                        diff_map = gr.Image(label="差异热力图")
                    region_detail = gr.Image(label="检测区域放大图")

        submit_btn = gr.Button("开始检测")
        submit_btn.click(
            fn=process_video_gradio,
            inputs=[
                video_input,
                abs_threshold,
                rel_threshold,
                circularity_threshold,
                region_size,
                frame_step,
                start_time
            ],
            outputs=[
                result_text,
                detection_details,
                result_image,
                diff_map,
                region_detail
            ]
        )

    return demo
