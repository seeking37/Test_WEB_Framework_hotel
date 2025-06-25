from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import Optional


class BasePage:
    def __init__(self, driver: webdriver.Chrome, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_title_contains(self, title: str) -> None:
        """等待页面标题包含指定文本"""
        self.wait.until(EC.title_contains(title))
    
    def verify_page_title(self, expected_title: str) -> None:
        """验证页面标题以预期文本开始"""
        actual_title = self.driver.title
        if not actual_title or not actual_title.startswith(expected_title):
            raise IllegalStateError(f"错误页面: {actual_title}")


class IllegalStateError(Exception):
    """非法状态的自定义异常"""
    pass 