from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List

# ================== 方案页面定位符 ==================
LOADING_INDICATOR = (By.CSS_SELECTOR, "#plan-list > div[role=\"status\"]")
PLAN_CARDS = (By.CLASS_NAME, "card")
PLAN_TITLES = (By.CLASS_NAME, "card-title")
PLAN_LINK = (By.TAG_NAME, "a")


class PlansPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Plans")
        self.verify_page_title("Plans")
    
    def get_plan_titles(self) -> List[str]:
        """获取计划标题列表"""
        # 等待加载完成
        self.wait_for_element_disappear(LOADING_INDICATOR)
        
        # 获取所有计划标题
        plan_elements = self.find_elements(PLAN_TITLES)
        return [plan.text for plan in plan_elements]
    
    def open_plan_by_title(self, title: str) -> None:
        """根据标题打开计划"""
        # 等待加载完成
        self.wait_for_element_disappear(LOADING_INDICATOR)
        
        # 获取所有计划卡片
        plan_cards = self.find_elements(PLAN_CARDS)
        
        for plan_card in plan_cards:
            # 在每个卡片中查找标题
            title_elements = plan_card.find_elements(*PLAN_TITLES)
            if title_elements and title_elements[0].text == title:
                # 找到匹配的计划，点击链接
                link_elements = plan_card.find_elements(*PLAN_LINK)
                if link_elements:
                    link_elements[0].click()
                    break
        
        # 等待新窗口打开
        self.wait.until(lambda driver: len(driver.window_handles) == 2) 