from enum import Enum
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import allure


class Contact(Enum):
    """联系方式枚举"""
    NO = "no"
    EMAIL = "email"
    TELEPHONE = "tel"


class ReservePage(BasePage):
    """预订页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
        self.wait.until(EC.title_contains("Reservation"))
        if not self.driver.title or not self.driver.title.startswith("Reservation"):
            raise Exception(f"错误页面: {self.driver.title}")
    
    @allure.step("设置预订日期")
    def set_reserve_date(self, date: str):
        """设置预订日期"""
        date_input = self.driver.find_element(By.ID, "date")
        date_input.clear()
        date_input.send_keys(date)
        date_picker_close = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-close")
        date_picker_close.click()
    
    @allure.step("设置预订天数")
    def set_reserve_term(self, term: str):
        """设置预订天数"""
        term_input = self.driver.find_element(By.ID, "term")
        term_input.clear()
        term_input.send_keys(term)
    
    @allure.step("设置人数")
    def set_head_count(self, head_count: str):
        """设置人数"""
        head_count_input = self.driver.find_element(By.ID, "head-count")
        head_count_input.clear()
        head_count_input.send_keys(head_count)
    
    @allure.step("设置早餐计划")
    def set_breakfast_plan(self, checked: bool):
        """设置早餐计划"""
        breakfast_check = self.driver.find_element(By.ID, "breakfast")
        if breakfast_check.is_selected() != checked:
            breakfast_check.click()
    
    @allure.step("设置早入住计划")
    def set_early_check_in_plan(self, checked: bool):
        """设置早入住计划"""
        early_check_in_check = self.driver.find_element(By.ID, "early-check-in")
        if early_check_in_check.is_selected() != checked:
            early_check_in_check.click()
    
    @allure.step("设置观光计划")
    def set_sightseeing_plan(self, checked: bool):
        """设置观光计划"""
        sightseeing_check = self.driver.find_element(By.ID, "sightseeing")
        if sightseeing_check.is_selected() != checked:
            sightseeing_check.click()
    
    @allure.step("设置用户名")
    def set_username(self, username: str):
        """设置用户名"""
        username_input = self.driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(username)
    
    @allure.step("设置联系方式")
    def set_contact(self, contact: Contact):
        """设置联系方式"""
        contact_select = Select(self.driver.find_element(By.ID, "contact"))
        contact_select.select_by_value(contact.value)
    
    @allure.step("设置邮箱")
    def set_email(self, email: str):
        """设置邮箱"""
        email_input = self.driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email)
    
    def is_email_displayed(self) -> bool:
        """检查邮箱字段是否显示"""
        email_input = self.driver.find_element(By.ID, "email")
        return email_input.is_displayed()
    
    @allure.step("设置电话")
    def set_tel(self, tel: str):
        """设置电话"""
        tel_input = self.driver.find_element(By.ID, "tel")
        tel_input.clear()
        tel_input.send_keys(tel)
    
    def is_tel_displayed(self) -> bool:
        """检查电话字段是否显示"""
        tel_input = self.driver.find_element(By.ID, "tel")
        return tel_input.is_displayed()
    
    @allure.step("设置备注")
    def set_comment(self, comment: str):
        """设置备注"""
        comment_textarea = self.driver.find_element(By.ID, "comment")
        comment_textarea.clear()
        comment_textarea.send_keys(comment)
    
    @allure.step("跳转到确认页面")
    def go_to_confirm_page(self):
        """跳转到确认页面"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-test='submit-button']")
        submit_button.click()
        from pages.confirm_page import ConfirmPage
        return ConfirmPage(self.driver)
    
    @allure.step("尝试跳转到确认页面（预期失败）")
    def go_to_confirm_page_expecting_failure(self):
        """尝试跳转到确认页面（预期失败）"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-test='submit-button']")
        submit_button.click()
    
    def get_plan_name(self) -> str:
        """获取计划名称"""
        import re
        self.wait.until(lambda driver: re.search(r'\S+', driver.find_element(By.ID, "plan-name").text))
        plan_name = self.driver.find_element(By.ID, "plan-name")
        return plan_name.text
    
    def get_reserve_date(self) -> str:
        """获取预订日期"""
        date_input = self.driver.find_element(By.ID, "date")
        return date_input.get_property("value")
    
    def get_reserve_term(self) -> str:
        """获取预订天数"""
        term_input = self.driver.find_element(By.ID, "term")
        return term_input.get_property("value")
    
    def get_head_count(self) -> str:
        """获取人数"""
        head_count_input = self.driver.find_element(By.ID, "head-count")
        return head_count_input.get_property("value")
    
    def get_username(self) -> str:
        """获取用户名"""
        username_input = self.driver.find_element(By.ID, "username")
        return username_input.get_property("value")
    
    def get_email(self) -> str:
        """获取邮箱"""
        email_input = self.driver.find_element(By.ID, "email")
        return email_input.get_property("value")
    
    def get_tel(self) -> str:
        """获取电话"""
        tel_input = self.driver.find_element(By.ID, "tel")
        return tel_input.get_property("value")
    
    def get_reserve_date_message(self) -> str:
        """获取预订日期错误信息"""
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#date ~ .invalid-feedback")))
            reserve_date_message = self.driver.find_element(By.CSS_SELECTOR, "#date ~ .invalid-feedback")
            return reserve_date_message.text
        except:
            # 如果找不到错误消息元素，尝试其他可能的选择器
            try:
                reserve_date_message = self.driver.find_element(By.CSS_SELECTOR, "#date + .invalid-feedback")
                return reserve_date_message.text
            except:
                return ""
    
    def get_reserve_term_message(self) -> str:
        """获取预订天数错误信息"""
        try:
            reserve_term_message = self.driver.find_element(By.CSS_SELECTOR, "#term ~ .invalid-feedback")
            return reserve_term_message.text
        except:
            try:
                reserve_term_message = self.driver.find_element(By.CSS_SELECTOR, "#term + .invalid-feedback")
                return reserve_term_message.text
            except:
                return ""
    
    def get_head_count_message(self) -> str:
        """获取人数错误信息"""
        try:
            head_count_message = self.driver.find_element(By.CSS_SELECTOR, "#head-count ~ .invalid-feedback")
            return head_count_message.text
        except:
            try:
                head_count_message = self.driver.find_element(By.CSS_SELECTOR, "#head-count + .invalid-feedback")
                return head_count_message.text
            except:
                return ""
    
    def get_username_message(self) -> str:
        """获取用户名错误信息"""
        try:
            username_message = self.driver.find_element(By.CSS_SELECTOR, "#username ~ .invalid-feedback")
            return username_message.text
        except:
            try:
                username_message = self.driver.find_element(By.CSS_SELECTOR, "#username + .invalid-feedback")
                return username_message.text
            except:
                return ""
    
    def get_email_message(self) -> str:
        """获取邮箱错误信息"""
        try:
            email_message = self.driver.find_element(By.CSS_SELECTOR, "#email ~ .invalid-feedback")
            return email_message.text
        except:
            try:
                email_message = self.driver.find_element(By.CSS_SELECTOR, "#email + .invalid-feedback")
                return email_message.text
            except:
                return ""
    
    def get_tel_message(self) -> str:
        """获取电话错误信息"""
        try:
            tel_message = self.driver.find_element(By.CSS_SELECTOR, "#tel ~ .invalid-feedback")
            return tel_message.text
        except:
            try:
                tel_message = self.driver.find_element(By.CSS_SELECTOR, "#tel + .invalid-feedback")
                return tel_message.text
            except:
                return ""