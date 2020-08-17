import pytest

from scripts import drivers_setup

# needed for pytest fixtures
driver_init = drivers_setup.driver_init


@pytest.mark.usefixtures('driver_init')
class TestWebpage:
    page_url = 'http://89.25.253.218:30082'

    def test_login_email(self):
        self.driver.get(f'{self.page_url}/login/form')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="e-mail/Nazwa użytkownika"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="hasło"]')
        login_button = self.driver.find_element_by_xpath(r'//*[@title="Zaloguj"]')

        name.send_keys('test@test.pl')
        password.send_keys('1234567890')
        login_button.click()
        self.driver.implicitly_wait(5)

        assert self.driver.find_element_by_xpath(r'//*[@id="root"]/nav')  # find navbar

    def test_navbar(self):
        self.driver.get(f'{self.page_url}/test')
        self.driver.implicitly_wait(5)
        aktualnosci = self.driver.find_element_by_xpath(r'//a[@href="/test"]')
        tutoriale = self.driver.find_element_by_xpath(r'//a[@href="/test3"]')
        wydarzenia = self.driver.find_element_by_xpath(r'//a[@href="/test2"]')

        tutoriale.click()
        self.driver.implicitly_wait(5)
        assert f'{self.page_url}/test3' in self.driver.current_url

        wydarzenia.click()
        self.driver.implicitly_wait(5)
        assert f'{self.page_url}/test2' in self.driver.current_url

        aktualnosci.click()
        self.driver.implicitly_wait(5)
        assert f'{self.page_url}/test' in self.driver.current_url
