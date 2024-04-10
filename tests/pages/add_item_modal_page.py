import time

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class AddItemModalPage:
    def __init__(self, driver):
        self.add_item_button = None
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver

    def click_add_item(self):
        self.add_item_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(), 'Add Item')])[2]")))
        try:
            self.add_item_button.click()
        except TimeoutException:
            self.driver.execute_script("arguments[0].click();", self.add_item_button)
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", self.add_item_button)

        # print("clicked")
