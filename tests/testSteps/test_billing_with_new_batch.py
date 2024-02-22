import time

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.testSteps.base_class import BaseClass


class TestBillingWithNewBatch(BaseClass):
    def test_billing(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        driver.get(config['1pharmacy_login_url'])
        login_page = LoginPage(driver, config['wait'])
        login_page.enter_phone_number(config['phone_number'])
        login_page.click_otp_button()
        otp_page = OtpPage(driver, config['wait'])
        otp_page.enter_otp(config['first_digit'], config['second_digit'], config['third_digit'], config['fourth_digit'])
        otp_page.click_login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_product(config['search_keyword'], config['product_name'])
        time.sleep(5)
        new_batch_name = config['custom_batch_name']
        billing_page.enter_batch(new_batch_name)
        log.info(f"New batch name = {new_batch_name}")
        billing_page.enter_quantity(config['item_quantity'])
        log.info(f"Sold quantity = {config['item_quantity']}")

        if billing_page.is_loose():
            # print(f"Strip = {billing_page.is_loose()}")
            billing_page.toggle_strip_loose()

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
        remaining_stock = medicine_inventory_page.get_remaining_stock(new_batch_name)
        log.info(f"Remaining stock = {remaining_stock}")
        assert -1 * config['item_quantity'] == remaining_stock

