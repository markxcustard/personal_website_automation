"""Testimonials carousel."""

import pytest

from page_objects.home_page import HomePage

EXPECTED = [
    ("Santiago Guerrero", "SR Software Development Engineer in Testing at Glassdoor",
     "https://www.linkedin.com/in/sguerrero22/"),
    ("Jon Kim", "iOS Developer at Stake",
     "https://www.linkedin.com/in/jonathanyjkim/"),
    ("Julia Guimiot", "Back End Software Engineer at Stake",
     "https://www.linkedin.com/in/juliaguimiot/"),
    ("Dominic Withers", "Managing Director & Co-Founder at Withers & Wagg",
     "https://www.linkedin.com/in/dominic-withers-221002100/"),
    ("Kristian Andrews-Brown", "Founder of TAG Parking",
     "https://www.linkedin.com/in/kristian-andrews-82543b109"),
]

NAMES = [name for name, _, _ in EXPECTED]


@pytest.fixture(scope="module")
def testimonials(site):
    site.go_to_section("testimonials")
    return {
        "entries": site.testimonials(),
        "bullets": len(site.find_all(HomePage.TESTIMONIAL_BULLETS)),
    }


def test_every_testimonial_is_present(testimonials):
    assert [t["name"] for t in testimonials["entries"]] == NAMES


@pytest.mark.parametrize("name, role, linkedin", EXPECTED, ids=NAMES)
def test_testimonial_details(testimonials, name, role, linkedin):
    entry = next(t for t in testimonials["entries"] if t["name"] == name)
    assert entry["role"] == role
    assert entry["linkedin"] == linkedin
    assert len(entry["quote"]) > 40, "quote looks truncated or empty"


def test_pagination_has_one_bullet_per_testimonial(testimonials):
    assert testimonials["bullets"] == len(EXPECTED)


def test_carousel_starts_on_the_first_testimonial(home):
    home.go_to_section("testimonials")
    assert home.active_testimonial_name() == NAMES[0]


def test_pagination_changes_the_active_testimonial(home):
    """Autoplay runs on a 5s delay, so assert that the slide changed rather
    than that it landed on one specific name."""
    home.go_to_section("testimonials")
    before = home.active_testimonial_name()
    after = home.show_testimonial(2)
    assert after != before
    assert after in NAMES
