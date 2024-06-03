import pytest
from page_objects.home_page import HomePage
import time
from selenium.common.exceptions import WebDriverException

@pytest.mark.usefixtures("driver")
class TestNavigation:

    @pytest.mark.parametrize("section", ["about", "portfolio", "testimonials", "contact"])
    def test_navigation(self, driver, section):
        home_page = HomePage(driver)
        home_page.open()
        print("Initial URL:", driver.current_url)
        print("Initial Page title:", driver.title)
        assert home_page.title in driver.title

        home_page.go_to_section(section)
        time.sleep(2)  # Wait for navigation to complete

        print("Final URL:", driver.current_url)
        print("Final Page title:", driver.title)

        # Verify the specified section is displayed
        assert home_page.verify_section(section)

    def test_portfolio_expansion(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("portfolio")
        time.sleep(2)  # Wait for navigation to complete

        portfolio_items = [
            ("QA Analyst at Stake (Fintech Industry)", "stake-details", "Ensured the integrity and functionality of web and mobile applications across Android and iOS platforms, overseeing quality standards for app releases as a KPR."),
            ("QA Engineer at CSC Generation", "csc-details", "Worked closely with multiple departments to clearly define and analyze requirements for new features and functionalities."),
            ("Software QA Analyst at Kemper Insurance", "kemper-details", "Actively participated in daily stand-up meetings and produced daily dashboard reports, enhancing project communication and status tracking."),
            ("Software QA Analyst at American Access Casualty Company", "american-access-details", "Led initiatives to enhance unit testing coverage and developed comprehensive test suites, significantly advancing the automation of end-to-end testing."),
            ("Junior Application Developer at American Access Casualty Company", "junior-developer-details", "Prepared detailed documentation for program requirements and contributed to research on emerging software technologies, supporting ongoing development efforts and innovation."),
            ("Technical Skills", "tech-skills-details", "Pytest, Postman, Testrail, Browserstack, Unit Testing, Integration Testing, Rainforest No Code QA Tool, Test Design, Test Writing, Test Coverage, Code Coverage, Test Planning, Functional Testing, Regression Testing, Exploratory Testing, Smoke Testing, Sanity Testing, Spot Checking, Data Analysis, Root Cause Analysis, Debugging, Salesforce, BigQuery.")
        ]

        for item_text, item_id, expected_text in portfolio_items:
            home_page.expand_portfolio_item(item_text)
            time.sleep(1)  # Wait for the item to expand
            assert home_page.verify_portfolio_item_expanded(item_id, expected_text)

    def test_email_link(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_email_link()
        time.sleep(1)  # Wait for the action to complete
        # Verifying email popup requires manual verification

    def test_linkedin_button(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.click_linkedin_button()
        time.sleep(2)  # Wait for the action to complete
        # Switch to the new window/tab if opened
        windows = driver.window_handles
        print(f"Windows after clicking LinkedIn button: {windows}")
        if len(windows) > 1:
            driver.switch_to.window(windows[1])
        print("LinkedIn URL:", driver.current_url)
        assert "linkedin.com" in driver.current_url

    def test_github_button(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        self.retry_click_github_button(home_page)

    def retry_click_github_button(self, home_page, attempts=3):
        for attempt in range(attempts):
            try:
                home_page.click_github_button()
                time.sleep(2)  # Wait for the action to complete
                # Check if the URL has changed to GitHub
                print("GitHub URL:", home_page.driver.current_url)
                assert "github.com" in home_page.driver.current_url
                return
            except WebDriverException as e:
                print(f"Attempt {attempt + 1} failed with WebDriverException: {e}")
                if attempt == attempts - 1:
                    raise
