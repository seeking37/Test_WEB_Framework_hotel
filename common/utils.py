import os
import time
from typing import List, Set


class Utils:
    BASE_URL = os.getenv('BASE_URL', 'https://hotel-example-site.takeyaqa.dev/en-US')
    
    @staticmethod
    def get_new_window_handle(handles_before_open: Set[str], handles_after_open: Set[str]) -> str:
        """获取新窗口句柄"""
        handles = handles_after_open - handles_before_open
        if not handles:
            raise RuntimeError("找不到新窗口")
        elif len(handles) > 1:
            raise RuntimeError("存在多个窗口")
        else:
            return list(handles)[0]
    
    @staticmethod
    def sleep(seconds: float) -> None:
        """休眠指定秒数"""
        time.sleep(seconds) 