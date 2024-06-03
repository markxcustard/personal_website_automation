from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.title = "Mark Custard - Portfolio"
        self.links = {
            "about": (By.XPATH, "//a[text()='About']"),
            "portfolio": (By.XPATH, "//a[text()='Portfolio']"),
            "testimonials": (By.XPATH, "//a[text()='Testimonials']"),
            "contact": (By.XPATH, "//a[text()='Contact']")
        }
        self.sections = {
            "about": (By.ID, "about"),
            "portfolio": (By.ID, "portfolio"),
            "testimonials": (By.ID, "testimonials"),
            "contact": (By.ID, "contact")
        }
        self.email_link = (By.XPATH, "//a[contains(@href, 'mailto:')]")
        self.linkedin_button = (By.XPATH, "//a[contains(@href, 'linkedin.com')]")
        self.github_button = (By.XPATH, "//a[contains(@href, 'github.com')]")

    def open(self):
        self.driver.get("https://markxcustard.github.io/")
        
    def go_to_section(self, section):
        link_locator = self.links[section]
        link = self.wait_for_element_to_be_clickable(link_locator)
        link.click()
        print(f"Navigated to {section} section")
        
    def verify_section(self, section):
        section_locator = self.sections[section]
        return self.wait_for_element_to_be_visible(section_locator).is_displayed()

    def expand_portfolio_item(self, item_text):
        try:
            portfolio_titles = self.driver.find_elements(By.CLASS_NAME, "portfolio-title")
            print(f"Found {len(portfolio_titles)} portfolio items.")
            for title in portfolio_titles:
                print(title.get_attribute('outerHTML'))
            item_link = self.wait_for_element_to_be_clickable((By.XPATH, f"//a[@class='portfolio-title' and contains(normalize-space(), '{item_text}')]"))
            item_link.click()
            print(f"Expanded portfolio item: {item_text}")
        except TimeoutException as e:
            print(f"TimeoutException: Could not expand portfolio item: {item_text} due to: {e}")

    def verify_portfolio_item_expanded(self, item_id, expected_text):
        try:
            item_expanded_content = self.wait_for_element_to_be_visible((By.ID, item_id), timeout=60)
            assert item_expanded_content.is_displayed()
            actual_text = item_expanded_content.text
            print(f"Expected text: {expected_text}")
            print(f"Actual text: {actual_text}")
            return expected_text in actual_text
        except TimeoutException as e:
            print(f"TimeoutException: Could not verify portfolio item expanded: {item_id} due to: {e}")
            return False

    def click_email_link(self):
        email_element = self.wait_for_element_to_be_clickable(self.email_link)
        email_element.click()
        print("Clicked on email link")

    def click_linkedin_button(self):
        self.retry_click(self.linkedin_button)
        print("Clicked on LinkedIn button")
        self.driver.execute_script("window.location.href = arguments[0];", self.wait_for_element_to_be_visible(self.linkedin_button).get_attribute('href'))
        
    def click_github_button(self):
        self.retry_click(self.github_button)
        print("Clicked on GitHub button")
        self.driver.execute_script("window.location.href = arguments[0];", self.wait_for_element_to_be_visible(self.github_button).get_attribute('href'))

    def wait_for_element_to_be_clickable(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_element_to_be_visible(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def retry_click(self, locator, attempts=3):
        for i in range(attempts):
            try:
                element = self.wait_for_element_to_be_clickable(locator)
                element.click()
                return
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(f"Retrying due to exception: {e}")
        raise Exception(f"Failed to click element after {attempts} attempts")
