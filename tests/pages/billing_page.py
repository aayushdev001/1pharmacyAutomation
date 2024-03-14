import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
import pyautogui
from selenium import webdriver


class BillingPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.product_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="1p-basic-text"]')))
        self.batch_input = None
        self.default_batch_name = ""
        # self.discount_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1p-basic-text"]')))
        self.discount_input = None
        self.discount = 0
        # self.unit_mrp = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":rfc:"]/td[10]/div')))
        self.unit_mrp_input = None
        self.unit_mrp = 0
        self.quantity_input = None
        self.quantity = 0
        self.stock = None
        self.strip_stock = 0
        # self.item_total = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":rfc:"]/td[13]')))
        self.item_total = None
        self.gst = None
        self.submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             "//body/div[@id='root']/section[1]/main[1]/section[1]/div[3]/section[1]/div[2]/div[2]/button[2]")))
        self.done_button = None
        self.strip_loose_toggle_wrapper = None
        self.strip_loose_toggle = None
        self.bill_submit_alert = None
        self.expiry_input = None
        # self.delivery_charge_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1p-basic-text"]')))
        # self.total_discount_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1p-basic-text"]')))
        # self.bill_total = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/section/main/section/div[3]/section/div[1]/div[1]/h6[2]')))
        # self.total_discount = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/main/section/div[3]/section/div[1]/div[2]/h6[2]')))
        # self.total_gst = wait.until(EC.presence_of_element_located((By.XPATH, '//body/div[@id="root"]/section[1]/main[1]/section[1]/div[3]/section[1]/div[1]/div[3]/h6[2]')))
        # self.net_amount = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/main/section/div[3]/section/div[1]/div[5]/h6[2]')))

    def enter_product_name(self, keyword):
        self.product_input.send_keys(keyword)

    def select_product(self, keyword, product_name):
        self.enter_product_name(keyword)
        product = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{product_name}')]")))
        product.click()

    def enter_batch(self, batch):
        self.batch_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                       "/html[1]/body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[4]/div[1]/div[1]/div[1]/input[1]")))
        self.batch_input.click()
        self.batch_input.send_keys(Keys.BACKSPACE * len(self.batch_input.get_attribute('value')))
        time.sleep(1)
        self.batch_input.send_keys(batch)

    def get_all_batches(self):
        self.batch_input.click()

    def read_default_batch(self):
        self.batch_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                           '/html[1]/body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[4]/div[1]/div[1]/div[1]/input[1]')))
        self.default_batch_name = self.batch_input.get_attribute('value')

    def get_default_batch(self):
        return self.default_batch_name

    def enter_quantity(self, quantity):
        self.quantity = quantity
        self.quantity_input = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/section/main/section/div[2]/div/table/tbody[1]/tr[1]/td[6]/div/div/input')))
        self.quantity_input.send_keys(quantity)
        time.sleep(8)

    def get_strip_quantity(self):
        self.batch_input.click()
        self.stock = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f"//div[text()='{self.default_batch_name}']/following::div[4]")))
        match = re.search(r'^(\d+)', self.stock.text)
        if match:
            self.quantity = int(match.group(1))
            return int(match.group(1))
        else:
            return None

    def get_loose_quantity(self):
        self.batch_input.click()
        self.stock = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f"//div[text()='{self.default_batch_name}']/following::div[4]")))
        pattern = r'\((\d+)\)'
        match = re.search(pattern, self.stock.text)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_discount(self):
        self.discount_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html[1]/body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[7]/div[1]/div[1]/input[1]")))
        self.discount = self.discount_input.get_attribute('value')
        return float(self.discount)

    def get_unit_mrp(self):
        self.unit_mrp_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html[1]/body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[8]/div[1]/div[1]/input[1]")))
        self.unit_mrp = self.unit_mrp_input.get_attribute('value')
        return float(self.unit_mrp)

    def get_gst(self):
        self.gst = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":r6:"]/td[12]')))
        return float(self.gst.text)

    def get_item_total(self):
        self.item_total = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                          '//body[1]/div[1]/section[1]/main[1]/section[1]/div[3]/section[1]/div[1]/div[5]/h6[2]')))
        # print(self.item_total.text)
        amount = self.item_total.text.replace('₹', '').replace(',', '')
        return float(amount)
        # match = re.search(r'₹ (\d+(\.\d*)?)', self.item_total.text)
        # if match:
        #     return float(match.group(1))
        # else:
        #     return None

    def click_submit(self):
        self.submit_button.click()

    def click_done(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def is_loose(self):
        self.strip_loose_toggle_wrapper = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                          "//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[10]/div[1]/div[1]/span[1]/span[1]")))
        return "Mui-checked" in self.strip_loose_toggle_wrapper.get_attribute('class')

    def toggle_strip_loose(self):
        self.strip_loose_toggle = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='looseEnabled']")))
        self.strip_loose_toggle.click()

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

    def enter_expiry(self, expiry):
        self.expiry_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/div[1]/input[1]")))
        self.expiry_input.send_keys(expiry)
