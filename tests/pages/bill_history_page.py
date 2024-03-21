import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium import webdriver


class BillHistoryPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.latest_bill = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/main/div[3]/div[2]/div/div[2]/table/tbody/tr')))
        self.latest_bill_quantity = None
        self.medicine_link = None
        self.return_button = None
        self.payment_type = None

    def click_latest_bill(self):
        self.latest_bill.click()

    def get_latest_bill_quantity(self):
        self.latest_bill_quantity = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/main/div[3]/div/div[2]/div/div[2]/table/tbody/tr/td[6]')))
        return int(self.latest_bill_quantity.text)

    def click_medicine_link(self, product_name):
        self.medicine_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, f'{product_name}')))
        self.medicine_link.click()

    def click_return(self):
        self.return_button = self.wait.until((EC.presence_of_element_located((By.XPATH, "//body/div[@id='root']/section[1]/main[1]/div[3]/div[1]/div[3]/div[2]/button[1]"))))
        self.return_button.click()

    def get_payment_type(self):
        self.payment_type = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]')))
        return self.payment_type.text