import platform
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

import const
from utils.cloud_storage_util import CloudStorageUtil


class BasePage:

    driver: WebDriver = None
    wait: WebDriverWait = None
    wait_long: WebDriverWait = None
    wait_super_long: WebDriverWait = None

    def __init__(self):

        if BasePage.driver is None:
            # options = webdriver.ChromeOptions()
            options = Options()
            prefs = {
                'download.prompt_for_download': False
            }
            user_agent_list = [
                # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            ]
            options.add_experimental_option('prefs', prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--disable-application-cache')
            options.add_argument('window-size=1920,1080')
            options.add_argument('--user-agent=' + random.choice(user_agent_list))
            if platform.system() != 'Darwin':  # For Cloud Run
                options.binary_location = '/usr/bin/google-chrome'
                options.add_argument('--headless=new')
                options.add_argument("--start-maximized")
            # options.add_experimental_option("prefs", {"download.default_directory": str(const.DOWNLOAD_FOLDER.absolute())})
            BasePage.driver = webdriver.Chrome(options=options)
            BasePage.driver.maximize_window()
            # BasePage.driver.implicitly_wait(1)
            BasePage.wait = WebDriverWait(BasePage.driver, 10)
            BasePage.wait_long = WebDriverWait(BasePage.driver, 60)
            BasePage.wait_super_long = WebDriverWait(BasePage.driver, 600)

    def take_screenshot_and_upload_to_cloud_storage(self) -> str:
        data = self.driver.get_screenshot_as_png()
        page_title = '_'.join(self.driver.title.split())
        file_name = f'{page_title}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        CloudStorageUtil.upload_blob_from_memory(const.BUCKET_NAME, data, file_name)
        return file_name