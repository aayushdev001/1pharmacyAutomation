import time

import pytest

from tests.pages.billing_page import BillingPage
from tests.pages.settings_sales_page import SettingsSalesPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestScheduledMedicines(BaseClass):
    def test_scheduled_medicines(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # settings
        driver.get(config['settings_sales_url'])
        settings_sales_page = SettingsSalesPage(driver)
        if settings_sales_page.is_schedule_drug_warning_disabled():
            settings_sales_page.toggle_schedule_drug_warning()
            settings_sales_page.save_settings()

        # billing
        driver.get(config['billing_url_alpha'])
        billing_page = BillingPage(driver)
        billing_page.select_first_product(config['scheduled_product_search_keyword'], config['scheduled_product_name'])
        billing_page.enter_quantity(config['item_quantity'])
        billing_page.click_submit()
        assert billing_page.is_schedule_medicine_alert() == True
        time.sleep(4)
