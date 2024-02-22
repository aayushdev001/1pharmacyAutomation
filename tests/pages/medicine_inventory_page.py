import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium import webdriver


class MedicineInventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.remaining_stock = None
        self.hide_zero_and_negative_stock_checkbox = None
        self.batches_button = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                              "//body/div[@id='root']/section[1]/main[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/button[1]")))
        self.medicine_link = None
        self.history_button = None
        self.latest_purchase_quantity = None

    def click_batches(self):
        self.batches_button.click()

    def show_zero_and_negative_stock(self):
        self.hide_zero_and_negative_stock_checkbox = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/main/div[3]/div/div[2]/div[2]/label[1]/span[1]')))
        self.hide_zero_and_negative_stock_checkbox.click()

    def get_remaining_stock(self, batch_name):
        self.remaining_stock = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(., '{batch_name}')]]//td[3]")))
        # print(self.remaining_stock.text)
        match = re.match(r'^(-?\d+)', self.remaining_stock.text)
        if match:
            extracted_integer = int(match.group(0))
            return extracted_integer  # Output: -5
        else:
            return None

    def click_history_button(self):
        self.history_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/button[6]')))
        self.history_button.click()

    def get_latest_purchase_quantity(self):
        self.latest_purchase_quantity = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/div[3]/div[1]/div[2]/div[3]/div[2]/table[1]/tbody[1]/tr[1]/td[6]')))
        return int(self.latest_purchase_quantity.text)