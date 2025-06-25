import pytest
import allure
import os
from datetime import date
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from pages.top_page import TopPage
from pages.signup_page import Rank, Gender
from common.utils import Utils


@allure.feature("个人页面")
@pytest.mark.usefixtures("driver")
class TestMyPage:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, driver):
        """设置driver和WebDriverWait"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
    
    @allure.story("用户信息显示")
    @allure.title("应该显示预设用户clark的信息")
    @pytest.mark.order(1)
    def test_mypage_exist_user_one(self):
        """测试显示预设用户clark的信息"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("clark@example.com", "password")
        
        with allure.step("验证个人页面显示"):
            assert my_page.get_email() == "clark@example.com"
            assert my_page.get_username() == "Clark Evans"
            assert my_page.get_rank() == "Premium"
            assert my_page.get_address() == "Mountain View, California"
            assert my_page.get_tel() == "01234567891"
            assert my_page.get_gender() == "male"
            assert my_page.get_birthday() == "not answered"
            assert my_page.get_notification() == "received"
    
    @allure.story("用户信息显示")
    @allure.title("应该显示预设用户diana的信息")
    @pytest.mark.order(2)
    def test_mypage_exist_user_two(self):
        """测试显示预设用户diana的信息"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("diana@example.com", "pass1234")
        
        with allure.step("验证个人页面显示"):
            assert my_page.get_email() == "diana@example.com"
            assert my_page.get_username() == "Diana Johansson"
            assert my_page.get_rank() == "Normal"
            assert my_page.get_address() == "Redmond, Washington"
            assert my_page.get_tel() == "not answered"
            assert my_page.get_gender() == "female"
            assert my_page.get_birthday() == "April 1, 2000"
            assert my_page.get_notification() == "not received"
    
    @allure.story("用户信息显示")
    @allure.title("应该显示预设用户ororo的信息")
    @pytest.mark.order(3)
    def test_mypage_exist_user_three(self):
        """测试显示预设用户ororo的信息"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("ororo@example.com", "pa55w0rd!")
        
        with allure.step("验证个人页面显示"):
            assert my_page.get_email() == "ororo@example.com"
            assert my_page.get_username() == "Ororo Saldana"
            assert my_page.get_rank() == "Premium"
            assert my_page.get_address() == "Cupertino, California"
            assert my_page.get_tel() == "01212341234"
            assert my_page.get_gender() == "other"
            assert my_page.get_birthday() == "December 17, 1988"
            assert my_page.get_notification() == "not received"
    
    @allure.story("用户信息显示")
    @allure.title("应该显示预设用户miles的信息")
    @pytest.mark.order(4)
    def test_mypage_exist_user_four(self):
        """测试显示预设用户miles的信息"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("miles@example.com", "pass-pass")
        
        with allure.step("验证个人页面显示"):
            assert my_page.get_email() == "miles@example.com"
            assert my_page.get_username() == "Miles Boseman"
            assert my_page.get_rank() == "Normal"
            assert my_page.get_address() == "not answered"
            assert my_page.get_tel() == "01298765432"
            assert my_page.get_gender() == "not answered"
            assert my_page.get_birthday() == "August 31, 1992"
            assert my_page.get_notification() == "received"
    
    @allure.story("新用户信息显示")
    @allure.title("应该显示新用户信息")
    @pytest.mark.order(5)
    def test_mypage_new_user(self):
        """测试显示新用户信息"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        signup_page = top_page.go_to_signup_page()
        signup_page.set_email("new-user@example.com")
        signup_page.set_password("11111111")
        signup_page.set_password_confirmation("11111111")
        signup_page.set_username("Jane Doe")
        signup_page.set_rank(Rank.NORMAL)
        signup_page.set_address("Detroit, Michigan")
        signup_page.set_tel("09876543211")
        signup_page.set_gender(Gender.FEMALE)
        signup_page.set_birthday(date(2000, 1, 1))
        signup_page.set_notification(False)
        my_page = signup_page.go_to_my_page()
        
        with allure.step("验证个人页面显示"):
            assert my_page.get_email() == "new-user@example.com"
            assert my_page.get_username() == "Jane Doe"
            assert my_page.get_rank() == "Normal"
            assert my_page.get_address() == "Detroit, Michigan"
            assert my_page.get_tel() == "09876543211"
            assert my_page.get_gender() == "female"
            assert my_page.get_birthday() == "January 1, 2000"
            assert my_page.get_notification() == "not received"
    
    @allure.story("图标设置")
    @allure.title("选择非图片文件时应该显示错误")
    @pytest.mark.order(6)
    def test_icon_not_image(self):
        """测试选择非图片文件时的错误"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("new-user@example.com", "11111111")
        icon_page = my_page.go_to_icon_page()
        
        file_path = Path("data/resources/dummy.txt")
        icon_page.set_icon(file_path)
        
        assert icon_page.get_icon_message() == "Please select an image file."
    
    @allure.story("图标设置")
    @allure.title("选择超过10KB文件时应该显示错误")
    @pytest.mark.order(7)
    def test_icon_over_size(self):
        """测试选择超过10KB文件时的错误"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("new-user@example.com", "11111111")
        icon_page = my_page.go_to_icon_page()
        
        file_path = Path("data/resources/240x240_12.png")
        icon_page.set_icon(file_path)
        
        assert icon_page.get_icon_message() == "Please select a file with a size of 10 KB or less."
    
    @allure.story("图标设置")
    @allure.title("应该显示图标图片")
    @pytest.mark.order(8)
    def test_icon_success(self):
        """测试成功设置图标"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("new-user@example.com", "11111111")
        icon_page = my_page.go_to_icon_page()
        
        file_path = Path("data/resources/240x240_01.png")
        icon_page.set_icon(file_path)
        icon_page.set_zoom(80)
        icon_page.set_color(Color.from_string("black"))
        my_page = icon_page.go_to_my_page()
        
        with allure.step("验证图标图片"):
            assert my_page.exists_icon_image() == True
            assert my_page.get_icon_image_width() == 80 - 10  # -(padding + border)
            assert my_page.get_icon_image_border() == Color.from_string("black")
    
    @allure.story("用户删除")
    @allure.title("应该删除新用户")
    @pytest.mark.order(9)
    def test_delete_user(self):
        """测试删除新用户"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("new-user@example.com", "11111111")
        my_page.delete_user()
        
        # 等待确认对话框出现
        confirm_alert = self.wait.until(EC.alert_is_present())
        assert confirm_alert.text == "If you cancel your membership, all information will be deleted.\nDo you wish to proceed?"
        confirm_alert.accept()
        
        # 等待完成对话框出现
        complete_alert = self.wait.until(EC.alert_is_present())
        assert complete_alert.text == "The process has been completed. Thank you for your service."
        complete_alert.accept()
        
        # 验证重定向到首页
        self.wait.until(EC.url_contains("index.html"))
        current_url = self.driver.current_url
        assert current_url is not None
        assert "index.html" in current_url 