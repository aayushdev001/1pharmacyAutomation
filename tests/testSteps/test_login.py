import time
import logging

import pytest

from tests.pages.login_page import LoginPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass


@pytest.mark.usefixtures("driver", "config")
class TestLogin(BaseClass):
    def test_login(self, driver, config):
        # report logging
        log = self.get_logger()

        # login page
        driver.get(config['1pharmacy_login_url'])
        login_page = LoginPage(driver, config['wait'])
        login_page.enter_phone_number(config['phone_number'])
        login_page.click_otp_button()

        # otp page
        otp_page = OtpPage(driver, config['wait'])
        otp_page.enter_otp(config['first_digit'], config['second_digit'], config['third_digit'], config['fourth_digit'])
        otp_page.click_login()
        time.sleep(4)
        log.info(f"Home page url -> {driver.current_url}")
        assert "https://alpha.1pharmacy.io/bill-entry/draft/1" in driver.current_url

