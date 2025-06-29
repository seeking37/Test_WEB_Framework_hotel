from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from pages.base_page import BasePage

# ================== 个人页面定位符 ==================
HEADER = (By.TAG_NAME, "h2")
EMAIL_TEXT = (By.ID, "email")
USERNAME_TEXT = (By.ID, "username")
RANK_TEXT = (By.ID, "rank")
ADDRESS_TEXT = (By.ID, "address")
TEL_TEXT = (By.ID, "tel")
GENDER_TEXT = (By.ID, "gender")
BIRTHDAY_TEXT = (By.ID, "birthday")
NOTIFICATION_TEXT = (By.ID, "notification")

# 导航链接
RESERVE_LINK = (By.LINK_TEXT, "Reserve")
ICON_LINK = (By.ID, "icon-link")

# 图标相关
ICON_IMAGE = (By.CSS_SELECTOR, "#icon-holder > img")

# 删除按钮
DELETE_BUTTON = (By.CSS_SELECTOR, "#delete-form > button")


class MyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("MyPage")
        self.verify_page_title("MyPage")
    
    def go_to_plans_page(self):
        """导航到方案页面"""
        self.click_element(RESERVE_LINK)
        
        # 在此处导入以避免循环导入
        from pages.plans_page import PlansPage
        return PlansPage(self.driver)
    
    def go_to_icon_page(self):
        """导航到图标页面"""
        self.click_element(ICON_LINK)
        
        # 在此处导入以避免循环导入
        from pages.icon_page import IconPage
        return IconPage(self.driver)
    
    def get_header_text(self) -> str:
        """获取页面标题文本"""
        return self.get_text(HEADER)
    
    def get_email(self) -> str:
        """获取邮箱信息"""
        return self.get_text(EMAIL_TEXT)
    
    def get_username(self) -> str:
        """获取用户名信息"""
        return self.get_text(USERNAME_TEXT)
    
    def get_rank(self) -> str:
        """获取会员等级信息"""
        return self.get_text(RANK_TEXT)
    
    def get_address(self) -> str:
        """获取地址信息"""
        return self.get_text(ADDRESS_TEXT)
    
    def get_tel(self) -> str:
        """获取电话信息"""
        return self.get_text(TEL_TEXT)
    
    def get_gender(self) -> str:
        """获取性别信息"""
        return self.get_text(GENDER_TEXT)
    
    def get_birthday(self) -> str:
        """获取生日信息"""
        return self.get_text(BIRTHDAY_TEXT)
    
    def get_notification(self) -> str:
        """获取通知设置信息"""
        return self.get_text(NOTIFICATION_TEXT)
    
    def exists_icon_image(self) -> bool:
        """检查图标图片是否存在"""
        elements = self.find_elements(ICON_IMAGE)
        return len(elements) > 0
    
    def get_icon_image_width(self) -> int:
        """获取图标图片宽度"""
        width = self.get_property(ICON_IMAGE, "width")
        return int(width) if width else -1
    
    def get_icon_image_border(self) -> Color:
        """获取图标图片边框颜色"""
        background_color = self.get_css_value(ICON_IMAGE, "backgroundColor")
        if not background_color:
            background_color = self.get_css_value(ICON_IMAGE, "background-color")
        return Color.from_string(background_color)
    
    def delete_user(self) -> None:
        """删除用户账户"""
        self.click_element(DELETE_BUTTON) 