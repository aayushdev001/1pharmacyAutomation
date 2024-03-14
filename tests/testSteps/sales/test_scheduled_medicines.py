import time

import pytest

from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.settings_sales_page import SettingsSalesPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestScheduledMedicines(BaseClass):
    def test_scheduled_medicines(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # settings
        driver.get(config['settings_sales_url'])
        settings_sales_page = SettingsSalesPage(driver)
        if settings_sales_page.is_schedule_drug_warning_disabled():
            settings_sales_page.toggle_schedule_drug_warning()
            settings_sales_page.save_settings()

        # billing
        driver.get(config['billing_url_alpha'])
        billing_page = BillingPage(driver)
        billing_page.select_first_product(config['scheduled_product_search_keyword'], config['scheduled_product_name'])
        billing_page.enter_quantity(config['item_quantity'])
        if billing_page.is_loose():
            billing_page.toggle_strip_loose()
        billing_page.read_default_batch()
        available_strips = billing_page.get_strip_quantity()
        billing_page.click_submit()
        assert billing_page.is_schedule_medicine_alert() == True
        time.sleep(4)

        # Inventory page
        driver.get(config['inventory_url_alpha'])
        inventory_page = InventoryPage(driver)
        inventory_page.search_medicine(config['scheduled_product_name'])
        inventory_page.click_medicine_link(config['scheduled_product_name'])
        time.sleep(3)

        # medicine inventory
        medicine_inventory_page = MedicineInventoryPage(driver)
        medicine_inventory_page.click_batches()
        remaining_stock = medicine_inventory_page.get_remaining_stock_strip(billing_page.get_default_batch())
        log.info(f"Original stock = {available_strips}")
        log.info(f"Remaining stock = {remaining_stock}")
        assert remaining_stock == available_strips
