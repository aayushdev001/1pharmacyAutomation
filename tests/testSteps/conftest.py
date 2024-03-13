import random
import string

import pytest
from selenium import webdriver


# Define the fixture to create a WebDriver instance
@pytest.fixture
def driver():
    # Create ChromeOptions object
    chrome_options = webdriver.ChromeOptions()

    # Set preferences to allow notifications
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    # Create WebDriver instance with ChromeOptions
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver


@pytest.fixture
def config():
    return {
        "phone_number": '8123456780',
        "first_digit": "8",
        "second_digit": "8",
        "third_digit": "0",
        "fourth_digit": "0",
        "1pharmacy_login_url": 'https://alpha.1pharmacy.io/login',
        "1pharmacy_login_url_beta": "https://beta.pharmacyone.io",
        "1pharmacy_login_url_ros": "https://ros.1pharmacy.io/login",
        "billing_url_alpha": "https://alpha.1pharmacy.io/bill-entry/draft/1",
        "bill_history_url": 'https://alpha.1pharmacy.io/bill-history',
        "bill_history_url_ros": 'https://ros.1pharmacy.io/bill-history',
        "dashboard_url": "https://alpha.pharmacyone.io/dashboard",
        "purchase_url_alpha": "https://alpha.1pharmacy.io/purchase-entry",
        "purchase_history_url_alpha": "https://alpha.1pharmacy.io/purchase-history",
        "settings_sales_url":"https://alpha.1pharmacy.io/settings?tabQuery=bill",
        "item_quantity": 10,
        "item_return_quantity": 5,
        "item_purchase_quantity": 10,
        "purchase_item_expiry_date": "05028",
        "purchase_mrp": 100,
        "purchase_ptr": 80,
        "purchase_discount": 5,
        "purchase_gst": 12,
        "custom_batch_name": generate_random_string(3),
        "product_name": "Dolfin Tablet",
        "search_keyword": "dolf",
        "wait": 50
    }


def generate_random_string(length=3):
    return ''.join(random.choices(string.ascii_letters, k=length))
