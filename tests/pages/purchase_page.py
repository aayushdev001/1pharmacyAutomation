import re

from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.product_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1p-basic-text"]')))
        self.batch_input = None
        self.batch = None
        self.quantity_input = None
        self.quantity = 0
        self.stock = None
        self.expiry_date_input = None
        self.mrp_input = None
        self.unit_mrp = 0
        self.purchase_rate_input = None
        self.supplier_input = None
        self.supplier = None
        self.invoice_number = None
        self.submit_button = None
        self.gst_input = None
        self.gst = None
        self.discount_input = None
        self.item_total = None

    def enter_product_name(self, keyword):
        self.product_input.send_keys(keyword)

    def select_product(self, keyword, product_name):
        self.enter_product_name(keyword)
        product = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{product_name}')]")))
        # for product in product_list:
        #     print(product.text)
        #     if product.text == product_name:
        product.click()

    def enter_quantity(self, quantity):
        # self.strip_stock = self.get_strip()
        self.quantity = quantity
        self.quantity_input = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/div[1]/input[1]')))
        self.quantity_input.send_keys(quantity)
        # time.sleep(8)

    def enter_batch(self, batch):
        self.batch_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                       "//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[7]/div[1]/div[1]/div[1]/input[1]")))
        # print(self.batch_input.get_attribute('value'))
        # self.batch_input.click()
        # self.batch_input.send_keys(Keys.BACKSPACE * len(self.batch_input.get_attribute('value')))
        # time.sleep(1)
        self.batch_input.send_keys(batch)

    def select_batch(self):
        self.batch_input = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                       "//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[7]/div[1]/div[1]/div[1]/input[1]")))
        self.batch_input.click()
        self.batch = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'ABCD')]")))
        self.batch.click()

    def enter_expiry_date(self, date):
        self.expiry_date_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[8]/div[1]/div[1]/input[1]')))
        self.expiry_date_input.send_keys(date)

    def enter_mrp(self, mrp):
        self.mrp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[9]/div[1]/div[1]/input[1]')))
        # self.mrp_input.clear()
        self.mrp_input.click()
        self.mrp_input.send_keys(Keys.BACKSPACE * len(self.mrp_input.get_attribute('value')))
        self.mrp_input.send_keys(mrp)

    def enter_purchase_rate(self, purchase_rate):
        self.purchase_rate_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[10]/div[1]/div[1]/input[1]')))
        # self.purchase_rate_input.clear()
        self.purchase_rate_input.click()
        self.purchase_rate_input.send_keys(Keys.BACKSPACE * len(self.purchase_rate_input.get_attribute('value')))
        self.purchase_rate_input.send_keys(purchase_rate)

    def enter_gst(self, gst):
        self.gst_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/div[1]/div[1]/input[1]')))
        self.driver.execute_script("arguments[0].click();", self.gst_input)
        self.gst_input.send_keys(Keys.BACKSPACE * len(self.gst_input.get_attribute('value')))
        self.gst_input.send_keys(gst)
        self.gst = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[text()='" + gst + "']")))
        self.gst.click()

    def enter_discount(self, discount):
        self.discount_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[15]/div[1]/div[1]/input[1]')))
        self.discount_input.send_keys(discount)

    def get_item_total(self):
        self.item_total = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                          '//body[1]/div[1]/section[1]/main[1]/section[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[17]')))
        # print(f"Item total = {self.item_total.text}")
        match = re.search(r'₹ (\d+(\.\d*)?)', self.item_total.text)
        # print(f"Item total = {matches[0]}")
        if match:
            return float(match.group(1))
        else:
            return None

    def enter_invoice_number(self, invoice_number):
        self.invoice_number = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/input[1]')))
        self.invoice_number.send_keys(invoice_number)

    def select_supplier_name(self):
        self.supplier_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]')))
        self.supplier_input.click()
        self.supplier = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             "//p[contains(text(),'AMAZON DISTRIBUTORES PRIVATE LIMITED')]")))
        self.supplier.click()

    def click_submit(self):
        self.submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//body[1]/div[1]/section[1]/main[1]/section[1]/div[2]/section[1]/div[2]/div[1]/button[2]')))
        self.submit_button.click()

    def click_done(self):
        # self.done_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/button[1]')))
        # self.done_button.click()
        # pyautogui.click(216,418)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

