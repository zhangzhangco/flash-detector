import gradio as gr
import time
import psutil
import os
from ..core.detector import FlashDetectorBuffer
from ..core.utils import time_str_to_seconds
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
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        # 检测闪光
        detector = FlashDetectorBuffer(
            buffer_size=5,
            region_size=region_size,
            diff_threshold=abs_threshold
        )

        results = detector.detect_video(
            video_input,
            start_time=time_str_to_seconds(start_time),
            frame_step=frame_step,
            circularity_threshold=circularity_threshold
        )

        # ... [处理结果和性能统计的代码]
        
        return (basic_info, detailed_info, frame_rgb, diff_map, region_detail)

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
                    # ... [其他参数控件]

            with gr.Column():
                # ... [结果显示部分]

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

        gr.Markdown("""
        ### 使用说明：
        1. **参数调整建议**：...
        2. **注意事项**：...
        """)

    return demo
