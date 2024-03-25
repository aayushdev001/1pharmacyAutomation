import time

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestResetBill(BaseClass):
    def test_reset_bill(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_first_product(config['search_keyword'], config['product_name'])
        time.sleep(4)
        billing_page.reset_bill()
        time.sleep(2)
        assert billing_page.is_reset_bill_alert() == True
