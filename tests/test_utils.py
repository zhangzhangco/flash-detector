import unittest
from flash_detector.core.utils import time_str_to_seconds, format_time

class TestUtils(unittest.TestCase):
    def test_time_str_to_seconds(self):
        self.assertEqual(time_str_to_seconds("1:30"), 90)
        self.assertEqual(time_str_to_seconds("0:45"), 45)
        self.assertEqual(time_str_to_seconds("invalid"), 0)

    def test_format_time(self):
        self.assertEqual(format_time(90), "01:30.00")
        self.assertEqual(format_time(45), "00:45.00")

    # ... [更多测试用例]

if __name__ == '__main__':
    unittest.main()
