import pytest
from selenium import webdriver


class Chrome:
    def load_driver(self, headless=False):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_driver_path = 'drivers/chrome/chromedriver.exe'
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
        return driver


class Firefox:
    def load_driver(self, headless=False):
        firefox_options = webdriver.FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        firefox_driver_path = 'drivers/firefox/geckodriver.exe'
        driver = webdriver.Firefox(options=firefox_options, executable_path=firefox_driver_path)
        return driver


@pytest.fixture(scope='class')
def driver_init(request):
    driver = Chrome()
    driver = driver.load_driver(headless=True)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.usefixtures('driver_init')
class TestLogin:
    def test_page(self):
        self.driver.get('https://lowcygier.pl/')
        assert 'https://lowcygier.pl/' in self.driver.current_url

    def test_valid_login(self):
        self.driver.get('https://www.google.pl/')

        elem = self.driver.find_element_by_name('q')
        elem.send_keys('pomocy')
        elem.submit()
        assert 1 == 1
