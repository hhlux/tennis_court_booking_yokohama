from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):

    def login(self):
        url = 'https://www.shisetsu.city.yokohama.lg.jp/user/Login'
        self.driver.get(url)
        username_input = self.driver.find_element(By.NAME, 'UserLoginInputModel.Id')
        password_input = self.driver.find_element(By.NAME, 'UserLoginInputModel.Password')
        username_input.send_keys('02075758')
        password_input.send_keys('841010Lkm')
        self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="ログイン"]').click()
