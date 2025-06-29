import pytest
import allure
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from pages.top_page import TopPage
from pages.login_page import LoginPage
from pages.reserve_page import ReservePage, Contact
from pages.room_page import RoomPage
from common.utils import Utils
from common.read_data import TestDataLoader


@allure.feature("酒店预订功能（参数化）")
@pytest.mark.order(81)
class TestReserveParameterized:
    """酒店预订参数化测试类"""
    
    SHORT_FORMATTER = "%m/%d/%Y"
    LONG_FORMATTER = "%B %d, %Y"

    @pytest.fixture(autouse=True)
    def setup_driver(self, driver):
        """设置driver和WebDriverWait，并导航到基础URL"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        # 导航到基础URL
        self.driver.get(Utils.BASE_URL)
        # 记录原始窗口句柄
        self.original_handle = self.driver.current_window_handle
    # 钩子函数
    def teardown_method(self):
        """测试后清理"""
        if not (hasattr(self, 'driver') and self.driver):
            return
        
        try:
            # 获取所有窗口句柄
            current_handles = self.driver.window_handles
            
            # 关闭除原始窗口外的所有窗口
            for handle in current_handles:
                if handle != self.original_handle:
                    try:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                    except Exception:
                        pass  # 窗口可能已关闭，忽略
            
            # 切换回原始窗口，如果原始窗口不存在则切换到任意可用窗口
            remaining_handles = self.driver.window_handles
            if remaining_handles:
                target_handle = (self.original_handle if self.original_handle in remaining_handles 
                               else remaining_handles[0])
                self.driver.switch_to.window(target_handle)
                
        except Exception as e:
            print(f"Teardown error: {e}")  # 记录错误但不中断测试



    def _get_formatted_date(self, date_marker: str) -> str:
        """根据日期标记返回格式化日期"""
        if date_marker == "today":
            return datetime.now().strftime(self.SHORT_FORMATTER)
        elif date_marker == "tomorrow":
            return (datetime.now() + timedelta(days=1)).strftime(self.SHORT_FORMATTER)
        elif date_marker == "after_90_days":
            return (datetime.now() + timedelta(days=90)).strftime(self.SHORT_FORMATTER)
        elif date_marker == "after_91_days":
            return (datetime.now() + timedelta(days=91)).strftime(self.SHORT_FORMATTER)
        else:
            return date_marker

    def _setup_reserve_page(self, test_case):
        """设置预订页面的通用逻辑"""
        if test_case.get('is_logged_in', False):
            # 已登录用户流程
            top_page = TopPage(self.driver)
            login_page = top_page.go_to_login_page()
            my_page = login_page.do_login(test_case['login_email'], test_case['login_password'])
            original_handles = set(self.driver.window_handles)
            plans_page = my_page.go_to_plans_page()
        else:
            # 未登录用户流程
            top_page = TopPage(self.driver)
            original_handles = set(self.driver.window_handles)
            plans_page = top_page.go_to_plans_page()
        
        # 打开计划页面
        plans_page.open_plan_by_title(test_case['plan_title'])
        Utils.sleep(0.5)
        new_handles = set(self.driver.window_handles)
        new_handle = Utils.get_new_window_handle(original_handles, new_handles)
        self.driver.switch_to.window(new_handle)
        return ReservePage(self.driver)

    @allure.story("页面初始值显示")
    @allure.title("页面初始值验证")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/reserve_cases.yaml', 'page_init_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(1)
    def test_page_init_values(self, driver, test_case):
        """测试页面初始值显示"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            reserve_page = self._setup_reserve_page(test_case)
            
            tomorrow = (datetime.now() + timedelta(days=1)).strftime(self.SHORT_FORMATTER)
            
            # 验证初始值
            with allure.step("验证初始值"):
                assert reserve_page.get_plan_name() == test_case['expected_plan_name']
                assert reserve_page.get_reserve_date() == tomorrow
                assert reserve_page.get_reserve_term() == test_case['expected_reserve_term']
                assert reserve_page.get_head_count() == test_case['expected_head_count']
                
                if test_case['has_login_data']:
                    assert reserve_page.get_username() == test_case['expected_username']
                
                assert not reserve_page.is_email_displayed()
                assert not reserve_page.is_tel_displayed()
            
            # 测试邮箱联系方式
            reserve_page.set_contact(Contact.EMAIL)
            with allure.step("验证邮箱联系方式"):
                assert reserve_page.is_email_displayed()
                assert not reserve_page.is_tel_displayed()
                assert reserve_page.get_email() == test_case['expected_email']
            
            # 测试电话联系方式
            reserve_page.set_contact(Contact.TELEPHONE)
            with allure.step("验证电话联系方式"):
                assert not reserve_page.is_email_displayed()
                assert reserve_page.is_tel_displayed()
                assert reserve_page.get_tel() == test_case['expected_tel']
            
            # 验证房间信息
            self.driver.switch_to.frame("room")
            room_page = RoomPage(self.driver)
            assert room_page.get_header() == test_case['expected_room_header']
            self.driver.switch_to.default_content()

    @allure.story("输入验证")
    @allure.title("输入验证测试")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/reserve_cases.yaml', 'input_validation_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(2)
    def test_input_validation(self, driver, test_case):
        """测试输入验证"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            # 设置为未登录用户场景
            test_case_setup = {'is_logged_in': False, 'plan_title': test_case['plan_title']}
            reserve_page = self._setup_reserve_page(test_case_setup)
            
            # 处理特殊日期标记
            reserve_date = self._get_formatted_date(test_case['reserve_date'])
            
            # 设置输入值
            reserve_page.set_reserve_date(reserve_date)
            reserve_page.set_reserve_term(test_case['reserve_term'])
            reserve_page.set_head_count(test_case['head_count'])
            reserve_page.set_username(test_case['username'])  # 移动焦点
            
            # 验证错误消息
            with allure.step("验证错误消息"):
                for field_name, expected_msg in test_case['expected_messages'].items():
                    method_name = f"get_{field_name}_message"
                    actual_msg = getattr(reserve_page, method_name)()
                    if expected_msg is not None:
                        assert actual_msg == expected_msg, f"{field_name} 错误消息不匹配"
                    else:
                        assert actual_msg is not None

    @allure.story("提交验证")
    @allure.title("提交验证测试")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/reserve_cases.yaml', 'submit_validation_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(3)
    def test_submit_validation(self, driver, test_case):
        """测试提交验证"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            # 设置为未登录用户场景
            test_case_setup = {'is_logged_in': False, 'plan_title': test_case['plan_title']}
            reserve_page = self._setup_reserve_page(test_case_setup)
            
            # 设置输入值
            reserve_page.set_username(test_case['username'])
            
            # 设置联系方式
            if test_case['contact_type'] == 'email':
                reserve_page.set_contact(Contact.EMAIL)
                reserve_page.set_email(test_case['email'])
            elif test_case['contact_type'] == 'tel':
                reserve_page.set_contact(Contact.TELEPHONE)
                reserve_page.set_tel(test_case['tel'])
            
            # 尝试提交（期望失败）
            reserve_page.go_to_confirm_page_expecting_failure()
            
            # 验证错误消息
            with allure.step("验证错误消息"):
                for field_name, expected_msg in test_case['expected_messages'].items():
                    method_name = f"get_{field_name}_message"
                    actual_msg = getattr(reserve_page, method_name)()
                    assert actual_msg == expected_msg, f"{field_name} 错误消息不匹配"

    @allure.story("预订成功")
    @allure.title("预订成功测试")
    @pytest.mark.parametrize("test_case", TestDataLoader.get_test_cases('../data/reserve_cases.yaml', 'reserve_success_cases'), ids=lambda x: x['id'])
    @pytest.mark.order(4)
    def test_reserve_success(self, driver, test_case):
        """测试预订成功"""
        with allure.step(f"执行测试用例: {test_case['description']}"):
            reserve_page = self._setup_reserve_page(test_case)
            
            # 计算预期的日期和价格
            if test_case['reserve_date'] == 'tomorrow':
                expected_start = datetime.now() + timedelta(days=1)
            elif test_case['reserve_date'] == 'after_90_days':
                expected_start = datetime.now() + timedelta(days=90)
            else:
                expected_start = datetime.now() + timedelta(days=1)  # 默认明天
            
            expected_end = expected_start + timedelta(days=int(test_case['reserve_term']))
            expected_term = f"{expected_start.strftime(self.LONG_FORMATTER)} - {expected_end.strftime(self.LONG_FORMATTER)}. {test_case['reserve_term']} night(s)"
            
            # 根据计划和星期几计算总金额
            if test_case['plan_title'] == "Plan with special offers":
                if expected_start.weekday() in [5, 6]:  # 周六日
                    expected_total_bill = "Total $87.50 (included taxes)"
                else:
                    expected_total_bill = "Total $70.00 (included taxes)"
            else:  # Premium plan
                if expected_start.weekday() == 5:  # 周六
                    expected_total_bill = "Total $1,120.00 (included taxes)"
                elif expected_start.weekday() in [4, 6]:  # 周五或周日
                    expected_total_bill = "Total $1,020.00 (included taxes)"
                else:
                    expected_total_bill = "Total $920.00 (included taxes)"
            
            # 根据测试类型设置不同的字段
            if test_case['id'] == 'guest_user_success':
                # 未登录用户测试：只设置用户名和联系方式（与Java版本一致）
                reserve_page.set_username(test_case['username'])
                reserve_page.set_contact(Contact.NO)
            else:
                # 已登录用户测试：按照Java版本的确切顺序设置所有字段
                reserve_page.set_reserve_term(test_case['reserve_term'])
                reserve_page.set_head_count(test_case['head_count'])
                
                # 设置额外服务
                if test_case.get('breakfast_plan'):
                    reserve_page.set_breakfast_plan(test_case['breakfast_plan'])
                if test_case.get('early_check_in_plan'):
                    reserve_page.set_early_check_in_plan(test_case['early_check_in_plan'])
                if test_case.get('sightseeing_plan') is not None:
                    reserve_page.set_sightseeing_plan(test_case['sightseeing_plan'])
                
                # 设置联系方式
                if test_case['contact_type'] == 'email':
                    reserve_page.set_contact(Contact.EMAIL)
                    if test_case.get('email'):
                        reserve_page.set_email(test_case['email'])
                elif test_case['contact_type'] == 'tel':
                    reserve_page.set_contact(Contact.TELEPHONE)
                    if test_case.get('tel'):
                        reserve_page.set_tel(test_case['tel'])
                elif test_case['contact_type'] == 'no':
                    reserve_page.set_contact(Contact.NO)
                
                # 设置备注
                if test_case.get('comment'):
                    reserve_page.set_comment(test_case['comment'])
                
                # 最后设置日期
                reserve_page.set_reserve_date(self._get_formatted_date(test_case['reserve_date']))
            
            # 提交预订
            confirm_page = reserve_page.go_to_confirm_page()
            
            # 验证确认页面信息
            with allure.step("验证确认预订信息"):
                assert confirm_page.get_total_bill() == expected_total_bill
                assert confirm_page.get_plan_name() == test_case['expected_plan_name']
                assert confirm_page.get_term() == expected_term
                assert confirm_page.get_head_count() == test_case['expected_head_count']
                
                # 验证额外服务
                if 'expected_plans_contain' in test_case:
                    plans_text = confirm_page.get_plans()
                    for plan in test_case['expected_plans_contain']:
                        assert plan in plans_text
                    for plan in test_case['expected_plans_not_contain']:
                        assert plan not in plans_text
                else:
                    assert confirm_page.get_plans() == test_case['expected_plans']
                
                assert confirm_page.get_username() == test_case['expected_username']
                assert confirm_page.get_contact() == test_case['expected_contact']
                assert confirm_page.get_comment() == test_case['expected_comment']
            
            # 确认预订
            confirm_page.do_confirm()
            assert confirm_page.get_modal_message() == test_case['expected_modal_message']
            confirm_page.close()
            
            # 窗口应该自动关闭回到主窗口
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda driver: len(driver.window_handles) == 1) 