import cv2
import numpy as np
from collections import deque
from typing import Dict, Optional, List, Tuple

from ..core.utils import time_str_to_seconds, check_circularity
from ..visualization.visualizer import create_diff_map

class FlashDetectorBuffer:
    def __init__(self, buffer_size=5, region_size=20, diff_threshold=30):
        """
        初始化检测器
        buffer_size: 缓存帧数
        region_size: 检测区域大小
        diff_threshold: 差异阈值
        """
        self.buffer_size = buffer_size
        self.region_size = region_size
        self.diff_threshold = diff_threshold

        # 帧缓冲区
        self.frame_buffer = deque(maxlen=buffer_size)
        # 区域亮度历史缓存
        self.brightness_cache = {}

    def _calculate_region_brightness(self, frame: np.ndarray, x: int, y: int) -> float:
        """计算指定区域的平均亮度"""
        region = frame[y:y+self.region_size, x:x+self.region_size]
        return np.mean(region)

    def process_frame(self, frame: np.ndarray, frame_num: int) -> Optional[Dict]:
        """
        处理新的帧
        frame: 输入帧
        frame_num: 帧号
        返回: 如果检测到闪光，返回位置和强度信息
        """
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 将新帧添加到缓冲区
        self.frame_buffer.append(gray)

        # 缓冲区未满时继续收集帧
        if len(self.frame_buffer) < self.buffer_size:
            return None

        # 网格划分图像
        height, width = gray.shape
        grid_step = self.region_size // 2  # 网格步长

        flash_regions = []
        for y in range(0, height - self.region_size, grid_step):
            for x in range(0, width - self.region_size, grid_step):
                region_key = (x, y)

                # 计算当前区域亮度
                current_brightness = self._calculate_region_brightness(gray, x, y)

                # 获取或初始化区域历史记录
                if region_key not in self.brightness_cache:
                    self.brightness_cache[region_key] = deque(maxlen=self.buffer_size)

                brightness_history = self.brightness_cache[region_key]
                brightness_history.append(current_brightness)

                # 分析亮度变化
                if len(brightness_history) == self.buffer_size:
                    brightness_array = np.array(brightness_history)
                    max_diff = np.max(brightness_array) - np.min(brightness_array)

                    # 检查是否存在显著的周期性变化
                    if max_diff > self.diff_threshold:
                        # 计算一阶差分
                        diffs = np.diff(brightness_array)
                        # 检查正负交替（周期性变化的特征）
                        sign_changes = np.sum(diffs[:-1] * diffs[1:] < 0)

                        if sign_changes >= 2:  # 至少有两次方向改变
                            flash_regions.append({
                                'frame_num': frame_num,
                                'position': (x + self.region_size//2, y + self.region_size//2),
                                'intensity': max_diff,
                                'frequency': sign_changes
                            })

        # 返回最强的闪光
        if flash_regions:
            return max(flash_regions, key=lambda x: x['intensity'])
        return None

    def clear_cache(self):
        """清除缓存"""
        self.frame_buffer.clear()
        self.brightness_cache.clear()

def detect_flash(
    video_path: str,
    abs_threshold: float = 20,
    rel_threshold: float = 0.3,
    region_size: int = 20,
    frame_step: int = 1,
    start_time: str = "0:00",
    circularity_threshold: float = 0.5
) -> Optional[List]:
    """使用环形缓冲区方法检测闪光"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("无法打开视频文件")

        fps = cap.get(cv2.CAP_PROP_FPS)

        # 设置开始位置
        start_seconds = time_str_to_seconds(start_time)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_seconds * fps)

        detector = FlashDetectorBuffer(
            buffer_size=5,
            region_size=region_size,
            diff_threshold=abs_threshold
        )

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_step == 0:
                flash_info = detector.process_frame(frame, frame_count)

                if flash_info:
                    # 检查圆形度
                    x, y = flash_info['position']
                    region = frame[
                        max(0, y-region_size):min(frame.shape[0], y+region_size),
                        max(0, x-region_size):min(frame.shape[1], x+region_size)
                    ]

                    if check_circularity(region, circularity_threshold):
                        # 准备debug图像
                        debug_images = {
                            'curr_frame': frame.copy(),
                            'diff_map': create_diff_map(frame,
                                                      flash_info['position'],
                                                      region_size)
                        }

                        return [(frame_count,
                                flash_info['intensity'],
                                flash_info['position']),
                               debug_images]

            frame_count += 1

    except Exception as e:
        print(f"检测失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

    finally:
        cap.release()
        detector.clear_cache()

    return None
