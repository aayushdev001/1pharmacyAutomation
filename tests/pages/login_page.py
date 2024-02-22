import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.otp_page import OtpPage
from tests.testSteps.conftest import config, driver


class LoginPage:
    def __init__(self, driver, wait):
        self.wait = WebDriverWait(driver, wait)
        self.phone_number_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]')))
        self.get_otp_button = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[2]/section/div/div/div/div[2]/div/div/button')))

    def enter_phone_number(self, phone_number):
        self.phone_number_input.send_keys(phone_number)

    def click_otp_button(self):
        self.get_otp_button.click()

    # def login(self, config, driver):
    #     # driver.get(config['1pharmacy_login_url'])
    #     driver
    #     driver.get("1pharmacy_login_url")
    #     login_page = LoginPage(driver, config['wait'])
    #     login_page.enter_phone_number(config['phone_number'])
    #     login_page.click_otp_button()
    #     otp_page = OtpPage(driver, config['wait'])
    #     otp_page.enter_otp(config['first_digit'], config['second_digit'], config['third_digit'], config['fourth_digit'])
    #     otp_page.click_login()
