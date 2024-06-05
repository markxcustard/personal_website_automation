from helpers.utils import Utils

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element_to_be_clickable(self, locator, timeout=30):
        return Utils.wait_for_element_to_be_clickable(self.driver, locator, timeout)

    def wait_for_element_to_be_visible(self, locator, timeout=30):
        return Utils.wait_for_element_to_be_visible(self.driver, locator, timeout)
