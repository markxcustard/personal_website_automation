from page_objects.home_page import HomePage
import pytest
import time
import os

@pytest.mark.usefixtures("driver")
class TestNavigation:

    @pytest.mark.parametrize("section", ["about", "portfolio", "projects", "testimonials", "contact"])
    def test_navigation(self, driver, section):
        home_page = HomePage(driver)
        home_page.open()
        assert home_page.title in driver.title

        home_page.go_to_section(section)
        time.sleep(2)  # Wait for navigation to complete

        assert home_page.verify_section(section)


@pytest.mark.usefixtures("driver")
class TestAboutMe:

    def test_about_me_paragraph(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("about")
        time.sleep(2)  # Wait for navigation to complete

        expected_paragraph = ("Furthermore, I have implemented post-deployment strategies, including smoke and regression testing, and spot-checking, to ensure that core functionalities remain intact after updates and that deliverables meet predefined quality standards.")
        
        assert home_page.verify_about_me_text(expected_paragraph)

    def test_personal_website_automation_link(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("projects")
        time.sleep(2)  # Wait for navigation to complete

        expected_github_url = "https://github.com/markxcustard/personal_website_automation"

    def test_pandas_filtering_films_link(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("projects")
        time.sleep(2)  # Wait for navigation to complete

        expected_github_url = "https://github.com/markxcustard/pandas_filtering_films"
        
        assert home_page.verify_pandas_filtering_films_link(expected_github_url)

    def test_resume_download(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("about")
        time.sleep(2)  # Wait for navigation to complete

        expected_file_name = "resume_mark_custard.pdf"
        
        assert home_page.verify_resume_download(expected_file_name)


@pytest.mark.usefixtures("driver")
class TestPortfolio:

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
            ("Technical Skills", "tech-skills-details", "Pytest, Postman, Testrail, Browserstack, Unit Testing, Integration Testing, Rainforest No Code QA Tool, Test Design, Test Writing, Test Coverage, Code Coverage, Test Planning, Functional Testing, Regression Testing, Exploratory Testing, Smoke Testing, Sanity Testing, Spot Checking, Data Analysis, Root Cause Analysis, Debugging, Salesforce, BigQuery, Selenium, Gherkin, Cucumber.")
        ]

        for item_text, item_id, expected_text in portfolio_items:
            home_page.expand_portfolio_item(item_text)
            is_expanded = home_page.verify_portfolio_item_expanded(item_id, expected_text)
            if not is_expanded:
                print(f"Verification failed for item {item_text} with ID {item_id}")
            assert is_expanded


@pytest.mark.usefixtures("driver")
class TestTestimonials:

    def test_testimonial_paragraph(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("testimonials")
        time.sleep(2)  # Wait for navigation to complete

        expected_testimonial = ('"I only needed a day to know how valuable Mark is on a QA team. '
                                'His experience, dedication and commitment are truly out of the ordinary. '
                                'He will get the job done, no questions asked."')
        
        assert home_page.verify_testimonial_text(expected_testimonial)

@pytest.mark.usefixtures("driver")
class TestContact:

    def test_contact_details(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        home_page.go_to_section("contact")
        time.sleep(2)  # Wait for navigation to complete

        assert home_page.verify_contact_email("mark.a.custard@gmail.com")
        assert home_page.verify_contact_phone("(360) 771-0564")
        assert home_page.verify_social_button("github.com", "https://github.com/markxcustard")
        assert home_page.verify_social_button("linkedin.com", "https://www.linkedin.com/in/mark-custard/")
