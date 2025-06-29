# 酒店预订平台自动化测试项目 - Python Selenium with Pytest & Allure

这是一个基于Python + Selenium + Pytest + Allure的酒店预订平台自动化测试项目，采用Page Object Model设计模式。

## 技术栈

- **Python**: 3.12+
- **测试框架**: pytest 7.4.3
- **自动化框架**: Selenium WebDriver 4.15.2
- **测试报告**: Allure 2.13.2 + pytest-html
- **浏览器**: Chrome (with ChromeDriver)
- **数据管理**: PyYAML 6.0.1

## 项目结构

```
├── pages/                    # Page Object Model 页面类
│   ├── base_page.py         # 基础页面类
│   ├── top_page.py          # 首页
│   ├── login_page.py        # 登录页面
│   ├── signup_page.py       # 注册页面
│   ├── my_page.py           # 用户个人页面
│   ├── plans_page.py        # 套餐列表页面
│   ├── reserve_page.py      # 预订页面
│   ├── room_page.py         # 房间页面
│   ├── confirm_page.py      # 确认页面
│   └── icon_page.py         # 头像设置页面
├── testcase/                # 测试用例文件
│   ├── test_login.py        # 登录功能测试
│   ├── test_signup.py       # 用户注册测试
│   ├── test_plans.py        # 套餐查看测试
│   ├── test_redirection.py  # 页面跳转测试
│   ├── test_reserve.py      # 预订功能测试
│   └── test_mypage.py       # 个人页面功能测试
├── common/                  # 公共工具类
│   └── utils.py             # 工具函数
├── data/                    # 测试数据文件
│   ├── login_cases.yaml     # 登录测试用例数据
│   ├── signup_cases.yaml    # 注册测试用例数据
│   ├── mypage_cases.yaml    # 个人页面测试数据
│   ├── reserve_cases.yaml   # 预订功能测试数据
├── reports/                 # 测试报告目录
├── conftest.py             # Pytest 配置和夹具
└── run.py                  # 测试运行脚本
```

### 查看测试报告
```bash
# HTML报告
reports/report.html

# Allure报告
allure serve allure-results
```