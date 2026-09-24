"""Hero banner."""

import pytest

from page_objects.home_page import HomePage

# The article lives inside each item, so "an API Testing Specialist" is
# possible. With "I'm a" fixed in the markup it read "I'm a API ...".
EXPECTED_ROLES = [
    "a QA & Automation Lead",
    "a Test Automation Engineer",
    "a Full-Stack Engineer",
    "an API Testing Specialist",
    "a Test Strategy Owner",
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


def test_every_role_is_correctly_articled(site):
    """Each item supplies its own article, so a vowel-initial role reads
    "an" rather than "a"."""
    for role in site.hero_typed_items():
        assert role.startswith("a ") or role.startswith("an "), role
    assert "an API Testing Specialist" in site.hero_typed_items()


def test_the_rendered_line_has_no_double_space(site):
    """Regression guard: main.js split the items on ',' without trimming, so
    every role after the first rendered as "I'm a  Test Automation Engineer"
    with two spaces, and the accent underline began on the space."""
    site.go_to_section("hero")
    site.reveal_one(HomePage.HERO_TYPED)

    captured = {}

    def a_complete_role_is_showing():
        snapshot = site.hero_snapshot()
        if snapshot["role"] in EXPECTED_ROLES:
            captured.update(snapshot)
            return True
        return False

    site.wait_until(
        a_complete_role_is_showing,
        timeout=30,
        message="Typed.js never settled on a complete role",
    )

    assert "  " not in captured["line"], repr(captured["line"])
    assert captured["line"].startswith(f"I'm {captured['role']}")
