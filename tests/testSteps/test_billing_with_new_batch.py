import time

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


class TestBillingWithNewBatch(BaseClass):
    def test_billing(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_first_product(config['search_keyword'], config['product_name'])
        time.sleep(5)
        new_batch_name = config['custom_batch_name']
        billing_page.enter_first_medicine_batch(new_batch_name)
        log.info(f"New batch name = {new_batch_name}")
        billing_page.enter_first_quantity(config['item_quantity'])
        log.info(f"Sold quantity = {config['item_quantity']}")

        if billing_page.is_first_medicine_loose():
            # print(f"Strip = {billing_page.is_loose()}")
            billing_page.toggle_first_medicine_strip_loose()

        time.sleep(4)
        expected_total = config['item_quantity'] * billing_page.get_first_unit_mrp() * (
                    1 - (billing_page.get_first_discount() / 100))
        # print(f"Expected Total = {expected_total}")
        # print(f"Actual Total = {billing_page.get_item_total()}")
        actual_total = billing_page.get_first_item_total()
        log.info(f"Expected Total = {expected_total}")
        log.info(f"Actual Total = {actual_total}")
        assert expected_total == actual_total
        billing_page.click_submit()
        time.sleep(3)

        # bill history
        driver.get(config['bill_history_url'])
        bill_history_page = BillHistoryPage(driver)
        bill_history_page.click_latest_bill()
        bill_history_page.click_medicine_link(config['product_name'])

        # inventory
        medicine_inventory_page = MedicineInventoryPage(driver)
        medicine_inventory_page.click_batches()
        time.sleep(5)
        medicine_inventory_page.show_zero_and_negative_stock()
        remaining_stock = medicine_inventory_page.get_remaining_stock_strip(new_batch_name)
        log.info(f"Remaining stock = {remaining_stock}")
        assert -1 * config['item_quantity'] == remaining_stock

