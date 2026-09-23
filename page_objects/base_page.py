"""Shared Selenium behaviour for every page object in the suite.

The site under test animates almost every element into view with AOS, which
means an element can be present in the DOM long before it is rendered. Anything
below the fold therefore reports ``is_displayed() == False`` and an empty
``.text`` until it has been scrolled to. The ``reveal*`` helpers exist so tests
never have to think about that.
"""

import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"

    # ----------------------------------------------------------------- waiting
    def _wait(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def wait_present(self, locator, timeout=DEFAULT_TIMEOUT):
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_until(self, predicate, timeout=DEFAULT_TIMEOUT, message=""):
        return self._wait(timeout).until(lambda _: predicate(), message)

    def wait_for_scroll_to_settle(self, timeout=DEFAULT_TIMEOUT):
        """Block until window.scrollY stops changing.

        The site sets ``scroll-behavior: smooth``, so a nav click starts an
        animation that outlives the click itself. Scrollspy only assigns the
        active menu item once that animation lands, so anything asserting on
        scroll position or the active link has to wait for it.
        """
        last = None
        stable = 0
        deadline = time.time() + timeout
        while time.time() < deadline:
            current = self.driver.execute_script("return window.scrollY;")
            stable = stable + 1 if current == last else 0
            if stable >= 2:
                return current
            last = current
            time.sleep(0.1)
        return last

    # ---------------------------------------------------------------- querying
    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def is_present(self, locator):
        return bool(self.find_all(locator))

    # --------------------------------------------------------------- revealing
    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            element,
        )
        return element

    def reveal(self, locator, timeout=DEFAULT_TIMEOUT):
        """Scroll every match into view and wait for AOS to finish revealing them."""
        elements = self.find_all(locator)
        if not elements:
            raise AssertionError(f"No elements matched {locator}")
        for element in elements:
            self.scroll_into_view(element)
        self._wait(timeout).until(
            lambda _: all(e.is_displayed() for e in self.find_all(locator)),
            f"Elements matching {locator} never became visible",
        )
        return self.find_all(locator)

    def reveal_one(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.wait_present(locator, timeout)
        self.scroll_into_view(element)
        return self.wait_visible(locator, timeout)

    # ------------------------------------------------------------------ text
    def text_of(self, element_or_locator):
        """Read text via ``textContent`` so off-screen nodes still answer.

        Needed for the testimonial carousel, where Swiper keeps all but the
        active slides out of the rendered flow.
        """
        element = (
            element_or_locator
            if isinstance(element_or_locator, WebElement)
            else self.find(element_or_locator)
        )
        return self.driver.execute_script(
            "return arguments[0].textContent.trim();", element
        )

    def texts_of(self, locator):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll(arguments[0]))"
            ".map(e => e.textContent.trim());",
            locator[1],
        )

    # ---------------------------------------------------------------- actions
    def js_click(self, element):
        """Click without needing the element under the cursor.

        The site has a fixed sidebar and sticky offsets that intercept real
        clicks on narrow viewports; a scripted click sidesteps that without
        changing what the page itself does in response.
        """
        self.scroll_into_view(element)
        self.driver.execute_script("arguments[0].click();", element)
