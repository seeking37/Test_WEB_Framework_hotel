import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from common.utils import Utils
import allure


class ConfirmPage(BasePage):
    """确认页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
        self.wait.until(EC.title_contains("Confirm Reservation"))
        if not self.driver.title or not self.driver.title.startswith("Confirm Reservation"):
            raise Exception(f"错误页面: {self.driver.title}")
    
    def get_total_bill(self) -> str:
        """获取总金额"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "total-bill").text))
        total_bill = self.driver.find_element(By.ID, "total-bill")
        return total_bill.text
    
    def get_plan_name(self) -> str:
        """获取计划名称"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "plan-name").text))
        plan_name = self.driver.find_element(By.ID, "plan-name")
        return plan_name.text
    
    def get_term(self) -> str:
        """获取预订时间段"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "term").text))
        term = self.driver.find_element(By.ID, "term")
        return term.text
    
    def get_head_count(self) -> str:
        """获取人数"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "head-count").text))
        head_count = self.driver.find_element(By.ID, "head-count")
        return head_count.text
    
    def get_plans(self) -> str:
        """获取选择的计划"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "plans").text))
        plans = self.driver.find_element(By.ID, "plans")
        return plans.text
    
    def get_username(self) -> str:
        """获取用户名"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "username").text))
        username = self.driver.find_element(By.ID, "username")
        return username.text
    
    def get_contact(self) -> str:
        """获取联系方式"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "contact").text))
        contact = self.driver.find_element(By.ID, "contact")
        return contact.text
    
    def get_comment(self) -> str:
        """获取备注"""
        self.wait.until(lambda driver: re.search(r'.+', driver.find_element(By.ID, "comment").text))
        comment = self.driver.find_element(By.ID, "comment")
        return comment.text
    
    @allure.step("确认预订")
    def do_confirm(self):
        """确认预订"""
        confirm_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-target='#success-modal']")
        confirm_button.click()
        Utils.sleep(2)
        self.wait.until(EC.visibility_of_element_located((By.ID, "success-modal")))
    
    def get_modal_message(self) -> str:
        """获取模态框消息"""
        modal_message = self.driver.find_element(By.CSS_SELECTOR, "#success-modal > div > div > .modal-body")
        return modal_message.text
    
    @allure.step("关闭模态框")
    def close(self):
        """关闭模态框"""
        close_button = self.driver.find_element(By.CSS_SELECTOR, "#success-modal > div > div > div > button.btn-success")
        close_button.click()