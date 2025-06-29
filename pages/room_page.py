from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ================== 房间页面定位符 ==================
HEADER = (By.TAG_NAME, "h5")
ROOM_INFO = (By.CSS_SELECTOR, ".room-info")
ROOM_IMAGES = (By.CSS_SELECTOR, ".room-image")


class RoomPage(BasePage):
    """房间页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_header(self) -> str:
        """获取页面标题"""
        return self.get_text(HEADER)