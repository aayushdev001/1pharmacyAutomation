import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class InventoryPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.search_box = None

    def search_medicine(self, medicine):
        self.search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        self.search_box.send_keys(medicine)

    def click_medicine_link(self, medicine):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f"//span[@aria-label='{medicine}']"))).click()
