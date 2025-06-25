import pytest
import allure
from pages.top_page import TopPage
from common.utils import Utils


@allure.feature("预订方案")
@pytest.mark.usefixtures("driver")
class TestPlans:
    
    @allure.story("方案列表")
    @allure.title("未登录时应该显示方案列表")
    @pytest.mark.order(1)
    def test_plan_list_not_login(self, driver):
        """测试未登录时方案列表显示"""
        driver.get(Utils.BASE_URL)
        top_page = TopPage(driver)
        
        plans_page = top_page.go_to_plans_page()
        plan_titles = plans_page.get_plan_titles()
        
        with allure.step("验证方案"):
            assert len(plan_titles) == 7
            assert plan_titles[0] == "Plan with special offers"
            assert plan_titles[1] == "Staying without meals"
            assert plan_titles[2] == "Business trip"
            assert plan_titles[3] == "With beauty salon"
            assert plan_titles[4] == "With private onsen"
            assert plan_titles[5] == "For honeymoon"
            assert plan_titles[6] == "With complimentary ticket"
    
    @allure.story("方案列表")
    @allure.title("普通会员登录时应该显示方案列表")
    @pytest.mark.order(2)
    def test_plan_list_login_normal(self, driver):
        """测试普通会员登录时方案列表显示"""
        driver.get(Utils.BASE_URL)
        top_page = TopPage(driver)
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("diana@example.com", "pass1234")
        
        plans_page = my_page.go_to_plans_page()
        plan_titles = plans_page.get_plan_titles()
        
        with allure.step("验证方案"):
            assert len(plan_titles) == 9
            assert plan_titles[0] == "Plan with special offers"
            assert plan_titles[1] == "With dinner"
            assert plan_titles[2] == "Economical"
            assert plan_titles[3] == "Staying without meals"
            assert plan_titles[4] == "Business trip"
            assert plan_titles[5] == "With beauty salon"
            assert plan_titles[6] == "With private onsen"
            assert plan_titles[7] == "For honeymoon"
            assert plan_titles[8] == "With complimentary ticket"
    
    @allure.story("方案列表")
    @allure.title("高级会员登录时应该显示方案列表")
    @pytest.mark.order(3)
    def test_plan_list_login_premium(self, driver):
        """测试高级会员登录时方案列表显示"""
        driver.get(Utils.BASE_URL)
        top_page = TopPage(driver)
        login_page = top_page.go_to_login_page()
        my_page = login_page.do_login("clark@example.com", "password")
        
        plans_page = my_page.go_to_plans_page()
        plan_titles = plans_page.get_plan_titles()
        
        with allure.step("验证方案"):
            assert len(plan_titles) == 10
            assert plan_titles[0] == "Plan with special offers"
            assert plan_titles[1] == "Premium plan"
            assert plan_titles[2] == "With dinner"
            assert plan_titles[3] == "Economical"
            assert plan_titles[4] == "Staying without meals"
            assert plan_titles[5] == "Business trip"
            assert plan_titles[6] == "With beauty salon"
            assert plan_titles[7] == "With private onsen"
            assert plan_titles[8] == "For honeymoon"
            assert plan_titles[9] == "With complimentary ticket" 