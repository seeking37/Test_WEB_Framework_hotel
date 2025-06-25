import pytest
import allure
from pages.top_page import TopPage
from common.utils import Utils
from common.read_data import TestDataLoader


@allure.feature("登录功能")
@pytest.mark.usefixtures("driver")
class TestLogin:
    
    @allure.story("登录成功")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_login_success_cases(), ids=lambda x: x['id'])
    @pytest.mark.order(1)
    def test_login_success(self, driver, test_case):
        """测试用户成功登录"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            
            login_page = top_page.go_to_login_page()
            my_page = login_page.do_login(test_case['email'], test_case['password'])
            
            assert my_page.get_header_text() == test_case['expected_header']
    
    @allure.story("登录失败")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_login_failure_cases(), ids=lambda x: x['id'])
    @pytest.mark.order(2)
    def test_login_failure(self, driver, test_case):
        """测试用户登录失败"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            driver.get(Utils.BASE_URL)
            top_page = TopPage(driver)
            
            login_page = top_page.go_to_login_page()
            login_page.do_login_expecting_failure(test_case['email'], test_case['password'])
            
            with allure.step("验证错误信息"):
                if test_case['expected_email_msg']:
                    assert login_page.get_email_message() == test_case['expected_email_msg']
                if test_case['expected_password_msg']:
                    assert login_page.get_password_message() == test_case['expected_password_msg'] 