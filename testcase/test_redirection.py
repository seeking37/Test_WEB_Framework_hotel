import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.top_page import TopPage
from common.utils import Utils


@allure.feature("页面重定向")
@pytest.mark.usefixtures("driver")
class TestRedirection:
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, driver):
        """设置driver和WebDriverWait"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
    
    @allure.story("页面重定向")
    @allure.title("未登录时个人页面应该重定向到首页")
    @pytest.mark.order(1)
    def test_mypage_to_top(self):
        """测试未登录时从个人页面重定向到首页"""
        self.driver.get(Utils.BASE_URL + "/mypage.html")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("页面重定向")
    @allure.title("已登录时登录页面应该重定向到首页")
    @pytest.mark.order(2)
    def test_login_page_to_top(self):
        """测试已登录时从登录页面重定向到首页"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        login_page.do_login("clark@example.com", "password")
        
        self.driver.get(Utils.BASE_URL + "/login.html")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("页面重定向")
    @allure.title("已登录时注册页面应该重定向到首页")
    @pytest.mark.order(3)
    def test_signup_page_to_top(self):
        """测试已登录时从注册页面重定向到首页"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        login_page.do_login("clark@example.com", "password")
        
        self.driver.get(Utils.BASE_URL + "/signup.html")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("无效方案访问")
    @allure.title("无效方案ID时预订页面应该重定向到首页[1]")
    @pytest.mark.order(4)
    def test_no_plan_page_to_top(self):
        """测试访问不存在的方案ID 100时重定向"""
        self.driver.get(Utils.BASE_URL + "/reserve.html?plan-id=100")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("无效方案访问")
    @allure.title("无效方案ID时预订页面应该重定向到首页[2]")
    @pytest.mark.order(5)
    def test_invalid_plan_page_to_top(self):
        """测试访问无效格式方案ID时重定向"""
        self.driver.get(Utils.BASE_URL + "/reserve.html?plan-id=abc")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("无效方案访问")
    @allure.title("无效方案ID时预订页面应该重定向到首页[3]")
    @pytest.mark.order(6)
    def test_invalid_param_plan_page_to_top(self):
        """测试访问预订页面没有方案ID参数时重定向"""
        self.driver.get(Utils.BASE_URL + "/reserve.html")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("会员访问控制")
    @allure.title("未登录用户访问会员方案时应该重定向到首页")
    @pytest.mark.order(7)
    def test_member_only_plan_page_to_top(self):
        """测试未登录用户尝试访问会员专属方案时重定向"""
        self.driver.get(Utils.BASE_URL + "/reserve.html?plan-id=3")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("高级会员访问控制")
    @allure.title("未登录用户访问高级会员方案时应该重定向到首页")
    @pytest.mark.order(8)
    def test_premium_only_plan_page_to_top(self):
        """测试未登录用户尝试访问高级会员专属方案时重定向"""
        self.driver.get(Utils.BASE_URL + "/reserve.html?plan-id=1")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("高级会员访问控制")
    @allure.title("普通用户访问高级会员方案时应该重定向到首页")
    @pytest.mark.order(9)
    def test_premium_only_plan_normal_member_page_to_top(self):
        """测试普通会员尝试访问高级会员专属方案时重定向"""
        self.driver.get(Utils.BASE_URL)
        top_page = TopPage(self.driver)
        
        login_page = top_page.go_to_login_page()
        login_page.do_login("diana@example.com", "pass1234")
        
        self.driver.get(Utils.BASE_URL + "/reserve.html?plan-id=1")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html")
    
    @allure.story("直接访问控制")
    @allure.title("直接访问确认页面时应该重定向到首页")
    @pytest.mark.order(10)
    def test_invalid_param_confirm_page_to_top(self):
        """测试直接访问确认页面而没有正确流程时重定向"""
        self.driver.get(Utils.BASE_URL + "/confirm.html")
        self.wait.until(EC.url_contains("index.html"))
        
        current_url = self.driver.current_url
        assert current_url is not None
        assert current_url.endswith("index.html") 