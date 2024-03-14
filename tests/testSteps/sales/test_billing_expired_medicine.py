import time

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass
from tests.utils.current_month_and_date import CurrentMonthAndYear
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestBillingExpiredMedicine(BaseClass):
    def test_billing_expired_medicine(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_product(config['search_keyword'], config['product_name'])
        time.sleep(4)
        billing_page.enter_quantity(config['item_quantity'])
        log.info(f"Sold quantity = {config['item_quantity']}")
        current_month_and_year = CurrentMonthAndYear()
        billing_page.enter_expiry(current_month_and_year.current_month_and_year())
        time.sleep(4)