import cv2
import numpy as np
from typing import Tuple, Optional

def create_diff_map(frame: np.ndarray, position: Tuple[int, int],
                   region_size: int) -> Optional[np.ndarray]:
    """创建差异热力图"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff_map = np.zeros_like(gray, dtype=np.float32)

        x, y = position
        x1 = max(0, x - region_size)
        y1 = max(0, y - region_size)
        x2 = min(gray.shape[1], x + region_size)
        y2 = min(gray.shape[0], y + region_size)

        Y, X = np.ogrid[y1:y2, x1:x2]
        dist_from_center = ((X - x)**2 + (Y - y)**2) / (region_size**2)
        diff_map[y1:y2, x1:x2] = np.exp(-dist_from_center) * 255

        diff_map = diff_map.astype(np.uint8)
        return cv2.applyColorMap(diff_map, cv2.COLORMAP_JET)

    except Exception as e:
        print(f"创建差异热力图失败: {str(e)}")
        return None

def create_region_detail(frame: np.ndarray, x: int, y: int,
                        region_size: int) -> Optional[np.ndarray]:
    """创建检测区域的放大图"""
    try:
        region_size_detail = max(100, region_size * 2)
        x1 = max(0, x - region_size_detail//2)
        y1 = max(0, y - region_size_detail//2)
        x2 = min(frame.shape[1], x + region_size_detail//2)
        y2 = min(frame.shape[0], y + region_size_detail//2)

        region_detail = frame[y1:y2, x1:x2].copy()
        center_x = (x2-x1)//2
        center_y = (y2-y1)//2
        cv2.line(region_detail, (center_x-10, center_y),
                (center_x+10, center_y), (0,0,255), 2)
        cv2.line(region_detail, (center_x, center_y-10),
                (center_x, center_y+10), (0,0,255), 2)

        return region_detail
    except Exception as e:
        print(f"创建区域细节图失败: {str(e)}")
        return None
