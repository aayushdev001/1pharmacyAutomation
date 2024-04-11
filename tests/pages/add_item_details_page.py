import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class AddItemDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.name_input = None
        self.item_mrp_input = None
        self.unit_input = None
        self.unit_list = None
        self.batch_input = None
        self.quantity_input = None
        self.expiry_input = None
        self.batch_mrp_input = None
        self.save_button = None

    def enter_name(self, name):
        self.name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@name="name"])[2]')))
        self.name_input.send_keys(name)

    def enter_mrp(self, mrp):
        self.item_mrp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="mrp"]')))
        self.item_mrp_input.send_keys(mrp)

    def enter_unit(self, unit):
        self.unit_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="packWeightage"]')))
        self.unit_input.send_keys(unit)

    def select_unit_type(self, type1):
        self.unit_list = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[3]/div[3]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/div[6]/div[1]/div[1]/div[1]')))
        self.unit_list.click()
        item_type = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-value="Tablet"]')))
        self.driver.execute_script("arguments[0].click();", item_type)
        # self.wait.until(EC.presence_of_element_located((By.XPATH, f"//ul[contains(li/text(), {type})]"))).click()

    def enter_batch(self, name):
        self.batch_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="batchNo"]')))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.batch_input.send_keys(name)

    def enter_quantity(self, qty):
        self.quantity_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="qty"]')))
        self.quantity_input.send_keys(qty)

    def enter_expiry(self, exp):
        self.expiry_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='mm/yyyy']")))
        self.expiry_input.send_keys(exp)

    def enter_batch_mrp(self, mrp):
        self.batch_mrp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@name="mrp"])[2]')))
        self.batch_mrp_input.send_keys(mrp)

    def click_save(self):
        self.save_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save')]")))
        self.save_button.click()

