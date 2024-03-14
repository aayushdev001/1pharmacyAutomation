import pytest

from tests.pages.billing_page import BillingPage
from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil
from tests.testSteps.conftest import driver, config


@pytest.mark.usefixtures("driver", "config")
class TestBillingWithMissingFeilds(BaseClass):
    def test_billing_with_missing_fields(self, driver, config):
        # report logging
        log = self.get_logger()

        # login
        login_util = LoginUtil(driver, config)
        login_util.login()

        # billing
        billing_page = BillingPage(driver)
        billing_page.click_submit()
        assert billing_page.is_missing_field_alert() == True