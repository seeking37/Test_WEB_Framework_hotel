from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ================== 首页定位符 ==================
LOGIN_LINK = (By.LINK_TEXT, "Login")
SIGNUP_LINK = (By.LINK_TEXT, "Sign up")
RESERVE_LINK = (By.LINK_TEXT, "Reserve")


class TopPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("HOTEL PLANISPHERE")
        self.verify_page_title("HOTEL PLANISPHERE")
    
    def go_to_login_page(self):
        """导航到登录页面"""
        self.click_element(LOGIN_LINK)
        
        # 在此处导入以避免循环导入
        from pages.login_page import LoginPage
        return LoginPage(self.driver)
    
    def go_to_signup_page(self):
        """导航到注册页面"""
        self.click_element(SIGNUP_LINK)
        
        # 在此处导入以避免循环导入
        from pages.signup_page import SignupPage
        return SignupPage(self.driver)
    
    def go_to_plans_page(self):
        """导航到方案页面"""
        self.click_element(RESERVE_LINK)
        
        # 在此处导入以避免循环导入
        from pages.plans_page import PlansPage
        return PlansPage(self.driver) 