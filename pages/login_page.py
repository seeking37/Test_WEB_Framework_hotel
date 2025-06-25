from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Login")
        self.verify_page_title("Login")
    
    def do_login(self, email: str, password: str):
        """使用邮箱和密码执行登录"""
        email_input = self.driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)
        
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # 在此处导入以避免循环导入
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def do_login_expecting_failure(self, email: str, password: str) -> None:
        """执行预期失败的登录"""
        email_input = self.driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)
        
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
    
    def get_email_message(self) -> str:
        """获取邮箱验证消息"""
        email_message = self.driver.find_element(By.ID, "email-message")
        return email_message.text
    
    def get_password_message(self) -> str:
        """获取密码验证消息"""
        password_message = self.driver.find_element(By.ID, "password-message")
        return password_message.text 