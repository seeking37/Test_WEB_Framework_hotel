from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class TopPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait.until(EC.title_is("HOTEL PLANISPHERE - Website for Practice Test Automation"))
        self.verify_page_title("HOTEL PLANISPHERE - Website for Practice Test Automation")
    
    def go_to_login_page(self):
        """导航到登录页面"""
        login_link = self.driver.find_element(By.LINK_TEXT, "Login")
        login_link.click()
        
        # 在此处导入以避免循环导入
        from pages.login_page import LoginPage
        return LoginPage(self.driver)
    
    def go_to_signup_page(self):
        """导航到注册页面"""
        signup_link = self.driver.find_element(By.LINK_TEXT, "Sign up")
        signup_link.click()
        
        # 在此处导入以避免循环导入
        from pages.signup_page import SignupPage
        return SignupPage(self.driver)
    
    def go_to_plans_page(self):
        """导航到方案页面"""
        plan_link = self.driver.find_element(By.LINK_TEXT, "Reserve")
        plan_link.click()
        
        # 在此处导入以避免循环导入
        from pages.plans_page import PlansPage
        return PlansPage(self.driver) 