"""Core functionality for flash detection."""
from .detector import FlashDetectorBuffer
from .utils import time_str_to_seconds, format_time

__all__ = ['FlashDetectorBuffer', 'time_str_to_seconds', 'format_time']
