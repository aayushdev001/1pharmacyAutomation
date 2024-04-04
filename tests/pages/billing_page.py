import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class BillingPage:
    def __init__(self, driver):
        self.first_quantity_input = None
        self.second_quantity_input = None
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.first_product_input = None
        self.second_row = None
        self.second_product_input = None
        self.first_batch_input = None
        self.second_batch_input = None
        self.first_default_batch_name = ""
        self.second_default_batch_name = ""
        self.first_discount_input = None
        self.second_discount_input = None
        self.overall_discount_input = None
        self.discount = 0
        self.first_unit_mrp_input = None
        self.first_unit_mrp = 0
        self.second_unit_mrp_input = None
        self.quantity = 0
        self.stock = None
        self.strip_stock = 0
        self.first_item_total = None
        self.second_item_total = None
        self.gst = None
        self.submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             "//body/div[@id='root']/section[1]/main[1]/section[1]/div[3]/section[1]/div[2]/div[2]/button[2]")))
        self.done_button = None
        self.first_strip_loose_toggle_wrapper = None
        self.second_strip_loose_toggle_wrapper = None
        self.first_strip_loose_toggle = None
        self.second_strip_loose_toggle = None
        self.bill_submit_alert = None
        self.expiry_input = None
        self.customer_name_input = None
        self.customer_mobile_input = None
        self.customer_name = None
        self.customer_mobile = None
        self.payment_type_input = None
        self.card_payment_type = None
        self.delete_button = None
        self.reset_button = None
        self.net_total = None

    def enter_first_product_name(self, keyword):
        self.first_product_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="name"]')))
        self.first_product_input.send_keys(keyword)

    def select_first_product(self, keyword, product_name):
        self.enter_first_product_name(keyword)
        product = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{product_name}')]")))
        product.click()

    def enter_second_product(self, keyword):
        self.second_product_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="name"]')))
        self.second_product_input.send_keys(keyword)

    def select_second_product(self, keyword, product_name):
        self.second_row = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//td[text()="2"]')))
        self.second_row.click()
        self.enter_second_product(keyword)
        product = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{product_name}')]")))
        product.click()

    def enter_first_medicine_batch(self, batch):
        self.first_batch_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                             '//*[@name="batch"]')))
        self.first_batch_input.click()
        self.first_batch_input.send_keys(Keys.BACKSPACE * len(self.first_batch_input.get_attribute('value')))
        time.sleep(1)
        self.first_batch_input.send_keys(batch)

    def get_all_batches(self):
        self.first_batch_input.click()

    def read_first_default_batch(self):
        self.first_batch_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="batch"]')))
        self.first_default_batch_name = self.first_batch_input.get_attribute('value')

    def read_second_default_batch(self):
        self.second_batch_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="batch"]')))
        self.second_default_batch_name = self.second_batch_input.get_attribute('value')

    def get_first_default_batch(self):
        return self.first_default_batch_name

    def get_second_default_batch(self):
        return self.second_default_batch_name

    def enter_first_quantity(self, quantity):
        self.first_quantity_input = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@name='billQty']")))
        self.first_quantity_input.send_keys(quantity)

    def enter_second_quantity(self, quantity):
        self.second_quantity_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@name='billQty']")))
        self.second_quantity_input.send_keys(quantity)

    def get_first_strip_quantity(self):
        self.first_batch_input.click()
        self.stock = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f"//div[text()='{self.first_default_batch_name}']/following::div[4]")))
        match = re.search(r'^(\d+)', self.stock.text)
        if match:
            self.quantity = int(match.group(1))
            return int(match.group(1))
        else:
            return None

    def get_second_strip_quantity(self):
        self.second_batch_input.click()
        stock = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//div[text()='{self.second_default_batch_name}']/following::div[4]")))
        match = re.search(r'^(\d+)', stock.text)
        if match:
            self.quantity = int(match.group(1))
            return int(match.group(1))
        else:
            return None

    def get_first_loose_quantity(self):
        self.first_batch_input.click()
        self.stock = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f"//div[text()='{self.first_default_batch_name}']/following::div[4]")))
        pattern = r'\((\d+)\)'
        match = re.search(pattern, self.stock.text)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_second_loose_quantity(self):
        self.second_batch_input.click()
        stock = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//div[text()='{self.second_default_batch_name}']/following::div[4]")))
        pattern = r'\((\d+)\)'
        match = re.search(pattern, stock.text)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_first_discount(self):
        self.first_discount_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "(//*[@name='discount'])[1]")))
        self.discount = self.first_discount_input.get_attribute('value')
        return float(self.discount)

    def get_second_discount(self):
        self.second_discount_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                 "(//*[@name='discount'])[1]")))
        # self.second_discount_input.send_keys(15)
        discount = self.second_discount_input.get_attribute('value')
        return float(discount)

    def get_first_unit_mrp(self):
        self.first_unit_mrp_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "(//*[@name='price'])")))
        self.first_unit_mrp = self.first_unit_mrp_input.get_attribute('value')
        return float(self.first_unit_mrp)

    def get_second_unit_mrp(self):
        self.second_unit_mrp_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                 "(//*[@name='price'])")))
        second_unit_mrp = self.second_unit_mrp_input.get_attribute('value')
        return float(second_unit_mrp)

    def get_gst(self):
        self.gst = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":r6:"]/td[12]')))
        return float(self.gst.text)

    def get_first_item_total(self):
        self.first_item_total = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'netItemAmount')]")))
        amount = self.first_item_total.text.replace('₹', '').replace(',', '')
        return float(amount)

    def get_second_item_total(self):
        self.second_item_total = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'netItemAmount')]")))
        amount = self.second_item_total.text.replace('₹', '').replace(',', '')
        return float(amount)

    def enter_overall_discount(self, disc):
        self.overall_discount_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                  "(//*[@name='discountPercent'])")))
        self.overall_discount_input.click()
        self.overall_discount_input.send_keys(disc)

    def click_submit(self):
        self.submit_button.click()

    def click_done(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def is_first_medicine_loose(self):
        self.first_strip_loose_toggle_wrapper = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                "//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[10]/div[1]/div[1]/span[1]/span[1]")))
        return "Mui-checked" in self.first_strip_loose_toggle_wrapper.get_attribute('class')

    def is_second_medicine_loose(self):
        self.second_strip_loose_toggle_wrapper = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                 '//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[2]/td[10]/div[1]/div[1]/span[1]/span[1]')))
        return "Mui-checked" in self.second_strip_loose_toggle_wrapper.get_attribute('class')

    def toggle_first_medicine_strip_loose(self):
        self.first_strip_loose_toggle = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "(//*[@name='looseEnabled'])[1]")))
        self.first_strip_loose_toggle.click()

    def toggle_second_medicine_strip_loose(self):
        self.second_strip_loose_toggle = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[@name='looseEnabled'])[2]")))
        self.second_strip_loose_toggle.click()
        # self.second_strip_loose_toggle_wrapper.click()

    def is_strict_quantity_alert(self):
        try:
            self.bill_submit_alert = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/div[2]')))
            if "is greater than stock quantity" in self.bill_submit_alert.text:
                return True
            else:
                return False
        except TimeoutException:
            return False

    def is_schedule_medicine_alert(self):
        try:
            self.bill_submit_alert = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/div[2]')))
            if "Please fill all the required fields" in self.bill_submit_alert.text:
                return True
            else:
                return False
        except TimeoutException:
            return False

    def is_missing_field_alert(self):
        try:
            self.bill_submit_alert = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/div[2]')))
            if "Please fill all the required fields" in self.bill_submit_alert.text:
                return True
            else:
                return False
        except TimeoutException:
            return False

    def is_reset_bill_alert(self):
        try:
            self.bill_submit_alert = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/div[2]')))
            if "Bill Draft reset successfully" in self.bill_submit_alert.text:
                return True
            else:
                return False
        except TimeoutException:
            return False

    def enter_first_medicine_expiry(self, expiry):
        self.expiry_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/div[1]/input[1]")))
        self.expiry_input.send_keys(expiry)

    def select_customer_name(self, name):
        self.customer_name_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                   '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/input[1]')))
        self.customer_name_input.click()
        self.customer_name = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//p[contains(text(),'{name}')]")))
        self.customer_name.click()

    def select_customer_mobile_number(self, number):
        self.customer_mobile_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                     '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/input[1]')))
        self.customer_name_input.click()
        self.customer_mobile = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//p[contains(text(),'{number}')]")))
        self.customer_mobile.click()

    def read_customer_number(self):
        self.customer_mobile_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                     '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/input[1]')))
        return self.customer_mobile_input.get_attribute('value')

    def read_customer_name(self):
        self.customer_name_input = self.customer_name_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                              '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/input[1]')))
        return self.customer_name_input.get_attribute('value')

    def read_payment_type(self):
        self.payment_type_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "(//*[@name='paymentMode'])")))
        return self.payment_type_input.text

    def select_card_payment_type(self):
        if self.payment_type_input is None:
            self.payment_type_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                      "(//*[@name='paymentMode'])")))
        self.payment_type_input.click()
        self.card_payment_type = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-value='Card']")))
        self.card_payment_type.click()

    def reset_bill(self):
        self.reset_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Reset')]")))
        self.reset_button.click()
        webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def delete_bill_entry(self, bill_number):
        self.delete_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"(//*[contains(@class, 'ri-delete-bin-line')])[{bill_number}]")))
        self.delete_button.click()

    def get_net_total(self):
        self.net_total = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/section[1]/div[1]/div[5]/h6[2]')))
        amount = self.net_total.text.replace('₹', '').replace(',', '')
        return float(amount)
