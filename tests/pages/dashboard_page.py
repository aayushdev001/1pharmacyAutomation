import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys


class DashboardPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        # self.dashboard_type_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/main/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div')))
        self.dashboard_type = None
        self.total_sale = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/main/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/span[2]')))
        self.total_purchase = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/main/div[3]/div[2]/div[1]/div/div[1]/div/div[2]/span[2]')))

    def get_total_sales_amount(self):
        # print(self.total_sale.text)
        return self.get_amount(self.total_sale.text)

    def get_total_purchase_amount(self):
        # print(self.total_purchase.text)
        return self.get_amount(self.total_purchase.text)

    def get_amount(self, exp):
        pattern = r'₹ (\d{1,3}(,\d{3})*(\.\d+)?)'

        match = re.search(pattern, exp)
        if match:
            value = float(match.group(1).replace(',', ''))  # Remove commas if present and convert to float
            return value
        else:
            return None

    def remove_commas(self, exp):
        cleaned_expression = exp.replace(",", "")
        return float(cleaned_expression)
