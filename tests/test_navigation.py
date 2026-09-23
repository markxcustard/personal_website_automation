"""Header, navigation menu and page-level checks.

Navigating the menu doesn't dirty the page, so these share one loaded page.
"""

import pytest

from page_objects.home_page import HomePage

EXPECTED_MENU = [
    ("hero", "Home"),
    ("about", "About"),
    ("resume", "Resume"),
    ("portfolio", "Portfolio"),
    ("technical-skills", "Technical Skills"),
    ("skills", "Skills"),
    ("testimonials", "Testimonials"),
    ("contact", "Contact"),
]

SECTIONS = [target for target, _ in EXPECTED_MENU]


@pytest.mark.smoke
def test_page_title(site):
    assert site.driver.title == HomePage.TITLE


@pytest.mark.smoke
def test_sitename_and_profile_image(site):
    assert site.text_of(HomePage.SITENAME) == "Mark Custard"
    assert site.find(HomePage.PROFILE_IMAGE).get_attribute("src").endswith(
        "my-profile-img.jpg"
    )


def test_menu_lists_every_section_in_order(site):
    assert site.nav_targets() == SECTIONS


def test_menu_labels(site):
    assert site.nav_labels() == [label for _, label in EXPECTED_MENU]


@pytest.mark.parametrize("section", SECTIONS)
def test_every_section_is_reachable_from_the_menu(site, section):
    site.go_to_section(section)
    assert site.section(section).is_displayed()


@pytest.mark.parametrize("section", SECTIONS[1:])
def test_menu_highlights_the_section_in_view(site, section):
    """Scrollspy only assigns the active item once the smooth scroll lands;
    ``go_to_section`` waits for that."""
    site.go_to_section(section)
    assert site.active_nav_section() == section


@pytest.mark.parametrize(
    "section, heading",
    [(s, label) for s, label in EXPECTED_MENU if s != "hero"],
)
def test_section_headings(site, section, heading):
    site.go_to_section(section)
    assert site.section_heading(section) == heading


def test_header_social_links(site):
    hrefs = [a.get_attribute("href") for a in site.reveal(HomePage.HEADER_SOCIAL_LINKS)]
    assert hrefs == [
        "https://github.com/markxcustard",
        "https://www.linkedin.com/in/mark-custard/",
    ]


def test_footer_is_present(site):
    assert site.reveal_one(HomePage.FOOTER).is_displayed()
