import time

from tests.pages.login_page import LoginPage
from tests.pages.otp_page import OtpPage


class LoginUtil:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def login(self):
        # login page
        self.driver.get(self.config['1pharmacy_login_url'])
        login_page = LoginPage(self.driver, self.config['wait'])
        login_page.enter_phone_number(self.config['phone_number'])
        login_page.click_otp_button()

        # otp page
        otp_page = OtpPage(self.driver, self.config['wait'])
        otp_page.enter_otp(self.config['first_digit'], self.config['second_digit'], self.config['third_digit'],
                           self.config['fourth_digit'])
        otp_page.click_login()
        time.sleep(4)
