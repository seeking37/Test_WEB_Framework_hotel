from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ================== 登录页面定位符 ==================
EMAIL_INPUT = (By.ID, "email")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
EMAIL_MESSAGE = (By.ID, "email-message")
PASSWORD_MESSAGE = (By.ID, "password-message")


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Login")
        self.verify_page_title("Login")
    
    def do_login(self, email: str, password: str):
        """使用邮箱和密码执行登录"""
        # 输入邮箱
        self.input_text(EMAIL_INPUT, email)
        
        # 输入密码
        self.input_text(PASSWORD_INPUT, password)
        
        # 点击登录按钮
        self.click_element(LOGIN_BUTTON)
        
        # 在此处导入以避免循环导入
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def do_login_expecting_failure(self, email: str, password: str) -> None:
        """执行预期失败的登录"""
        # 输入邮箱
        self.input_text(EMAIL_INPUT, email)
        
        # 输入密码
        self.input_text(PASSWORD_INPUT, password)
        
        # 点击登录按钮
        self.click_element(LOGIN_BUTTON)
    
    def get_email_message(self) -> str:
        """获取邮箱验证消息"""
        return self.get_text(EMAIL_MESSAGE)
    
    def get_password_message(self) -> str:
        """获取密码验证消息"""
        return self.get_text(PASSWORD_MESSAGE) 