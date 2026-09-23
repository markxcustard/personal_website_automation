"""About section."""

import pytest

EXPECTED_FACTS = {
    "Degree": "Bachelor of Laws (LLB)",
    "GitHub": "github.com/markxcustard",
    "Phone": "(360) 771-0564",
    "City": "Ridgefield, Washington",
    "Experience": "7+ Years",
    "Specialization": "QA, Automation & Full-Stack",
    "Email": "mark.a.custard@gmail.com",
    "Freelance": "Available",
}


@pytest.fixture(scope="module")
def about(site):
    site.go_to_section("about")
    return {"headline": site.about_headline(), "facts": site.about_facts()}


@pytest.mark.smoke
def test_about_headline(about):
    assert about["headline"] == "QA & Automation Engineering Lead"


@pytest.mark.parametrize("label, value", sorted(EXPECTED_FACTS.items()))
def test_about_fact(about, label, value):
    assert about["facts"][label] == value


def test_about_lists_no_unexpected_facts(about):
    assert set(about["facts"]) == set(EXPECTED_FACTS)
