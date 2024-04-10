import time

import pytest

from tests.pages.add_item_details_page import AddItemDetailsPage
from tests.pages.add_item_modal_page import AddItemModalPage
from tests.pages.bill_history_page import BillHistoryPage
from tests.pages.billing_page import BillingPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestAddNewItemMissingInInventory(BaseClass):
    def test_add_new_item_missing_in_inventory(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.enter_first_product_name(config['new_product_name'])
        billing_page.add_new_item()

        add_item_modal_page = AddItemModalPage(driver)
        add_item_modal_page.click_add_item()
        time.sleep(5)

        add_item_details_page = AddItemDetailsPage(driver)
        add_item_details_page.enter_name("Test")
        add_item_details_page.enter_mrp("25")
        add_item_details_page.enter_unit("10")
        add_item_details_page.select_unit_type('Tablet')
        add_item_details_page.enter_batch(config['custom_batch_name'])
        add_item_details_page.enter_quantity("30")
        add_item_details_page.enter_expiry("05/25")
        add_item_details_page.enter_batch_mrp("25")
        time.sleep(5)
        add_item_details_page.click_save()
        time.sleep(7)
