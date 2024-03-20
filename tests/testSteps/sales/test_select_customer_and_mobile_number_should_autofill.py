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
class TestSelectCustomerAndMobileNumberShouldAutofill(BaseClass):
    def test_select_customer_and_mobile_number_should_autofill(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_customer_name(config['customer_name'])
        time.sleep(2)
        assert billing_page.read_customer_number() == config['customer_mobile_number']
