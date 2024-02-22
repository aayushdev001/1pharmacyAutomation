import time
import logging

import pytest

from tests.testSteps.base_class import BaseClass
from tests.utils.login_util import LoginUtil


@pytest.mark.usefixtures("driver", "config")
class TestLogin(BaseClass):
    def test_login(self, driver, config):
        # report logging
        log = self.get_logger()

        login_util = LoginUtil(driver, config)
        login_util.login()
        log.info(f"Home page url -> {driver.current_url}")
        assert "https://alpha.1pharmacy.io/bill-entry/draft/1" in driver.current_url

