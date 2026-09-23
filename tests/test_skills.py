"""Skills section progress bars."""

import pytest

EXPECTED_SKILLS = [
    ("Test Automation (Playwright, pytest, Vitest)", 95),
    ("Manual & Exploratory Testing", 95),
    ("Test Strategy & Coverage Design", 90),
    ("Python, JavaScript & SQL", 90),
    ("API & Integration Testing (Postman, ChaiJS)", 90),
    ("CI/CD & Release Gating (GitHub Actions, Azure DevOps)", 90),
    ("Salesforce & Data Validation", 85),
]


@pytest.fixture(scope="module")
def skills(site):
    site.go_to_section("skills")
    return site.skills()


def test_expected_skills_are_listed(skills):
    names = [s["name"] for s in skills]
    for expected, _ in EXPECTED_SKILLS:
        assert expected in names


@pytest.mark.parametrize("name, value", EXPECTED_SKILLS)
def test_skill_percentage(skills, name, value):
    skill = next(s for s in skills if s["name"] == name)
    assert skill["value"] == value
    assert skill["label"] == f"{value}%"


def test_percentages_are_in_range(skills):
    assert all(0 <= s["value"] <= 100 for s in skills)


def test_label_matches_aria_value(skills):
    """The visible percentage and the accessible one must not drift apart."""
    mismatched = [s["name"] for s in skills if s["label"] != f"{s['value']}%"]
    assert not mismatched, f"aria-valuenow disagrees with the label for: {mismatched}"
