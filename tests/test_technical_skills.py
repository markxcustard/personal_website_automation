"""Technical Skills section."""

import pytest

EXPECTED_GROUPS = [
    "Programming Languages",
    "Testing Tools",
    "Types of Testing",
    "Test Practices & Methodologies",
    "Frameworks & Libraries",
    "Project Management & Agile",
    "Version Control & CI/CD",
    "Cloud & Databases",
    "Developer Tools & Integrations",
    "Platform Testing",
]

# Tools worth failing a build over if a redesign quietly drops them.
KEY_TOOLS = [
    ("Programming Languages", "Python"),
    ("Programming Languages", "TypeScript"),
    ("Testing Tools", "Playwright"),
    ("Testing Tools", "pytest"),
    ("Testing Tools", "Selenium"),
    ("Frameworks & Libraries", "Behave"),
    ("Test Practices & Methodologies", "Page Object Model (POM)"),
    ("Version Control & CI/CD", "GitHub Actions"),
]


@pytest.fixture(scope="module")
def groups(site):
    site.go_to_section("technical-skills")
    return {g["title"]: g["description"] for g in site.technical_skill_groups()}


def test_every_group_is_listed(groups):
    assert list(groups) == EXPECTED_GROUPS


@pytest.mark.parametrize("title", EXPECTED_GROUPS)
def test_group_has_a_description(groups, title):
    assert groups[title].strip(), f"{title} has no description"


@pytest.mark.parametrize("title, tool", KEY_TOOLS)
def test_group_mentions_key_tool(groups, title, tool):
    assert tool in groups[title]
