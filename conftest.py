"""Fixtures and command line options for the portfolio test suite.

Driver binaries are resolved by Selenium Manager (built into Selenium 4.6+), so
there are no hard coded chromedriver/geckodriver paths to keep in sync.
"""

import shutil
import tempfile

import pytest
from selenium import webdriver

from page_objects.home_page import HomePage

DEFAULT_BASE_URL = "https://markcustard.com/"
WINDOW_SIZE = (1600, 1000)  # wide enough for the sidebar nav to be expanded


def pytest_addoption(parser):
    group = parser.getgroup("portfolio tests")
    group.addoption(
        "--base-url",
        action="store",
        default=DEFAULT_BASE_URL,
        help=f"Site under test (default: {DEFAULT_BASE_URL})",
    )
    group.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox", "safari"),
        help="Browser to run against (default: chrome)",
    )
    group.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run the browser headless (ignored for safari, which has no headless mode)",
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def download_dir():
    """Throwaway download directory, so the resume test never touches ~/Downloads."""
    path = tempfile.mkdtemp(prefix="portfolio-downloads-")
    yield path
    shutil.rmtree(path, ignore_errors=True)


def _chrome(headless, download_dir):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
        },
    )
    return webdriver.Chrome(options=options)


def _firefox(headless, download_dir):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)
    return webdriver.Firefox(options=options)


def _safari(_headless, _download_dir):
    return webdriver.Safari()


BUILDERS = {"chrome": _chrome, "firefox": _firefox, "safari": _safari}


@pytest.fixture(scope="session")
def driver(request, browser_name, download_dir):
    headless = request.config.getoption("--headless")
    instance = BUILDERS[browser_name](headless, download_dir)
    instance.set_window_size(*WINDOW_SIZE)
    instance.implicitly_wait(0)  # explicit waits only
    yield instance
    instance.quit()


@pytest.fixture
def home(driver, base_url):
    """A freshly loaded home page, so no test inherits another's scroll position.

    Use this for anything that clicks, types or resizes.
    """
    return HomePage(driver, base_url).open()


@pytest.fixture(scope="session")
def site(driver, base_url):
    """A page loaded once for the whole run.

    Read-only assertions (copy, links, percentages) don't need a fresh load
    each time, and reloading for every parametrised case dominated the runtime.
    Modules cache what they scrape from this in a module-scoped fixture.
    """
    return HomePage(driver, base_url).open()
