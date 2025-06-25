from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RoomPage(BasePage):
    """房间页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_header(self) -> str:
        """获取页面标题"""
        header = self.driver.find_element(By.TAG_NAME, "h5")
        return header.text