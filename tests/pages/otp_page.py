import time

import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class OtpPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait)
        self.first_digit_input = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//body/div[@id="root"]/div[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[3]/div[1]/input[1]')))
        self.second_digit_input = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//body/div[@id='root']/div[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[3]/div[1]/input[2]")))
        self.third_digit_input = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='root']/div/div[2]/section/div/div[1]/div/div[3]/div/input[3]")))
        self.fourth_digit_input = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//body/div[@id='root']/div[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[3]/div[1]/input[4]")))
        self.login_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Login')]")))
        self.dashboard_link = None
        self.sidebar_xpath = None
        self.sidebar = None

    def enter_otp(self, first_digit, second_digit, third_digit, fourth_digit):
        self.first_digit_input.send_keys(first_digit)
        self.second_digit_input.send_keys(second_digit)
        self.third_digit_input.send_keys(third_digit)
        self.fourth_digit_input.send_keys(fourth_digit)

    def click_login(self):
        self.login_button.click()

    def navigate_dashboard(self):
        if self.sidebar is None:
            self.sidebar_xpath = '//*[@id="root"]/section/section'
            self.sidebar = self.wait.until(EC.presence_of_element_located((By.XPATH, self.sidebar_xpath)))

        # hovering on the sidebar
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(self.sidebar)
        pyautogui.moveTo(42, 206)
        pyautogui.click(42, 206)
        time.sleep(5)

        # clicking on the dashboard quicklink
        self.dashboard_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/section/div/div/ul/li[7]/a/div[2]/span')))
        # action_chains = ActionChains(self.driver)
        # action_chains.move_to_element(self.dashboard_link)
        # time.sleep(5)
        self.dashboard_link.click()
        pyautogui.moveTo(1000, 300)

    def navigate_billing_page(self):
        pyautogui.moveTo(5, 478)
