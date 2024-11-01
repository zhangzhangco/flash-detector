import unittest
import numpy as np
import cv2
from flash_detector.core.utils import time_str_to_seconds, format_time, check_circularity

class TestUtils(unittest.TestCase):
    def test_time_str_to_seconds(self):
        """测试时间字符串转换"""
        self.assertEqual(time_str_to_seconds("1:30"), 90)
        self.assertEqual(time_str_to_seconds("0:45"), 45)
        self.assertEqual(time_str_to_seconds("invalid"), 0)
        self.assertEqual(time_str_to_seconds("2:00"), 120)

    def test_format_time(self):
        """测试时间格式化"""
        self.assertEqual(format_time(90), "01:30.00")
        self.assertEqual(format_time(45), "00:45.00")
        self.assertEqual(format_time(120), "02:00.00")

    def test_check_circularity(self):
        """测试圆形度检查"""
        # 创建一个圆形图像
        img = np.zeros((100, 100), dtype=np.uint8)
        cv2.circle(img, (50, 50), 30, 255, -1)
        self.assertTrue(check_circularity(img, 0.5))

        # 创建一个方形图像
        img = np.zeros((100, 100), dtype=np.uint8)
        cv2.rectangle(img, (25, 25), (75, 75), 255, -1)
        self.assertFalse(check_circularity(img, 0.8))

if __name__ == '__main__':
    unittest.main()
