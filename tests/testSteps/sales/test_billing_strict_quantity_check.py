import time

import pytest

from tests.pages.billing_page import BillingPage
from tests.pages.settings_sales_page import SettingsSalesPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestStrictQuantityCheck(BaseClass):
    def test_strict_quantity_check(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # settings
        driver.get(config['settings_sales_url'])
        settings_sales_page = SettingsSalesPage(driver)
        if settings_sales_page.is_strict_quantity_check_on() is False:
            settings_sales_page.toggle_stric_quantity()
        settings_sales_page.save_settings()

        # billing
        driver.get(config['billing_url_alpha'])
        billing_page = BillingPage(driver)
        billing_page.select_product(config['search_keyword'], config['product_name'])
        time.sleep(4)

        if billing_page.is_loose():
            billing_page.toggle_strip_loose()

        billing_page.read_default_batch()
        available_strips = billing_page.get_strip_quantity()

        billing_page.enter_quantity(f"{available_strips + 1}")
        billing_page.click_submit()
        assert billing_page.is_strict_quantity_alert() == True
