import unittest
import numpy as np
import cv2
from flash_detector.core.detector import FlashDetectorBuffer

class TestFlashDetector(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        self.detector = FlashDetectorBuffer(
            buffer_size=5,
            region_size=20,
            diff_threshold=30
        )

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.detector.buffer_size, 5)
        self.assertEqual(self.detector.region_size, 20)
        self.assertEqual(self.detector.diff_threshold, 30)
        self.assertEqual(len(self.detector.frame_buffer), 0)
        self.assertEqual(len(self.detector.brightness_cache), 0)

    def test_calculate_region_brightness(self):
        """测试区域亮度计算"""
        # 创建测试图像
        test_frame = np.ones((100, 100), dtype=np.uint8) * 128
        brightness = self.detector._calculate_region_brightness(test_frame, 0, 0)
        self.assertEqual(brightness, 128)

    def test_clear_cache(self):
        """测试缓存清理"""
        # 添加一些测试数据
        test_frame = np.ones((100, 100), dtype=np.uint8)
        self.detector.process_frame(test_frame, 0)
        self.detector.clear_cache()
        self.assertEqual(len(self.detector.frame_buffer), 0)
        self.assertEqual(len(self.detector.brightness_cache), 0)

if __name__ == '__main__':
    unittest.main()
