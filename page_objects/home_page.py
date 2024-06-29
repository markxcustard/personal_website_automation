import os
import glob
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
            "projects": (By.XPATH, "//a[text()='Projects']"),
            "testimonials": (By.XPATH, "//a[text()='Testimonials']"),
            "contact": (By.XPATH, "//a[text()='Contact']")
        }
        self.sections = {
            "about": (By.ID, "about"),
            "portfolio": (By.ID, "portfolio"),
            "projects": (By.ID, "projects"),
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

    def verify_about_me_text(self, expected_text):
        about_me_section = self.wait_for_element_to_be_visible(self.sections['about'])
        actual_text = about_me_section.text.strip()

        # Normalize whitespace
        actual_text = ' '.join(actual_text.split())
        expected_text = ' '.join(expected_text.split())

        if expected_text in actual_text:
            print(f"Expected text found in About Me section")
            return True
        else:
            print(f"Expected text not found in About Me section")
            return False

    def verify_personal_website_automation_link(self, expected_url):
        about_me_section = self.wait_for_element_to_be_visible(self.sections['projects'])
        github_link = about_me_section.find_element(By.XPATH, ".//a[contains(@href, 'github.com/markxcustard/personal_website_automation')]")
        actual_url = github_link.get_attribute('href')

        if actual_url == expected_url:
            print(f"GitHub link URL is correct: {actual_url}")
            return True
        else:
            print(f"GitHub link URL is incorrect: {actual_url}")
            return False
        
    def verify_pandas_filtering_films_link(self, expected_url):
            about_me_section = self.wait_for_element_to_be_visible(self.sections['projects'])
            github_link = about_me_section.find_element(By.XPATH, ".//a[contains(@href, 'github.com/markxcustard/pandas_filtering_films')]")
            actual_url = github_link.get_attribute('href')

            if actual_url == expected_url:
                print(f"GitHub link URL is correct: {actual_url}")
                return True
            else:
                print(f"GitHub link URL is incorrect: {actual_url}")
                return False
            
    def verify_resume_download(self, expected_file_name):
        about_me_section = self.wait_for_element_to_be_visible(self.sections['about'])
        download_button = about_me_section.find_element(By.XPATH, ".//a[contains(@href, 'img/resume_mark_custard.pdf')]")
        download_button.click()
        
        # Wait for the file to be downloaded
        time.sleep(5)  # Adjust time if necessary for file download
        
        # Check for the presence of any file that starts with the expected file name in the default download directory
        download_dir = os.path.expanduser('~/Downloads')  # Default download directory for many systems
        downloaded_files = glob.glob(os.path.join(download_dir, f"{expected_file_name}*"))
        if downloaded_files:
            print(f"Resume downloaded successfully to: {downloaded_files[0]}")
            return True
        else:
            print(f"Failed to download resume to: {download_dir}")
            return False

    def verify_contact_email(self, expected_email):
        contact_section = self.wait_for_element_to_be_visible(self.sections['contact'])
        email_link = contact_section.find_element(By.XPATH, ".//a[contains(@href, 'mailto:')]")
        actual_email = email_link.get_attribute('href').replace('mailto:', '')

        if actual_email == expected_email:
            print(f"Email link is correct: {actual_email}")
            return True
        else:
            print(f"Email link is incorrect: {actual_email}")
            return False

    def verify_contact_phone(self, expected_phone):
        contact_section = self.wait_for_element_to_be_visible(self.sections['contact'])
        phone_element = contact_section.find_element(By.XPATH, ".//p[contains(., 'Phone:')]")
        actual_phone = phone_element.text.split('Phone:')[1].strip()

        if actual_phone == expected_phone:
            print(f"Phone number is correct: {actual_phone}")
            return True
        else:
            print(f"Phone number is incorrect: {actual_phone}")
            return False

    def verify_social_button(self, platform, expected_url):
        contact_section = self.wait_for_element_to_be_visible(self.sections['contact'])
        button = contact_section.find_element(By.XPATH, f".//a[contains(@href, '{platform}')]")
        actual_url = button.get_attribute('href')

        if actual_url == expected_url:
            print(f"{platform.capitalize()} button URL is correct: {actual_url}")
            return True
        else:
            print(f"{platform.capitalize()} button URL is incorrect: {actual_url}")
            return False

    def verify_testimonial_text(self, expected_text):
        testimonials_section = self.wait_for_element_to_be_visible(self.sections['testimonials'])
        actual_text = testimonials_section.text.strip()

        # Normalize whitespace
        actual_text = ' '.join(actual_text.split())
        expected_text = ' '.join(expected_text.split())

        if expected_text in actual_text:
            print(f"Expected text found in Testimonials section")
            return True
        else:
            print(f"Expected text not found in Testimonials section")
            return False

    def wait_for_element_to_be_clickable(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_element_to_be_visible(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
