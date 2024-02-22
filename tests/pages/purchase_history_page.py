import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class PurchaseHistoryPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.latest_purchase = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/div[3]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]')))
        self.latest_bill_quantity = None
        self.medicine_link = None
        self.return_button = None

    def click_latest_bill(self):
        self.latest_purchase.click()

    def click_medicine_link(self, product_name):
        self.medicine_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, f'{product_name}')))
        self.medicine_link.click()