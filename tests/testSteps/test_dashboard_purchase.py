import time

import pytest

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.otp_page import OtpPage
from tests.pages.purchase_page import PurchasePage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


@pytest.mark.usefixtures("driver", "config")
class TestDashboardPurchase(BaseClass):
    def test_dashboard_purchase(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()
        otp_page = OtpPage(driver, config['wait'])
        otp_page.navigate_dashboard()
        time.sleep(2)

        # storing initial sales and purchase amount
        dashboard_page = DashboardPage(driver)
        initial_sales_amount = dashboard_page.get_total_sales_amount()
        # print(f"Initial sales amount {dashboard_page.get_total_sales_amount()}")
        initial_purchase_amount = dashboard_page.get_total_purchase_amount()
        log.info(f"Initial purchase amount on dashboard = {initial_purchase_amount}")
        # print(f"Initial purchase amount {dashboard_page.get_total_purchase_amount()}")

        # purchase
        driver.get(config['purchase_url_alpha'])
        purchase_page = PurchasePage(driver)
        time.sleep(2)
        purchase_page.select_product(config['search_keyword'], config['product_name'])
        purchase_page.enter_quantity(config['item_purchase_quantity'])
        purchase_page.select_batch()
        purchase_page.enter_expiry_date(config['purchase_item_expiry_date'])
        purchase_page.enter_mrp(config['purchase_mrp'])
        purchase_page.enter_purchase_rate(config['purchase_ptr'])
        purchase_page.enter_discount(config['purchase_discount'])
        purchase_page.enter_gst(str(config['purchase_gst']))
        purchase_page.enter_invoice_number("9876qwer")
        purchase_page.select_supplier_name()
        total_amount = purchase_page.get_item_total()
        log.info(f"Purchase amount = {total_amount}")
        # time.sleep(5)
        purchase_page.click_submit()
        time.sleep(6)

        # asserting new sales and purchase amount
        otp_page.navigate_dashboard()
        time.sleep(2)
        dashboard_page2 = DashboardPage(driver)
        final_sales_amount = dashboard_page2.get_total_sales_amount()
        # print(f'Final sales amount = {dashboard_page2.get_total_sales_amount()}')
        final_purchase_amount = dashboard_page2.get_total_purchase_amount()
        # print(f"Final purchase amount = {dashboard_page2.get_total_purchase_amount()}")
        log.info(f"Final purchase amount on dashboard = {final_purchase_amount}")
        assert float("{:.2f}".format(initial_purchase_amount + total_amount)) == final_purchase_amount
