import time

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


@pytest.mark.usefixtures("driver", "config")
class TestBilling(BaseClass):
    def test_billing(self, driver, config):
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

        if billing_page.is_loose():
            # print(f"Strip = {billing_page.is_loose()}")
            billing_page.toggle_strip_loose()

        billing_page.read_default_batch()
        available_strips = billing_page.get_strip()
        time.sleep(4)
        expected_total = config['item_quantity'] * billing_page.get_unit_mrp() * (
                    1 - (billing_page.get_discount() / 100))
        # print(f"Expected Total = {expected_total}")
        # print(f"Actual Total = {billing_page.get_item_total()}")
        actual_total = billing_page.get_item_total()
        log.info(f"Expected Total = {expected_total}")
        log.info(f"Actual Total = {actual_total}")
        assert expected_total == actual_total
        billing_page.click_submit()
        time.sleep(5)

        # bill history
        driver.get(config['bill_history_url'])
        bill_history_page = BillHistoryPage(driver)
        bill_history_page.click_latest_bill()
        bill_history_page.click_medicine_link(config['product_name'])

        # medicine inventory
        medicine_inventory_page = MedicineInventoryPage(driver)
        medicine_inventory_page.click_batches()
        remaining_stock = medicine_inventory_page.get_remaining_stock(billing_page.get_default_batch())
        log.info(f"Original stock = {available_strips}")
        log.info(f"Remaining stock = {remaining_stock}")
        assert remaining_stock == available_strips - config['item_quantity']



