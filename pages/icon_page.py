from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from pages.base_page import BasePage
from pathlib import Path


class IconPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Setting Icon")
        self.verify_page_title("Setting Icon")
    
    def set_icon(self, file_path: Path) -> None:
        """设置图标文件"""
        icon_input = self.driver.find_element(By.ID, "icon")
        icon_input.send_keys(str(file_path.absolute()))
    
    def set_zoom(self, value: int) -> None:
        """设置缩放值"""
        zoom_input = self.driver.find_element(By.ID, "zoom")
        self.driver.execute_script("arguments[0].value = arguments[1]", zoom_input, str(value))
    
    def set_color(self, color: Color) -> None:
        """设置颜色"""
        color_input = self.driver.find_element(By.ID, "color")
        self.driver.execute_script("arguments[0].value = arguments[1]", color_input, color.hex)
    
    def go_to_my_page(self):
        """提交图标设置并返回个人页面"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#icon-form > button")
        submit_button.click()
        
        # 在此处导入以避免循环导入
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def get_icon_message(self) -> str:
        """获取图标验证消息"""
        icon_message = self.driver.find_element(By.CSS_SELECTOR, "#icon ~ .invalid-feedback")
        return icon_message.text 