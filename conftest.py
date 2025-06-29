import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# setup和teardown
@pytest.fixture(scope="class")
def driver():
    """测试类的WebDriver fixture"""
    service = Service(r'C:\Users\seeki\AppData\Local\Programs\Python\Python312\chromedriver.exe')
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False
    })
    
    # 检查无头模式的环境变量
    github_actions = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
    remote_containers = os.getenv('REMOTE_CONTAINERS', 'false').lower() == 'true'
    codespaces = os.getenv('CODESPACES', 'false').lower() == 'true'
    
    if github_actions:
        chrome_options.add_argument('--headless')
    elif remote_containers or codespaces:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def clear_cookies(driver):
    """每个测试后清除cookies"""
    yield
    driver.delete_all_cookies()


def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line(
        "markers", "order: 标记测试以特定顺序运行"
    ) 