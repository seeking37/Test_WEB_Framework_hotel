import pytest
import allure
from datetime import date
from pages.top_page import TopPage
from pages.signup_page import Rank, Gender
from common.utils import Utils
from common.read_data import TestDataLoader


@allure.feature("用户注册")
@pytest.mark.usefixtures("driver")
class TestSignup:
    
    def _set_signup_form(self, signup_page, test_case):
        """设置注册表单数据"""
        signup_page.set_email(test_case['email'])
        signup_page.set_password(test_case['password'])
        signup_page.set_password_confirmation(test_case['password_confirmation'])
        signup_page.set_username(test_case['username'])
        signup_page.set_rank(getattr(Rank, test_case['rank']))
        signup_page.set_address(test_case['address'])
        signup_page.set_tel(test_case['tel'])
        signup_page.set_gender(getattr(Gender, test_case['gender']))
        
        # 处理生日字段
        if test_case['birthday']:
            birthday_date = date.fromisoformat(test_case['birthday'])
            signup_page.set_birthday(birthday_date)
        else:
            signup_page.set_birthday(None)
            
        signup_page.set_notification(test_case['notification'])
    
    @allure.story("注册成功")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_signup_success_cases(), ids=lambda x: x['id'])
    @pytest.mark.order(1)
    def test_signup_success(self, driver, test_case):
        """测试用户成功注册"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            
            signup_page = top_page.go_to_signup_page()
            self._set_signup_form(signup_page, test_case)
            my_page = signup_page.go_to_my_page()
            
            assert my_page.get_header_text() == test_case['expected_header']
    
    @allure.story("注册失败")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_signup_failure_cases(), ids=lambda x: x['id'])
    @pytest.mark.order(2)
    def test_signup_failure(self, driver, test_case):
        """测试用户注册失败"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            
            signup_page = top_page.go_to_signup_page()
            self._set_signup_form(signup_page, test_case)
            signup_page.go_to_my_page_expecting_failure()
            
            with allure.step("验证错误信息"):
                expected_msgs = test_case['expected_messages']
                
                if expected_msgs['email']:
                    assert signup_page.get_email_message() == expected_msgs['email']
                if expected_msgs['password']:
                    assert signup_page.get_password_message() == expected_msgs['password']
                if expected_msgs['password_confirmation']:
                    assert signup_page.get_password_confirmation_message() == expected_msgs['password_confirmation']
                if expected_msgs['username']:
                    assert signup_page.get_username_message() == expected_msgs['username']
                if expected_msgs['address']:
                    assert signup_page.get_address_message() == expected_msgs['address']
                if expected_msgs['tel']:
                    assert signup_page.get_tel_message() == expected_msgs['tel']
                if expected_msgs['gender']:
                    assert signup_page.get_gender_message() == expected_msgs['gender']
                if expected_msgs['birthday']:
                    assert signup_page.get_birthday_message() == expected_msgs['birthday'] 