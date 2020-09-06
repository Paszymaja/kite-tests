import json
import os
import random
import time

import pytest
import requests

from scripts import drivers_setup


def valid_logins():
    """Load logins from json file and return it"""
    login_data = json.load(open('data/login_data.json', 'r', encoding="utf8"))
    return (random.choice(login_data['name']),
            random.choice(login_data['email']),
            random.choice(login_data['password']))


# needed for pytest fixtures
driver_init = drivers_setup.driver_init


@pytest.mark.usefixtures('driver_init')
class TestLogin:
    page_url = os.getenv('PAGE_URL')
    valid_login = valid_logins()

    def test_pages(self):
        assert requests.get(f'{self.page_url}/login').status_code == 200
        assert requests.get(f'{self.page_url}/login/form').status_code == 200
        assert requests.get(f'{self.page_url}/register').status_code == 200

    def test_move_to_register(self):
        self.driver.get(f'{self.page_url}/login')

        self.driver.find_element_by_xpath(r'//*[@title="Stwórz konto"]').click()
        assert f'{self.page_url}/register' in self.driver.current_url

    def test_move_to_login(self):
        self.driver.get(f'{self.page_url}/login')

        self.driver.find_element_by_xpath(r'//*[@title="Zaloguj się teraz"]').click()
        assert f'{self.page_url}/login/form' in self.driver.current_url

    def test_move_arrow_register(self):
        self.driver.get(f'{self.page_url}/register')
        link = self.driver.find_element_by_xpath('//a[@href="/login"]')
        link.click()
        assert f'{self.page_url}/login' in self.driver.current_url

    def test_move_arrow_login(self):
        self.driver.get(f'{self.page_url}/login/form')
        link = self.driver.find_element_by_xpath('//a[@href="/login"]')
        link.click()
        assert f'{self.page_url}/login' in self.driver.current_url

    def test_register(self):
        self.driver.get(f'{self.page_url}/register')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="Nazwa użytkownika"]')
        email = self.driver.find_element_by_xpath(r'//input[@placeholder="adres@mail.com"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="przynajmniej 8 znaków"]')
        check_box = self.driver.find_element_by_xpath(r'//input[@type="checkbox"]')
        register_button = self.driver.find_element_by_xpath(r'//*[@title="Stwórz konto"]')
        name.send_keys(self.valid_login[0])
        email.send_keys(self.valid_login[1])
        password.send_keys(self.valid_login[2])
        check_box.click()
        register_button.click()
        time.sleep(3)

        assert f'{self.page_url}/login' in self.driver.current_url

    def test_login_username(self):
        self.driver.execute_script('window.localStorage.clear();')  # clear login token
        self.driver.get(f'{self.page_url}/login/form')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="e-mail/Nazwa użytkownika"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="hasło"]')
        login_button = self.driver.find_element_by_xpath(r'//*[@title="Zaloguj"]')

        name.send_keys(self.valid_login[0])
        password.send_keys(self.valid_login[2])
        login_button.click()
        self.driver.implicitly_wait(5)

        assert self.driver.find_element_by_xpath(r'//*[@id="root"]/nav')  # find navbar

    def test_login_email(self):
        self.driver.execute_script('window.localStorage.clear();')  # clear login token
        self.driver.get(f'{self.page_url}/login/form')

        name = self.driver.find_element_by_xpath(r'//input[@placeholder="e-mail/Nazwa użytkownika"]')
        password = self.driver.find_element_by_xpath(r'//input[@placeholder="hasło"]')
        login_button = self.driver.find_element_by_xpath(r'//*[@title="Zaloguj"]')

        name.send_keys(self.valid_login[1])
        password.send_keys(self.valid_login[2])
        login_button.click()
        self.driver.implicitly_wait(5)

        assert self.driver.find_element_by_xpath(r'//*[@id="root"]/nav')  # find navbar
