from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from pages.base_page import BasePage


class ParkSelectionPage(BasePage):

    def go_to_park(self, park_name: str):
        self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'ul[role="tablist"] li:nth-child(6) a')),
            '没有找到 “施設名から探す”'
        ).click()

        park_name_input = self.driver.find_element(By.ID, '__BVID__255')
        park_name_input.clear()
        park_name_input.send_keys(park_name)

        # 点击 "検索" 按钮
        self.driver.find_element(By.CSS_SELECTOR, '#__BVID__253 > div > div.d-flex > button').click()

        # 选择检索结果的第一行
        self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                         '#jisMain > div > div.page-body.p-3.page-body-custom-padding > table > tbody > tr > td.p-1 > div'))
        ).click()

        # 点击 "次へ進む" 按钮
        self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="次へ進む"]').click()