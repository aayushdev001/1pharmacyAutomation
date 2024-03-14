import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class SettingsSalesPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 20)
        self.driver = driver
        self.strict_quantity_check_toggle = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                            '//*[@id="root"]/section/main/div[3]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]/label/span[1]/span[1]')))
        self.schedule_drug_warning_toggle = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/main/div[3]/div[2]/div[1]/div[2]/div/div/div[1]/div[10]/div/div[2]/label/span[1]/span[1]')))
        self.save_settings_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/main/div[3]/div[2]/div[2]/button')))

    def toggle_strict_quantity(self):
        self.strict_quantity_check_toggle.click()

    def toggle_schedule_drug_warning(self):
        self.schedule_drug_warning_toggle.click()

    def is_strict_quantity_check_on(self):
        if "Mui-checked" in self.strict_quantity_check_toggle.get_attribute('class'):
            return True
        else:
            return False

    def is_schedule_drug_warning_disabled(self):
        if "Mui-checked" in self.schedule_drug_warning_toggle.get_attribute('class'):
            return True
        else:
            return False

    def save_settings(self):
        self.save_settings_button.click()
