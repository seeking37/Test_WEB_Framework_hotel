from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from typing import List


class PlansPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_title_contains("Plans")
        self.verify_page_title("Plans")
    
    def get_plan_titles(self) -> List[str]:
        """Get list of plan titles"""
        # Wait for loading to complete
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#plan-list > div[role=\"status\"]")))
        plans = self.driver.find_elements(By.CLASS_NAME, "card-title")
        return [plan.text for plan in plans]
    
    def open_plan_by_title(self, title: str) -> None:
        """Open plan by title"""
        # Wait for loading to complete
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#plan-list > div[role=\"status\"]")))
        plans = self.driver.find_elements(By.CLASS_NAME, "card")
        
        for plan in plans:
            plan_title = plan.find_element(By.CLASS_NAME, "card-title").text
            if plan_title == title:
                link = plan.find_element(By.TAG_NAME, "a")
                link.click()
                break
        
        # Wait for new window to open
        self.wait.until(EC.number_of_windows_to_be(2)) 