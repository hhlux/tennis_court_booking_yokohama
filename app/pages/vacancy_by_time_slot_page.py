from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from pages.base_page import BasePage


class VacancyByTimeSlotPage(BasePage):

    def __init__(self):
        super().__init__()

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'li.events-group'))
        )
        # 滑到底部
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def is_last_time_slot_vacant_for_any_count(self) -> bool:
        result = False
        # 遍历选中的 courts
        lis = self.driver.find_elements(By.CSS_SELECTOR, 'li.events-group')
        for j in range(1, len(lis)):
           # 拿到 court 的最后一个时间段，也即 19:00 - 21:00
           time_slot = lis[j].find_element(By.CSS_SELECTOR, 'li:last-child div')

           if 'vacant' in time_slot.get_attribute('class').split():
               print('19:00-21:00 时段空缺')
               return True  # 只要有一个 court 在最后一个时间段可用即可

        print('19:00-21:00 时段满')
        return False

        # print(f'{date}: 没有19:00:-21:00的空缺')

    def return_page(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="前に戻る"]')),
            '"前に戻る"按钮无法点击'
        ).click()
