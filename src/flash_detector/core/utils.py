import cv2
import numpy as np
from typing import Tuple

def time_str_to_seconds(time_str: str) -> float:
    """将时间字符串(分:秒)转换为秒数"""
    try:
        if ':' in time_str:
            minutes, seconds = map(float, time_str.split(':'))
            return minutes * 60 + seconds
        return float(time_str)
    except:
        return 0.0

def format_time(seconds: float) -> str:
    """将秒数格式化为时间字符串"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:05.2f}"

def check_circularity(region: np.ndarray, threshold: float) -> bool:
    """检查区域的圆形度"""
    try:
        # 转换为灰度图
        if len(region.shape) == 3:
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        else:
            gray = region

        # 二值化
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 找到轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return False

        # 获取最大轮廓
        contour = max(contours, key=cv2.contourArea)

        # 计算圆形度
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return False

        circularity = 4 * np.pi * area / (perimeter * perimeter)
        return circularity >= threshold

    except Exception as e:
        print(f"圆形度检查失败: {str(e)}")
        return False
