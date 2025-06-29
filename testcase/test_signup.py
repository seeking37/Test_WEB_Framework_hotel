import pytest
import allure
from datetime import date
from pages.top_page import TopPage
from pages.signup_page import Rank, Gender
from common.utils import Utils


@allure.feature("注册功能")
@pytest.mark.usefixtures("driver")
class TestSignup:
    
    @allure.story("用户注册")
    @allure.title("注册成功")
    @pytest.mark.parametrize("test_case", Utils.get_test_cases('../data/signup_cases.yaml', 'signup_success_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(1)
    def test_signup_success(self, driver, test_case):
        """测试用户成功注册"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            signup_page = top_page.go_to_signup_page()
            
            with allure.step("填写注册信息"):
                signup_page.set_email(test_case['email'])
                signup_page.set_password(test_case['password'])
                signup_page.set_password_confirmation(test_case['password_confirmation'])
                signup_page.set_username(test_case['username'])
                signup_page.set_rank(Rank(test_case['rank']))
                signup_page.set_address(test_case['address'])
                signup_page.set_tel(test_case['tel'])
                signup_page.set_gender(Gender(test_case['gender']))
                if test_case.get('birthday'):
                    birthday_str = test_case['birthday']
                    year, month, day = birthday_str.split('-')
                    birthday = date(int(year), int(month), int(day))
                    signup_page.set_birthday(birthday)
                signup_page.set_notification(test_case['notification'])
            
            my_page = signup_page.go_to_my_page()
            
            with allure.step("验证注册成功"):
                assert my_page.get_header_text() == test_case['expected_header']
    
    @allure.story("注册失败")
    @allure.title("注册失败")
    @pytest.mark.parametrize("test_case", Utils.get_test_cases('../data/signup_cases.yaml', 'signup_failure_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(2)
    def test_signup_failure(self, driver, test_case):
        """测试用户注册失败"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            signup_page = top_page.go_to_signup_page()
            
            with allure.step("填写注册信息"):
                signup_page.set_email(test_case['email'])
                signup_page.set_password(test_case['password'])
                signup_page.set_password_confirmation(test_case['password_confirmation'])
                signup_page.set_username(test_case['username'])
                signup_page.set_rank(Rank(test_case['rank']))
                signup_page.set_address(test_case['address'])
                signup_page.set_tel(test_case['tel'])
                signup_page.set_gender(Gender(test_case['gender']))
                if test_case.get('birthday'):
                    birthday_str = test_case['birthday']
                    year, month, day = birthday_str.split('-')
                    birthday = date(int(year), int(month), int(day))
                    signup_page.set_birthday(birthday)
                signup_page.set_notification(test_case['notification'])
            
            signup_page.go_to_my_page_expecting_failure()
            
            with allure.step("验证错误信息"):
                for field_name, expected_msg in test_case['expected_messages'].items():
                    if expected_msg:  # 只验证非空的错误消息
                        method_name = f"get_{field_name}_message"
                        actual_msg = getattr(signup_page, method_name)()
                        assert actual_msg == expected_msg, f"{field_name} 错误消息不匹配" 