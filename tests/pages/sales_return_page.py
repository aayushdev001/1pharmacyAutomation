import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium import webdriver


class SalesReturnPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.quantity_input = None
        self.discount_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//tbody/tr[1]/td[8]/div[1]/div[1]/input[1]')))
        self.item_total = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/main/section/div[1]/div/table/tbody/tr/td[12]')))
        self.net_amount = self.wait.until(EC.presence_of_element_located((By.XPATH, '//tbody/tr[1]/td[12]')))
        self.unit_mrp_input = None
        self.unit_mrp = 0
        self.submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    def enter_return_quantity(self, quantity):
        self.quantity_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//tbody/tr[1]/td[4]/div[1]/div[1]/input[1]')))
        self.quantity_input.send_keys(quantity)

    def get_discount(self):
        return self.discount_input.get_attribute('value')

    def get_unit_mrp(self):
        self.unit_mrp_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//tbody/tr[1]/td[7]/div[1]/div[1]/input[1]')))
        self.unit_mrp = self.unit_mrp_input.get_attribute('value')
        return float(self.unit_mrp)

    def get_item_total(self):
        # print(f"Item total = {self.item_total.text}")
        return self.clean_expression(self.item_total.text)

    def get_net_amount(self):
        # print(f"Net amount = {self.net_amount.text}")
        return self.clean_expression(self.net_amount.text)

    # ₹ 152.45 -> 152.45
    def clean_expression(self, exp):
        match = re.search(r'₹ (\d+(\.\d*)?)', exp)
        # print(f"Item total = {matches[0]}")
        if match:
            return float(match.group(1))
        else:
            return None

    def click_submit(self):
        self.submit_button.click()
