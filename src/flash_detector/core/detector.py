import cv2
import numpy as np
from collections import deque
from typing import Dict, Optional

class FlashDetectorBuffer:
    def __init__(self, buffer_size=5, region_size=20, diff_threshold=30):
        """初始化检测器"""
        self.buffer_size = buffer_size
        self.region_size = region_size
        self.diff_threshold = diff_threshold
        
        self.frame_buffer = deque(maxlen=buffer_size)
        self.brightness_cache = {}
        
    # ... [之前的FlashDetectorBuffer类的其余代码]
