"""Hero banner."""

import pytest

from page_objects.home_page import HomePage

EXPECTED_ROLES = [
    "QA & Automation Lead",
    "Test Automation Engineer",
    "Full-Stack Engineer",
    "API Testing Specialist",
    "Test Strategy Owner",
]


@pytest.mark.smoke
def test_hero_heading(site):
    site.go_to_section("hero")
    assert site.hero_heading() == "Mark Custard"


def test_hero_cycles_through_every_role(site):
    assert site.hero_typed_items() == EXPECTED_ROLES


def test_typed_element_renders_a_role(site):
    """Typed.js clears and retypes the span continuously, so assert that it is
    rendering one of the roles rather than equal to any single one."""
    site.go_to_section("hero")
    typed = site.reveal_one(HomePage.HERO_TYPED)
    site.wait_until(
        lambda: len(site.text_of(typed)) > 0,
        message="Typed.js never rendered a role into the hero",
    )
    assert site.text_of(typed) in " ".join(EXPECTED_ROLES)
