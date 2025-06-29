from enum import Enum
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import allure
import re

# ================== 预订页面定位符 ==================
# 基本信息字段
DATE_INPUT = (By.ID, "date")
DATE_PICKER_CLOSE = (By.CLASS_NAME, "ui-datepicker-close")
TERM_INPUT = (By.ID, "term")
HEAD_COUNT_INPUT = (By.ID, "head-count")

# 附加服务复选框
BREAKFAST_CHECKBOX = (By.ID, "breakfast")
EARLY_CHECKIN_CHECKBOX = (By.ID, "early-check-in")
SIGHTSEEING_CHECKBOX = (By.ID, "sightseeing")

# 用户信息
USERNAME_INPUT = (By.ID, "username")
CONTACT_SELECT = (By.ID, "contact")
EMAIL_INPUT = (By.ID, "email")
TEL_INPUT = (By.ID, "tel")
COMMENT_TEXTAREA = (By.ID, "comment")

# 计划信息显示
PLAN_NAME_TEXT = (By.ID, "plan-name")

# 提交按钮
SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-test='submit-button']")

# 错误消息定位符
DATE_MESSAGE = (By.CSS_SELECTOR, "#date ~ .invalid-feedback")
DATE_MESSAGE_ALT = (By.CSS_SELECTOR, "#date + .invalid-feedback")
TERM_MESSAGE = (By.CSS_SELECTOR, "#term ~ .invalid-feedback")
TERM_MESSAGE_ALT = (By.CSS_SELECTOR, "#term + .invalid-feedback")
HEAD_COUNT_MESSAGE = (By.CSS_SELECTOR, "#head-count ~ .invalid-feedback")
HEAD_COUNT_MESSAGE_ALT = (By.CSS_SELECTOR, "#head-count + .invalid-feedback")
USERNAME_MESSAGE = (By.CSS_SELECTOR, "#username ~ .invalid-feedback")
USERNAME_MESSAGE_ALT = (By.CSS_SELECTOR, "#username + .invalid-feedback")
EMAIL_MESSAGE = (By.CSS_SELECTOR, "#email ~ .invalid-feedback")
EMAIL_MESSAGE_ALT = (By.CSS_SELECTOR, "#email + .invalid-feedback")
TEL_MESSAGE = (By.CSS_SELECTOR, "#tel ~ .invalid-feedback")
TEL_MESSAGE_ALT = (By.CSS_SELECTOR, "#tel + .invalid-feedback")


class Contact(Enum):
    """联系方式枚举"""
    NO = "no"
    EMAIL = "email"
    TELEPHONE = "tel"


class ReservePage(BasePage):
    """预订页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Reservation")
        self.verify_page_title("Reservation")
    
    @allure.step("设置预订日期")
    def set_reserve_date(self, date: str):
        """设置预订日期"""
        # 对于日期输入框，需要特殊处理以确保完全清空
        element = self.find_element(DATE_INPUT)
        # 先清空
        element.clear()
        # 全选并删除，确保彻底清空
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        # 输入新日期
        if date:  # 只有当日期不为空时才输入
            element.send_keys(date)
        
        try:
            # 尝试关闭日期选择器，如果失败则忽略
            self.click_element(DATE_PICKER_CLOSE)
        except Exception:
            # 如果日期选择器关闭按钮不存在或不可点击，忽略异常
            pass
    
    @allure.step("设置预订天数")
    def set_reserve_term(self, term: str):
        """设置预订天数"""
        self.input_text(TERM_INPUT, term)
    
    @allure.step("设置人数")
    def set_head_count(self, head_count: str):
        """设置人数"""
        self.input_text(HEAD_COUNT_INPUT, head_count)
    
    @allure.step("设置早餐计划")
    def set_breakfast_plan(self, checked: bool):
        """设置早餐计划"""
        self.set_checkbox(BREAKFAST_CHECKBOX, checked)
    
    @allure.step("设置早入住计划")
    def set_early_check_in_plan(self, checked: bool):
        """设置早入住计划"""
        self.set_checkbox(EARLY_CHECKIN_CHECKBOX, checked)
    
    @allure.step("设置观光计划")
    def set_sightseeing_plan(self, checked: bool):
        """设置观光计划"""
        self.set_checkbox(SIGHTSEEING_CHECKBOX, checked)
    
    @allure.step("设置用户名")
    def set_username(self, username: str):
        """设置用户名"""
        self.input_text(USERNAME_INPUT, username)
    
    @allure.step("设置联系方式")
    def set_contact(self, contact: Contact):
        """设置联系方式"""
        self.select_dropdown_by_value(CONTACT_SELECT, contact.value)
    
    @allure.step("设置邮箱")
    def set_email(self, email: str):
        """设置邮箱"""
        self.input_text(EMAIL_INPUT, email)
    
    def is_email_displayed(self) -> bool:
        """检查邮箱字段是否显示"""
        return self.is_element_visible(EMAIL_INPUT)
    
    @allure.step("设置电话")
    def set_tel(self, tel: str):
        """设置电话"""
        self.input_text(TEL_INPUT, tel)
    
    def is_tel_displayed(self) -> bool:
        """检查电话字段是否显示"""
        return self.is_element_visible(TEL_INPUT)
    
    @allure.step("设置备注")
    def set_comment(self, comment: str):
        """设置备注"""
        self.input_text(COMMENT_TEXTAREA, comment)
    
    @allure.step("跳转到确认页面")
    def go_to_confirm_page(self):
        """跳转到确认页面"""
        self.click_element(SUBMIT_BUTTON)
        from pages.confirm_page import ConfirmPage
        return ConfirmPage(self.driver)
    
    @allure.step("尝试跳转到确认页面（预期失败）")
    def go_to_confirm_page_expecting_failure(self):
        """尝试跳转到确认页面（预期失败）"""
        self.click_element(SUBMIT_BUTTON)
    
    def get_plan_name(self) -> str:
        """获取计划名称"""
        # 等待计划名称文本出现
        self.wait.until(lambda driver: re.search(r'\S+', self.get_text(PLAN_NAME_TEXT)))
        return self.get_text(PLAN_NAME_TEXT)
    
    def get_reserve_date(self) -> str:
        """获取预订日期"""
        return self.get_property(DATE_INPUT, "value")
    
    def get_reserve_term(self) -> str:
        """获取预订天数"""
        return self.get_property(TERM_INPUT, "value")
    
    def get_head_count(self) -> str:
        """获取人数"""
        return self.get_property(HEAD_COUNT_INPUT, "value")
    
    def get_username(self) -> str:
        """获取用户名"""
        return self.get_property(USERNAME_INPUT, "value")
    
    def get_email(self) -> str:
        """获取邮箱"""
        return self.get_property(EMAIL_INPUT, "value")
    
    def get_tel(self) -> str:
        """获取电话"""
        return self.get_property(TEL_INPUT, "value")
    
    def _get_message_with_fallback(self, primary_locator, fallback_locator) -> str:
        """获取错误消息的通用方法，支持备用定位符"""
        try:
            return self.get_text(primary_locator)
        except:
            try:
                return self.get_text(fallback_locator)
            except:
                return ""
    
    def get_reserve_date_message(self) -> str:
        """获取预订日期错误信息"""
        return self._get_message_with_fallback(
            DATE_MESSAGE,
            DATE_MESSAGE_ALT
        )
    
    def get_reserve_term_message(self) -> str:
        """获取预订天数错误信息"""
        return self._get_message_with_fallback(
            TERM_MESSAGE,
            TERM_MESSAGE_ALT
        )
    
    def get_head_count_message(self) -> str:
        """获取人数错误信息"""
        return self._get_message_with_fallback(
            HEAD_COUNT_MESSAGE,
            HEAD_COUNT_MESSAGE_ALT
        )
    
    def get_username_message(self) -> str:
        """获取用户名错误信息"""
        return self._get_message_with_fallback(
            USERNAME_MESSAGE,
            USERNAME_MESSAGE_ALT
        )
    
    def get_email_message(self) -> str:
        """获取邮箱错误信息"""
        return self._get_message_with_fallback(
            EMAIL_MESSAGE,
            EMAIL_MESSAGE_ALT
        )
    
    def get_tel_message(self) -> str:
        """获取电话错误信息"""
        return self._get_message_with_fallback(
            TEL_MESSAGE,
            TEL_MESSAGE_ALT
        )