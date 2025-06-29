from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from datetime import date
from enum import Enum
from typing import Optional

# ================== 注册页面定位符 ==================
EMAIL_INPUT = (By.ID, "email")
PASSWORD_INPUT = (By.ID, "password")
PASSWORD_CONFIRMATION_INPUT = (By.ID, "password-confirmation")
USERNAME_INPUT = (By.ID, "username")
RANK_PREMIUM_RADIO = (By.ID, "rank-premium")
RANK_NORMAL_RADIO = (By.ID, "rank-normal")
ADDRESS_INPUT = (By.ID, "address")
TEL_INPUT = (By.ID, "tel")
GENDER_SELECT = (By.ID, "gender")
BIRTHDAY_INPUT = (By.ID, "birthday")
NOTIFICATION_CHECKBOX = (By.ID, "notification")
SIGNUP_BUTTON = (By.CSS_SELECTOR, "#signup-form > button")

# 错误消息定位符
EMAIL_MESSAGE = (By.CSS_SELECTOR, "#email ~ .invalid-feedback")
PASSWORD_MESSAGE = (By.CSS_SELECTOR, "#password ~ .invalid-feedback")
PASSWORD_CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, "#password-confirmation ~ .invalid-feedback")
USERNAME_MESSAGE = (By.CSS_SELECTOR, "#username ~ .invalid-feedback")
ADDRESS_MESSAGE = (By.CSS_SELECTOR, "#address ~ .invalid-feedback")
TEL_MESSAGE = (By.CSS_SELECTOR, "#tel ~ .invalid-feedback")
GENDER_MESSAGE = (By.CSS_SELECTOR, "#gender ~ .invalid-feedback")
BIRTHDAY_MESSAGE = (By.CSS_SELECTOR, "#birthday ~ .invalid-feedback")


class Rank(Enum):
    PREMIUM = "premium"
    NORMAL = "normal"


class Gender(Enum):
    NOT_ANSWER = "0"
    MALE = "1"
    FEMALE = "2"
    OTHER = "9"


class SignupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Sign up")
        self.verify_page_title("Sign up")
    
    def set_email(self, email: str) -> None:
        """设置邮箱"""
        self.input_text(EMAIL_INPUT, email)
    
    def set_password(self, password: str) -> None:
        """设置密码"""
        self.input_text(PASSWORD_INPUT, password)
    
    def set_password_confirmation(self, password: str) -> None:
        """设置确认密码"""
        self.input_text(PASSWORD_CONFIRMATION_INPUT, password)
    
    def set_username(self, username: str) -> None:
        """设置用户名"""
        self.input_text(USERNAME_INPUT, username)
    
    def set_rank(self, rank: Rank) -> None:
        """设置会员等级"""
        if rank == Rank.PREMIUM:
            self.click_element(RANK_PREMIUM_RADIO)
        elif rank == Rank.NORMAL:
            self.click_element(RANK_NORMAL_RADIO)
        else:
            raise ValueError(f"Invalid rank: {rank}")
    
    def set_address(self, address: str) -> None:
        """设置地址"""
        self.input_text(ADDRESS_INPUT, address)
    
    def set_tel(self, tel: str) -> None:
        """设置电话"""
        self.input_text(TEL_INPUT, tel)
    
    def set_gender(self, gender: Gender) -> None:
        """设置性别"""
        self.select_dropdown_by_value(GENDER_SELECT, gender.value)
    
    def set_birthday(self, birthday: Optional[date]) -> None:
        """设置生日"""
        birthday_str = birthday.strftime("%Y-%m-%d") if birthday else ""
        self.execute_script_on_element(
            "arguments[0].value = arguments[1]", 
            BIRTHDAY_INPUT, 
            birthday_str
        )
    
    def set_notification(self, checked: bool) -> None:
        """设置通知选项"""
        self.set_checkbox(NOTIFICATION_CHECKBOX, checked)
    
    def go_to_my_page(self):
        """提交注册表单并跳转到个人页面"""
        self.click_element(SIGNUP_BUTTON)
        
        # 在此处导入以避免循环导入
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def go_to_my_page_expecting_failure(self) -> None:
        """提交注册表单期望失败"""
        self.click_element(SIGNUP_BUTTON)
    
    def get_email_message(self) -> str:
        """获取邮箱验证消息"""
        return self.get_text(EMAIL_MESSAGE)
    
    def get_password_message(self) -> str:
        """获取密码验证消息"""
        return self.get_text(PASSWORD_MESSAGE)
    
    def get_password_confirmation_message(self) -> str:
        """获取确认密码验证消息"""
        return self.get_text(PASSWORD_CONFIRMATION_MESSAGE)
    
    def get_username_message(self) -> str:
        """获取用户名验证消息"""
        return self.get_text(USERNAME_MESSAGE)
    
    def get_address_message(self) -> str:
        """获取地址验证消息"""
        return self.get_text(ADDRESS_MESSAGE)
    
    def get_tel_message(self) -> str:
        """获取电话验证消息"""
        return self.get_text(TEL_MESSAGE)
    
    def get_gender_message(self) -> str:
        """获取性别验证消息"""
        return self.get_text(GENDER_MESSAGE)
    
    def get_birthday_message(self) -> str:
        """获取生日验证消息"""
        return self.get_text(BIRTHDAY_MESSAGE) 