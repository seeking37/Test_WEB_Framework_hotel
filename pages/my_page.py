from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from pages.base_page import BasePage
from typing import List


class MyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("MyPage")
        self.verify_page_title("MyPage")
    
    def go_to_plans_page(self):
        """导航到方案页面"""
        plan_link = self.driver.find_element(By.LINK_TEXT, "Reserve")
        plan_link.click()
        
        # 在此处导入以避免循环导入
        from pages.plans_page import PlansPage
        return PlansPage(self.driver)
    
    def go_to_icon_page(self):
        """导航到图标页面"""
        icon_link = self.driver.find_element(By.ID, "icon-link")
        icon_link.click()
        
        # 在此处导入以避免循环导入
        from pages.icon_page import IconPage
        return IconPage(self.driver)
    
    def get_header_text(self) -> str:
        """获取标题文本"""
        header = self.driver.find_element(By.TAG_NAME, "h2")
        return header.text
    
    def get_email(self) -> str:
        """获取邮箱文本"""
        email = self.driver.find_element(By.ID, "email")
        return email.text
    
    def get_username(self) -> str:
        """获取用户名文本"""
        username = self.driver.find_element(By.ID, "username")
        return username.text
    
    def get_rank(self) -> str:
        """获取会员等级文本"""
        rank = self.driver.find_element(By.ID, "rank")
        return rank.text
    
    def get_address(self) -> str:
        """获取地址文本"""
        address = self.driver.find_element(By.ID, "address")
        return address.text
    
    def get_tel(self) -> str:
        """获取电话文本"""
        tel = self.driver.find_element(By.ID, "tel")
        return tel.text
    
    def get_gender(self) -> str:
        """获取性别文本"""
        gender = self.driver.find_element(By.ID, "gender")
        return gender.text
    
    def get_birthday(self) -> str:
        """获取生日文本"""
        birthday = self.driver.find_element(By.ID, "birthday")
        return birthday.text
    
    def get_notification(self) -> str:
        """获取通知文本"""
        notification = self.driver.find_element(By.ID, "notification")
        return notification.text
    
    def exists_icon_image(self) -> bool:
        """检查图标图片是否存在"""
        images = self.driver.find_elements(By.CSS_SELECTOR, "#icon-holder > img")
        return len(images) > 0
    
    def get_icon_image_width(self) -> int:
        """获取图标图片宽度"""
        image = self.driver.find_element(By.CSS_SELECTOR, "#icon-holder > img")
        width = image.get_property("width")
        return int(width) if width else -1
    
    def get_icon_image_border(self) -> Color:
        """获取图标图片边框颜色"""
        image = self.driver.find_element(By.CSS_SELECTOR, "#icon-holder > img")
        background_color = image.value_of_css_property("backgroundColor")
        if not background_color:
            background_color = image.value_of_css_property("background-color")
        return Color.from_string(background_color)
    
    def delete_user(self) -> None:
        """删除用户账户"""
        delete_button = self.driver.find_element(By.CSS_SELECTOR, "#delete-form > button")
        delete_button.click() 