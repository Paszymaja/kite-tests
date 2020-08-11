import sys

import pytest
from selenium import webdriver


class Chrome:
    """Class with single function returning windows chromedriver"""

    @staticmethod
    def load_driver(headless=False):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_driver_path = 'drivers/chrome/chromedriver.exe'
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
        return driver


class DockerChrome:
    """Class with single function returning chromedriver for docker image"""

    @staticmethod
    def load_driver(headless=True):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(1)
        return driver


@pytest.fixture(scope='class')
def driver_init(request):
    """Generator witch yields driver and automatically close it"""
    if sys.platform == 'linux' or sys.platform == 'linux2':
        driver = DockerChrome()
    else:
        driver = Chrome()

    driver = driver.load_driver()
    request.cls.driver = driver
    yield
    driver.close()
