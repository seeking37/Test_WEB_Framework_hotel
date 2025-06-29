import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import allure

# ================== 确认页面定位符 ==================
# 信息显示
TOTAL_BILL_TEXT = (By.ID, "total-bill")
PLAN_NAME_TEXT = (By.ID, "plan-name")
TERM_TEXT = (By.ID, "term")
HEAD_COUNT_TEXT = (By.ID, "head-count")
PLANS_TEXT = (By.ID, "plans")
USERNAME_TEXT = (By.ID, "username")
CONTACT_TEXT = (By.ID, "contact")
COMMENT_TEXT = (By.ID, "comment")

# 按钮和模态框
CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[data-target='#success-modal']")
SUCCESS_MODAL = (By.ID, "success-modal")
MODAL_MESSAGE = (By.CSS_SELECTOR, "#success-modal > div > div > .modal-body")
CLOSE_BUTTON = (By.CSS_SELECTOR, "#success-modal > div > div > div > button.btn-success")


class ConfirmPage(BasePage):
    """确认页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Confirm Reservation")
        self.verify_page_title("Confirm Reservation")
    
    def get_total_bill(self) -> str:
        """获取总金额"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(TOTAL_BILL_TEXT)))
        return self.get_text(TOTAL_BILL_TEXT)
    
    def get_plan_name(self) -> str:
        """获取计划名称"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(PLAN_NAME_TEXT)))
        return self.get_text(PLAN_NAME_TEXT)
    
    def get_term(self) -> str:
        """获取预订时间段"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(TERM_TEXT)))
        return self.get_text(TERM_TEXT)
    
    def get_head_count(self) -> str:
        """获取人数"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(HEAD_COUNT_TEXT)))
        return self.get_text(HEAD_COUNT_TEXT)
    
    def get_plans(self) -> str:
        """获取选择的计划"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(PLANS_TEXT)))
        return self.get_text(PLANS_TEXT)
    
    def get_username(self) -> str:
        """获取用户名"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(USERNAME_TEXT)))
        return self.get_text(USERNAME_TEXT)
    
    def get_contact(self) -> str:
        """获取联系方式"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(CONTACT_TEXT)))
        return self.get_text(CONTACT_TEXT)
    
    def get_comment(self) -> str:
        """获取备注"""
        self.wait.until(lambda driver: re.search(r'.+', self.get_text(COMMENT_TEXT)))
        return self.get_text(COMMENT_TEXT)
    
    @allure.step("确认预订")
    def do_confirm(self):
        """确认预订"""
        self.click_element(CONFIRM_BUTTON)
        self.wait_for_element_visible(SUCCESS_MODAL)
    
    def get_modal_message(self) -> str:
        """获取模态框消息"""
        return self.get_text(MODAL_MESSAGE)
    
    @allure.step("关闭模态框")
    def close(self):
        """关闭模态框"""
        self.click_element(CLOSE_BUTTON)