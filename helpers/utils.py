from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Utils:
    @staticmethod
    def wait_for_element_to_be_clickable(driver, locator, timeout=30):
        try:
            return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            return None

    @staticmethod
    def wait_for_element_to_be_visible(driver, locator, timeout=30):
        try:
            return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return None
