import unittest
import numpy as np
from flash_detector.core.detector import FlashDetectorBuffer

class TestFlashDetector(unittest.TestCase):
    def setUp(self):
        self.detector = FlashDetectorBuffer(
            buffer_size=5,
            region_size=20,
            diff_threshold=30
        )

    def test_initialization(self):
        self.assertEqual(self.detector.buffer_size, 5)
        self.assertEqual(self.detector.region_size, 20)
        self.assertEqual(self.detector.diff_threshold, 30)

    # ... [更多测试用例]

if __name__ == '__main__':
    unittest.main()
