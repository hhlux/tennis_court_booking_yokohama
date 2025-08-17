import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait



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
            options.add_experimental_option('prefs', prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--disable-application-cache')
            options.add_argument('window-size=1920,1080')
            if platform.system() != 'Darwin':  # For Cloud Run
                options.binary_location = '/usr/bin/google-chrome'
                options.add_argument('--headless=new')
            # options.add_experimental_option("prefs", {"download.default_directory": str(const.DOWNLOAD_FOLDER.absolute())})
            # BasePage.driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
            BasePage.driver = webdriver.Chrome(options=options)
            BasePage.driver.maximize_window()
            # BasePage.driver.implicitly_wait(10)
            BasePage.wait = WebDriverWait(BasePage.driver, 10)
            BasePage.wait_long = WebDriverWait(BasePage.driver, 60)
            BasePage.wait_super_long = WebDriverWait(BasePage.driver, 600)

