import pytest
import requests
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
    driver = driver.load_driver(headless=False)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.usefixtures('driver_init')
class TestLogin:
    def test_pages(self):
        assert requests.get('http://localhost:3000/login').status_code == 200
        assert requests.get('http://localhost:3000/login/form').status_code == 200
        assert requests.get('http://localhost:3000/register').status_code == 200

    def test_move_to_register(self):
        self.driver.get('http://localhost:3000/login')

        self.driver.find_element_by_xpath(r'//*[@title="Stwórz konto"]').click()
        assert 'http://localhost:3000/register' in self.driver.current_url

    def test_move_to_login(self):
        self.driver.get('http://localhost:3000/login')

        self.driver.find_element_by_xpath(r'//*[@title="Zaloguj się teraz"]').click()
        assert 'http://localhost:3000/login/form' in self.driver.current_url

    def test_register(self):
        self.driver.get('http://localhost:3000/register')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="Nazwa użytkownika"]')
        email = self.driver.find_element_by_xpath(r'//input[@placeholder="adres@mail.com"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="przynajmniej 8 znaków"]')
        check_box = self.driver.find_element_by_xpath(r'//input[@type="checkbox"]')
        register_button = self.driver.find_element_by_xpath(r'//*[@title="Stwórz konto"]')
        name.send_keys('test')
        email.send_keys('test@test.pl')
        password.send_keys('123456789')
        check_box.click()
        register_button.click()

    def test_login(self):
        self.driver.get('http://localhost:3000/login/form')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="email/username"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="hasło"]')
        login_button = self.driver.find_element_by_xpath(r'//*[@title="Zaloguj"]')

        name.send_keys('test')
        password.send_keys('12344567889')
        login_button.click()


