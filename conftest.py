import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService

@pytest.fixture(params=["firefox", "chrome", "safari"], scope="class")
def driver(request):
    browser = request.param
    headless = request.config.getoption("--headless")
    print(f"Opening {browser} browser in {'headless' if headless else 'normal'} mode")
    
    if browser == "firefox":
        service = FirefoxService(executable_path='/usr/local/bin/geckodriver')
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        my_driver = webdriver.Firefox(service=service, options=options)
    elif browser == "chrome":
        service = ChromeService(executable_path='/usr/local/bin/chromedriver')
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        my_driver = webdriver.Chrome(service=service, options=options)
    elif browser == "safari":
        options = webdriver.SafariOptions()
        service = SafariService()
        my_driver = webdriver.Safari(service=service, options=options)
    else:
        raise TypeError(f"Expected 'firefox', 'chrome', or 'safari', but got {browser}")
    
    my_driver.maximize_window()
    yield my_driver
    print(f"\nClosing {browser} browser")
    my_driver.quit()

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="firefox", help="browser to execute tests (chrome, firefox, or safari)"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="run browsers in headless mode"
    )
