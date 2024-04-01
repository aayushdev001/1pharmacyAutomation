import time

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestDeleteBillEntry(BaseClass):
    def test_delete_bill_entry(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_first_product(config['search_keyword'], config['product_name'])
        time.sleep(4)
        billing_page.enter_first_quantity(config['item_quantity'])
        log.info(f"Sold quantity = {config['item_quantity']}")

        if billing_page.is_first_medicine_loose():
            billing_page.toggle_first_medicine_strip_loose()

        billing_page.read_first_default_batch()
        available_strips = billing_page.get_first_strip_quantity()
        time.sleep(4)
        expected_total = config['item_quantity'] * billing_page.get_first_unit_mrp() * (
                1 - (billing_page.get_first_discount() / 100))
        actual_total = billing_page.get_first_item_total()
        log.info(f"Expected Total = {expected_total}")
        log.info(f"Actual Total = {actual_total}")
        assert expected_total == actual_total

        # delete bill
        billing_page.delete_bill_entry(1)
        billing_page.click_submit()
        assert billing_page.is_missing_field_alert() == True
