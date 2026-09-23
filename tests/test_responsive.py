"""Mobile viewport behaviour.

Below the xl breakpoint the template slides the whole sidebar off-canvas with
``.header { left: -100% }`` and brings it back by adding ``.header-show``. It is
never ``display: none``, so ``is_displayed()`` returns True either way — an
assertion on visibility here would pass whether the menu opened or not. These
tests assert the state class and the header's actual position instead.
"""

import pytest

from page_objects.home_page import HomePage

MOBILE = (390, 844)  # iPhone-ish


@pytest.fixture
def mobile_home(driver, base_url):
    original = driver.get_window_size()
    driver.set_window_size(*MOBILE)
    yield HomePage(driver, base_url).open()
    driver.set_window_size(original["width"], original["height"])


def header_right_edge(page):
    return page.driver.execute_script(
        "return document.querySelector('#header').getBoundingClientRect().right;"
    )


def header_classes(page):
    return page.find(HomePage.HEADER).get_attribute("class")


@pytest.mark.responsive
def test_toggle_is_offered_on_mobile(mobile_home):
    assert mobile_home.wait_visible(HomePage.HEADER_TOGGLE).is_displayed()


@pytest.mark.responsive
def test_sidebar_starts_off_canvas(mobile_home):
    assert "header-show" not in header_classes(mobile_home)
    assert header_right_edge(mobile_home) <= 0, "sidebar is not off-canvas"


@pytest.mark.responsive
def test_toggle_slides_the_sidebar_in(mobile_home):
    mobile_home.js_click(mobile_home.wait_visible(HomePage.HEADER_TOGGLE))
    mobile_home.wait_until(
        lambda: "header-show" in header_classes(mobile_home),
        message="tapping the toggle did not add .header-show",
    )
    # The sidebar slides in on a CSS transition, so poll rather than read once.
    mobile_home.wait_until(
        lambda: header_right_edge(mobile_home) > 0,
        message="the sidebar never came on screen",
    )


@pytest.mark.responsive
def test_toggle_slides_the_sidebar_away_again(mobile_home):
    toggle = mobile_home.wait_visible(HomePage.HEADER_TOGGLE)
    mobile_home.js_click(toggle)
    mobile_home.wait_until(lambda: "header-show" in header_classes(mobile_home))
    mobile_home.js_click(toggle)
    mobile_home.wait_until(
        lambda: "header-show" not in header_classes(mobile_home),
        message="tapping the toggle again did not remove .header-show",
    )
    mobile_home.wait_until(
        lambda: header_right_edge(mobile_home) <= 0,
        message="the sidebar never went back off-canvas",
    )


@pytest.mark.responsive
def test_toggle_reports_its_state_to_assistive_technology(mobile_home):
    toggle = mobile_home.wait_visible(HomePage.HEADER_TOGGLE)
    assert toggle.get_attribute("aria-expanded") == "false"
    mobile_home.js_click(toggle)
    mobile_home.wait_until(
        lambda: mobile_home.find(HomePage.HEADER_TOGGLE).get_attribute("aria-expanded")
        == "true",
        message="aria-expanded was not updated when the menu opened",
    )


@pytest.mark.responsive
def test_toggle_is_hidden_on_desktop(home):
    assert not home.find(HomePage.HEADER_TOGGLE).is_displayed()
    assert home.find(HomePage.NAV).is_displayed()
    assert header_right_edge(home) > 0


@pytest.mark.responsive
def test_portfolio_cards_stack_without_horizontal_overflow(mobile_home):
    mobile_home.go_to_section("portfolio")
    overflow = mobile_home.driver.execute_script(
        "return document.documentElement.scrollWidth - document.documentElement.clientWidth;"
    )
    assert overflow <= 1, f"page scrolls horizontally by {overflow}px on mobile"
