import pytest
import allure
from datetime import date
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from pages.top_page import TopPage
from pages.signup_page import Rank, Gender
from common.utils import Utils
from common.read_data import TestDataLoader


@allure.feature("个人页面")
@pytest.mark.usefixtures("driver")
class TestMyPageParameterized:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, driver):
        """设置driver和WebDriverWait，并导航到基础URL"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        # 导航到基础URL
        self.driver.get(Utils.BASE_URL)
    
    @allure.story("预设用户信息显示")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/mypage_cases.yaml', 'existing_users_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(1)
    def test_existing_users_info(self, test_case):
        """测试预设用户信息显示"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            top_page = TopPage(self.driver)
            
            # 登录用户
            login_page = top_page.go_to_login_page()
            my_page = login_page.do_login(test_case['email'], test_case['password'])
            
            # 验证用户信息
            expected = test_case['expected_data']
            with allure.step("验证个人页面显示"):
                assert my_page.get_email() == expected['email']
                assert my_page.get_username() == expected['username']
                assert my_page.get_rank() == expected['rank']
                assert my_page.get_address() == expected['address']
                assert my_page.get_tel() == expected['tel']
                assert my_page.get_gender() == expected['gender']
                assert my_page.get_birthday() == expected['birthday']
                assert my_page.get_notification() == expected['notification']
    
    @allure.story("新用户信息显示")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/mypage_cases.yaml', 'new_user_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(2)
    def test_new_user_info(self, test_case):
        """测试新用户注册后信息显示"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            top_page = TopPage(self.driver)
            
            # 注册新用户
            signup_page = top_page.go_to_signup_page()
            signup_data = test_case['signup_data']
            
            signup_page.set_email(signup_data['email'])
            signup_page.set_password(signup_data['password'])
            signup_page.set_password_confirmation(signup_data['password_confirmation'])
            signup_page.set_username(signup_data['username'])
            
            # 设置会员等级
            rank = Rank.NORMAL if signup_data['rank'] == 'NORMAL' else Rank.PREMIUM
            signup_page.set_rank(rank)
            
            signup_page.set_address(signup_data['address'])
            signup_page.set_tel(signup_data['tel'])
            
            # 设置性别
            gender_map = {
                'FEMALE': Gender.FEMALE,
                'MALE': Gender.MALE,
                'OTHER': Gender.OTHER,
                'NOT_ANSWER': Gender.NOT_ANSWER
            }
            gender = gender_map[signup_data['gender']]
            signup_page.set_gender(gender)
            
            # 设置生日
            birthday_str = signup_data['birthday']
            if birthday_str:
                year, month, day = birthday_str.split('-')
                birthday = date(int(year), int(month), int(day))
                signup_page.set_birthday(birthday)
            
            signup_page.set_notification(signup_data['notification'])
            my_page = signup_page.go_to_my_page()
            
            # 验证用户信息
            expected = test_case['expected_data']
            with allure.step("验证个人页面显示"):
                assert my_page.get_email() == expected['email']
                assert my_page.get_username() == expected['username']
                assert my_page.get_rank() == expected['rank']
                assert my_page.get_address() == expected['address']
                assert my_page.get_tel() == expected['tel']
                assert my_page.get_gender() == expected['gender']
                assert my_page.get_birthday() == expected['birthday']
                assert my_page.get_notification() == expected['notification']
    
    @allure.story("图标设置")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/mypage_cases.yaml', 'icon_test_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(3)
    def test_icon_settings(self, test_case):
        """测试图标设置功能"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            top_page = TopPage(self.driver)
            
            # 登录用户
            login_data = test_case['login_data']
            login_page = top_page.go_to_login_page()
            my_page = login_page.do_login(login_data['email'], login_data['password'])
            icon_page = my_page.go_to_icon_page()
            
            # 设置图标
            icon_data = test_case['icon_data']
            file_path = Path(icon_data['file_path'])
            icon_page.set_icon(file_path)
            
            # 如果有zoom和color设置
            if icon_data['zoom'] is not None:
                icon_page.set_zoom(icon_data['zoom'])
            if icon_data['color'] is not None:
                icon_page.set_color(Color.from_string(icon_data['color']))
            
            # 验证结果
            if test_case['expected_success']:
                # 成功设置图标
                my_page = icon_page.go_to_my_page()
                expected_results = test_case['expected_results']
                
                with allure.step("验证图标设置成功"):
                    assert my_page.exists_icon_image() == expected_results['image_exists']
                    assert my_page.get_icon_image_width() == expected_results['image_width']
                    assert my_page.get_icon_image_border() == Color.from_string(expected_results['border_color'])
            else:
                # 验证错误消息
                with allure.step("验证错误消息"):
                    assert icon_page.get_icon_message() == test_case['expected_message']
    
    @allure.story("用户删除")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/mypage_cases.yaml', 'delete_user_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(4)
    def test_delete_user(self, test_case):
        """测试用户删除功能"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            top_page = TopPage(self.driver)
            
            # 登录用户
            login_data = test_case['login_data']
            login_page = top_page.go_to_login_page()
            my_page = login_page.do_login(login_data['email'], login_data['password'])
            
            # 删除用户
            my_page.delete_user()
            
            # 验证确认对话框
            with allure.step("验证确认对话框"):
                confirm_alert = self.wait.until(EC.alert_is_present())
                assert confirm_alert.text == test_case['expected_confirm_message']
                confirm_alert.accept()
            
            # 验证完成对话框
            with allure.step("验证完成对话框"):
                complete_alert = self.wait.until(EC.alert_is_present())
                assert complete_alert.text == test_case['expected_complete_message']
                complete_alert.accept()
            
            # 验证重定向
            with allure.step("验证重定向到首页"):
                self.wait.until(EC.url_contains(test_case['expected_redirect_url']))
                current_url = self.driver.current_url
                assert current_url is not None
                assert test_case['expected_redirect_url'] in current_url 