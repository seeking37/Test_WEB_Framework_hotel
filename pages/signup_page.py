from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from datetime import date
from enum import Enum
from typing import Optional


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
        """Set email field"""
        email_input = self.driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email)
    
    def set_password(self, password: str) -> None:
        """Set password field"""
        password_input = self.driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)
    
    def set_password_confirmation(self, password: str) -> None:
        """Set password confirmation field"""
        password_confirmation_input = self.driver.find_element(By.ID, "password-confirmation")
        password_confirmation_input.clear()
        password_confirmation_input.send_keys(password)
    
    def set_username(self, username: str) -> None:
        """Set username field"""
        username_input = self.driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(username)
    
    def set_rank(self, rank: Rank) -> None:
        """Set rank radio button"""
        if rank == Rank.PREMIUM:
            premium_radio = self.driver.find_element(By.ID, "rank-premium")
            premium_radio.click()
        elif rank == Rank.NORMAL:
            normal_radio = self.driver.find_element(By.ID, "rank-normal")
            normal_radio.click()
        else:
            raise ValueError(f"Invalid rank: {rank}")
    
    def set_address(self, address: str) -> None:
        """Set address field"""
        address_input = self.driver.find_element(By.ID, "address")
        address_input.clear()
        address_input.send_keys(address)
    
    def set_tel(self, tel: str) -> None:
        """Set telephone field"""
        tel_input = self.driver.find_element(By.ID, "tel")
        tel_input.clear()
        tel_input.send_keys(tel)
    
    def set_gender(self, gender: Gender) -> None:
        """Set gender dropdown"""
        gender_select = Select(self.driver.find_element(By.ID, "gender"))
        gender_select.select_by_value(gender.value)
    
    def set_birthday(self, birthday: Optional[date]) -> None:
        """Set birthday field using JavaScript"""
        birthday_str = birthday.strftime("%Y-%m-%d") if birthday else ""
        birthday_input = self.driver.find_element(By.ID, "birthday")
        self.driver.execute_script("arguments[0].value = arguments[1]", birthday_input, birthday_str)
    
    def set_notification(self, checked: bool) -> None:
        """Set notification checkbox"""
        notification_check = self.driver.find_element(By.ID, "notification")
        if notification_check.is_selected() != checked:
            notification_check.click()
    
    def go_to_my_page(self):
        """Submit signup form and go to my page"""
        signup_button = self.driver.find_element(By.CSS_SELECTOR, "#signup-form > button")
        signup_button.click()
        
        # Import here to avoid circular import
        from pages.my_page import MyPage
        return MyPage(self.driver)
    
    def go_to_my_page_expecting_failure(self) -> None:
        """Submit signup form expecting failure"""
        signup_button = self.driver.find_element(By.CSS_SELECTOR, "#signup-form > button")
        signup_button.click()
    
    def get_email_message(self) -> str:
        """Get email validation message"""
        email_message = self.driver.find_element(By.CSS_SELECTOR, "#email ~ .invalid-feedback")
        return email_message.text
    
    def get_password_message(self) -> str:
        """Get password validation message"""
        password_message = self.driver.find_element(By.CSS_SELECTOR, "#password ~ .invalid-feedback")
        return password_message.text
    
    def get_password_confirmation_message(self) -> str:
        """Get password confirmation validation message"""
        password_confirmation_message = self.driver.find_element(By.CSS_SELECTOR, "#password-confirmation ~ .invalid-feedback")
        return password_confirmation_message.text
    
    def get_username_message(self) -> str:
        """Get username validation message"""
        username_message = self.driver.find_element(By.CSS_SELECTOR, "#username ~ .invalid-feedback")
        return username_message.text
    
    def get_address_message(self) -> str:
        """Get address validation message"""
        address_message = self.driver.find_element(By.CSS_SELECTOR, "#address ~ .invalid-feedback")
        return address_message.text
    
    def get_tel_message(self) -> str:
        """Get telephone validation message"""
        tel_message = self.driver.find_element(By.CSS_SELECTOR, "#tel ~ .invalid-feedback")
        return tel_message.text
    
    def get_gender_message(self) -> str:
        """Get gender validation message"""
        gender_message = self.driver.find_element(By.CSS_SELECTOR, "#gender ~ .invalid-feedback")
        return gender_message.text
    
    def get_birthday_message(self) -> str:
        """Get birthday validation message"""
        birthday_message = self.driver.find_element(By.CSS_SELECTOR, "#birthday ~ .invalid-feedback")
        return birthday_message.text 