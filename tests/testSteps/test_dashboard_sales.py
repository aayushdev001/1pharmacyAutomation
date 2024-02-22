import time

import pytest

from tests.pages.billing_page import BillingPage
from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.otp_page import OtpPage
import pyautogui

from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


@pytest.mark.usefixtures("driver", "config")
class TestDashboardSales(BaseClass):
    def test_dashboard_sales(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()
        otp_page = OtpPage(driver, config['wait'])
        otp_page = OtpPage(driver, config['wait'])
        otp_page.navigate_dashboard()
        time.sleep(4)
        # print(driver.current_url)

        # storing initial sales and purchase amount
        dashboard_page = DashboardPage(driver)
        initial_sales_amount = dashboard_page.get_total_sales_amount()
        # print(f"Initial sales amount {dashboard_page.get_total_sales_amount()}")
        initial_purchase_amount = dashboard_page.get_total_purchase_amount()
        log.info(f"Initial sales amount = {initial_sales_amount}")
        # print(f"Initial purchase amount {dashboard_page.get_total_purchase_amount()}")
        # time.sleep(7)

        # billing
        driver.get(config['billing_url_alpha'])
        billing_page = BillingPage(driver)
        billing_page.select_product(config['search_keyword'], config['product_name'])
        time.sleep(4)
        billing_page.enter_quantity(config['item_quantity'])
        time.sleep(4)
        total_amount = billing_page.get_item_total()
        log.info(f"Sales amount = {total_amount}")
        billing_page.click_submit()
        time.sleep(7)
        billing_page.click_done()

        # asserting new sales and purchase amount
        otp_page.navigate_dashboard()
        time.sleep(3)
        dashboard_page2 = DashboardPage(driver)
        final_sales_amount = dashboard_page2.get_total_sales_amount()
        # print(f'Final sales amount = {dashboard_page2.get_total_sales_amount()}')
        final_purchase_amount = dashboard_page2.get_total_purchase_amount()
        log.info(f"Final sales amount = {final_sales_amount}")
        # print(f"Final purchase amount = {dashboard_page2.get_total_purchase_amount()}")
        assert float("{:.2f}".format(initial_sales_amount + total_amount)) == final_sales_amount




