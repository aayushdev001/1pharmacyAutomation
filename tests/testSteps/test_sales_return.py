import time
import logging

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.pages.sales_return_page import SalesReturnPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


@pytest.mark.usefixtures("driver", "config")
class TestSalesReturn(BaseClass):
    def test_sales_return(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.select_product(config['search_keyword'], config['product_name'])
        time.sleep(4)
        if billing_page.is_loose():
            billing_page.toggle_strip_loose()
        billing_page.enter_quantity(config['item_quantity'])
        log.info(f"Sales quantity = {config['item_quantity']}")
        billing_page.read_default_batch()
        available_strips = billing_page.get_strip_quantity()
        log.info(f"Initial Stock = {available_strips}")
        time.sleep(4)
        total_amount = billing_page.get_item_total()
        billing_discount = billing_page.get_discount()
        billing_page.click_submit()
        time.sleep(7)
        billing_page.click_done()

        # bill history
        driver.get(config['bill_history_url'])
        bill_history_page = BillHistoryPage(driver)
        bill_history_page.click_latest_bill()
        bill_history_page.click_return()

        # sales return
        sales_return_page = SalesReturnPage(driver)
        sales_return_page.enter_return_quantity(config['item_return_quantity'])
        log.info(f"Return quantity = {config['item_return_quantity']}")
        return_discount = float(sales_return_page.get_discount())
        # print(f"Billing discount = {billing_discount}")
        # print(f"Return discount = {return_discount}")
        assert return_discount == billing_discount
        actual_total = sales_return_page.get_item_total()
        expected_total = config['item_return_quantity'] * sales_return_page.get_unit_mrp() * (1 - return_discount/100)
        assert actual_total == expected_total
        assert round(expected_total) == sales_return_page.get_net_amount()
        sales_return_page.click_submit()
        time.sleep(5)

        # checking inventory
        driver.get(config['bill_history_url'])
        bill_history_page = BillHistoryPage(driver)
        bill_history_page.click_latest_bill()
        bill_history_page.click_medicine_link(config['product_name'])
        medicine_inventory_page = MedicineInventoryPage(driver)
        medicine_inventory_page.click_batches()
        time.sleep(3)
        final_quantity = medicine_inventory_page.get_remaining_stock_strip(billing_page.get_default_batch())
        # print(f"Initial Stock = {available_strips}")
        # print(f"Sales quantity = {config['item_quantity']}")
        # print(f"Return quantity = {config['item_return_quantity']}")
        # print(f"Final Stock (after sales and return) = {final_quantity}")
        log.info(f"Final Stock (after sales and return) = {final_quantity}")
        assert final_quantity == available_strips - config['item_quantity'] + config['item_return_quantity']




