from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException
import time

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
        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            try:
                item_link = self.wait_for_element_to_be_clickable((By.XPATH, f"//a[@class='portfolio-title' and contains(normalize-space(), '{item_text}')]"))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", item_link)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(item_link))
                self.driver.execute_script("arguments[0].click();", item_link)  # Use JavaScript click
                time.sleep(2)  # Wait for the item to expand
                print(f"Expanded portfolio item: {item_text}")
                return
            except (ElementClickInterceptedException, WebDriverException) as e:
                print(f"Exception: Could not click on portfolio item: {item_text} due to: {e}. Retrying...")
                attempts += 1
                self.driver.execute_script("window.scrollBy(0, -100);")  # Scroll up slightly
            except TimeoutException as e:
                print(f"TimeoutException: Could not expand portfolio item: {item_text} due to: {e}")
                break

        if attempts == max_attempts:
            raise Exception(f"Failed to expand portfolio item: {item_text} after {max_attempts} attempts")

    def verify_portfolio_item_expanded(self, item_id, expected_text):
        try:
            item_expanded_content = self.wait_for_element_to_be_visible((By.ID, item_id), timeout=60)
            assert item_expanded_content.is_displayed()
            actual_text = item_expanded_content.text.strip()
            expected_text = expected_text.strip()

            # Normalize whitespace
            actual_text = ' '.join(actual_text.split())
            expected_text = ' '.join(expected_text.split())

            # Split the expected text into phrases and check if each is present in the actual text
            expected_phrases = expected_text.split(', ')
            for phrase in expected_phrases:
                if phrase not in actual_text:
                    print(f"Missing expected phrase: {phrase}")
                    return False

            print(f"Expected text: {expected_text}")
            print(f"Actual text: {actual_text}")
            return True
        except TimeoutException as e:
            print(f"TimeoutException: Could not verify portfolio item expanded: {item_id} due to: {e}")
            return False

    def wait_for_element_to_be_clickable(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_element_to_be_visible(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
