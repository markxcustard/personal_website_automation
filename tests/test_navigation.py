from page_objects.home_page import HomePage
import pytest
import time

@pytest.mark.usefixtures("driver")
class TestNavigation:

    @pytest.mark.parametrize("section", ["about", "portfolio", "testimonials", "contact"])
    def test_navigation(self, driver, section):
        home_page = HomePage(driver)
        home_page.open()
        assert home_page.title in driver.title

        home_page.go_to_section(section)
        time.sleep(2)  # Wait for navigation to complete

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
            ("Technical Skills", "tech-skills-details", "Pytest, Postman, Testrail, Browserstack, Unit Testing, Integration Testing, Rainforest No Code QA Tool, Test Design, Test Writing, Test Coverage, Code Coverage, Test Planning, Functional Testing, Regression Testing, Exploratory Testing, Smoke Testing, Sanity Testing, Spot Checking, Data Analysis, Root Cause Analysis, Debugging, Salesforce, BigQuery, Selenium.")
        ]

        for item_text, item_id, expected_text in portfolio_items:
            home_page.expand_portfolio_item(item_text)
            is_expanded = home_page.verify_portfolio_item_expanded(item_id, expected_text)
            if not is_expanded:
                print(f"Verification failed for item {item_text} with ID {item_id}")
            assert is_expanded
