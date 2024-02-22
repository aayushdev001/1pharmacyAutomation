import time

from tests.pages.login_page import LoginPage
from tests.pages.medicine_inventory_page import MedicineInventoryPage
from tests.pages.otp_page import OtpPage
from tests.pages.purchase_history_page import PurchaseHistoryPage
from tests.pages.purchase_page import PurchasePage
from tests.testSteps.base_class import BaseClass


class TestPurchase(BaseClass):
    def test_purchase(self, driver, config):
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
        time.sleep(5)

        # purchase
        driver.get(config['purchase_url_alpha'])
        purchase_page = PurchasePage(driver)
        time.sleep(2)
        purchase_page.select_product(config['search_keyword'], config['product_name'])
        purchase_page.enter_quantity(config['item_purchase_quantity'])
        log.info(f"Quantity purchased = {config['item_purchase_quantity']}")
        purchase_page.select_batch()
        purchase_page.enter_expiry_date(config['purchase_item_expiry_date'])
        purchase_page.enter_mrp(config['purchase_mrp'])
        purchase_page.enter_purchase_rate(config['purchase_ptr'])
        purchase_page.enter_discount(config['purchase_discount'])
        purchase_page.enter_gst(str(config['purchase_gst']))
        purchase_page.enter_invoice_number("9876qwer")
        purchase_page.select_supplier_name()
        expected_total = ((config['item_purchase_quantity'] * config['purchase_ptr']) * (
                    1 - config['purchase_discount'] / 100)) * (1 + config['purchase_gst'] / 100)
        assert expected_total == purchase_page.get_item_total()
        # time.sleep(5)
        purchase_page.click_submit()
        time.sleep(4)

        # purchase history
        driver.get(config["purchase_history_url_alpha"])
        purchase_history = PurchaseHistoryPage(driver)
        purchase_history.click_latest_bill()
        purchase_history.click_medicine_link(config['product_name'])

        # medicine inventory
        medicine_inventory = MedicineInventoryPage(driver)
        medicine_inventory.click_history_button()
        # print(medicine_inventory.get_latest_purchase_quantity())
        log.info(f"Latest purchase input in inventory = {medicine_inventory.get_latest_purchase_quantity()}")
        assert medicine_inventory.get_latest_purchase_quantity() == config['item_purchase_quantity']


