from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from typing import Optional, List, Tuple, Union


class BasePage:
    def __init__(self, driver: webdriver.Chrome, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def wait_for_title_contains(self, title: str) -> None:
        """等待页面标题包含指定文本"""
        self.wait.until(EC.title_contains(title))
    
    def verify_page_title(self, expected_title: str) -> None:
        """验证页面标题以预期文本开始"""
        actual_title = self.driver.title
        if not actual_title or not actual_title.startswith(expected_title):
            raise IllegalStateError(f"错误页面: {actual_title}")
    
    # ================== 元素定位封装 ==================
    # 使用元组作为参数
    def find_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """查找单个元素，带等待机制"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise ElementNotFoundError(f"元素未找到: {locator}")
    
    def find_elements(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[WebElement]:
        """查找多个元素，带等待机制"""
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def find_clickable_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """查找可点击的元素"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise ElementNotFoundError(f"可点击元素未找到: {locator}")
    
    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """等待元素可见"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise ElementNotFoundError(f"元素不可见: {locator}")
    
    def wait_for_element_disappear(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """等待元素消失"""
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """检查元素是否存在"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Tuple[By, str]) -> bool:
        """检查元素是否可见"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    # ================== 元素操作封装 ==================
    
    def click_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """点击元素"""
        element = self.find_clickable_element(locator, timeout)
        element.click()
    
    def input_text(self, locator: Tuple[By, str], text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """输入文本到元素"""
        element = self.find_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def get_attribute(self, locator: Tuple[By, str], attribute_name: str, timeout: Optional[int] = None) -> str:
        """获取元素属性"""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute_name)
    
    def get_property(self, locator: Tuple[By, str], property_name: str, timeout: Optional[int] = None) -> str:
        """获取元素属性值"""
        element = self.find_element(locator, timeout)
        return element.get_property(property_name)
    
    def get_css_value(self, locator: Tuple[By, str], css_property: str, timeout: Optional[int] = None) -> str:
        """获取元素CSS值"""
        element = self.find_element(locator, timeout)
        return element.value_of_css_property(css_property)
    
    def select_dropdown_by_value(self, locator: Tuple[By, str], value: str, timeout: Optional[int] = None) -> None:
        """通过值选择下拉框选项"""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
    
    def select_dropdown_by_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """通过文本选择下拉框选项"""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def set_checkbox(self, locator: Tuple[By, str], checked: bool, timeout: Optional[int] = None) -> None:
        """设置复选框状态"""
        element = self.find_element(locator, timeout)
        if element.is_selected() != checked:
            element.click()
    
    def is_checkbox_checked(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """检查复选框是否选中"""
        element = self.find_element(locator, timeout)
        return element.is_selected()
    
    def execute_script_on_element(self, script: str, locator: Tuple[By, str], *args, timeout: Optional[int] = None):
        """在元素上执行JavaScript"""
        element = self.find_element(locator, timeout)
        return self.driver.execute_script(script, element, *args)

# ================== 自定义异常 ==================

class ElementNotFoundError(Exception):
    """元素未找到异常"""
    pass

class IllegalStateError(Exception):
    """非法状态异常"""
    pass
