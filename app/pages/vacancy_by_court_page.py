import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from pages.base_page import BasePage


class VacancyByCourtPage(BasePage):

    def __init__(self):
        super().__init__()
        # 等到表格出现，确认画面加载完毕
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'table.table-schedule'))
        )
        # 滑到底部
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def select_one_month(self) -> int:
        # 选择 "一ヶ月"
        self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                         '#app_page > form > div.application-main > div > div.d-flex.select-days-header > div.card.card-body.disp-condition > dl > dd > div > div:nth-child(3) > div > div:nth-child(4)'))
        ).click()

        # 点击 "表示の変更" 按钮
        self.driver.find_element(By.CSS_SELECTOR, '#app_page > form > div.application-main > div > div.d-flex.select-days-header > div.card.card-body.disp-condition > div.d-flex.justify-content-end.align-items-end > button'). click()

        time.sleep(2)

        days_count = len(self.driver.find_elements(By.TAG_NAME, 'th')) - 2
        print(f'总共有{days_count}天')

        return days_count

    def get_date(self, date_index: int):
        th = self.driver.find_element(By.CSS_SELECTOR, f'thead > tr > th:nth-child({date_index})')
        date = th.text.replace('\n', '')
        return date

    def click_next_if_any_court_is_vacant_by_date(self, date_index: int, court_count: int) -> bool:
        # 日期显示在 th 中，取出日期
        th = self.driver.find_element(By.CSS_SELECTOR, f'thead > tr > th:nth-child({date_index})')
        date = th.text.replace('\n', '')

        # 判断这一天里是否有球场有空缺
        check_further = False
        # 遍历4个球场
        for i in range(1, court_count + 1):
            # court_name = self.driver.find_element(By.CSS_SELECTOR, f'tbody > tr:nth-child({i}) > td:nth-child(1)').text
            # print(court_name)
            td = self.driver.find_element(By.CSS_SELECTOR, f'tbody > tr:nth-child({i}) > td:nth-child({date_index})')
            classes = td.find_element(By.TAG_NAME, 'label').get_attribute('class').split()
            # Circle icon: vacant; triangle icon: some
            if 'vacant' in classes or 'some' in classes:
                # print('ok')
                td.click()
                check_further = True

        if not check_further:
            print(f'{date} 没有球场空缺')
            return False
        else:
            print(f'{date} 有球场空缺，进一步查看是否有19:00-21:00的空缺')
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="次へ進む"]').click()
            return True

    def clear_selected(self):

        tds = self.driver.find_elements(By.CSS_SELECTOR, f'tbody > tr > td')
        for td in tds:
            labels = td.find_elements(By.TAG_NAME, 'label')
            if len(labels) > 0:
                if 'active' in labels[0].get_attribute('class').split():
                    td.click()