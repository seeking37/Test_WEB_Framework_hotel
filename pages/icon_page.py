from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from pages.base_page import BasePage
from pathlib import Path

# ================== 图标页面定位符 ==================
ICON_INPUT = (By.ID, "icon")
ZOOM_INPUT = (By.ID, "zoom")
COLOR_INPUT = (By.ID, "color")
SUBMIT_BUTTON = (By.CSS_SELECTOR, "#icon-form > button")
ICON_MESSAGE = (By.CSS_SELECTOR, "#icon ~ .invalid-feedback")


class IconPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Setting Icon")
        self.verify_page_title("Setting Icon")
    
    def set_icon(self, file_path: Path) -> None:
        """设置图标文件"""
        self.input_text(ICON_INPUT, str(file_path.absolute()), clear_first=False)
    
    def set_zoom(self, value: int) -> None:
        """设置缩放值"""
        self.execute_script_on_element(
            "arguments[0].value = arguments[1]", 
            ZOOM_INPUT, 
            str(value)
        )
    
    def set_color(self, color: Color) -> None:
        """设置颜色"""
        self.execute_script_on_element(
            "arguments[0].value = arguments[1]", 
            COLOR_INPUT, 
            color.hex
        )
    
    def go_to_my_page(self):
        """提交图标设置并返回个人页面"""
        self.click_element(SUBMIT_BUTTON)
        
        # 在此处导入以避免循环导入
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def get_icon_message(self) -> str:
        """获取图标验证消息"""
        return self.get_text(ICON_MESSAGE) 