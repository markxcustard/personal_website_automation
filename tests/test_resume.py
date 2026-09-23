"""Resume section, including the PDF download."""

import os

import pytest

EXPECTED_COLUMN_TITLES = ["Summary", "Education", "Professional Experience"]

EXPECTED_ROLES = [
    "Lead Engineer, Full Stack & Quality",
    "QA Analyst — Manual | Automation",
    "Senior QA Engineer",
    "QA Analyst",
    "QA Engineer",
    "Software QA Analyst",
    "Junior Application Developer",
]

EXPECTED_EDUCATION = [
    "Web Development Certification",
    "Bachelor of Laws (LLB) in Business Law",
]

CURRENT_RESUME_PDF = "mark_custard_resume_09_2026.pdf"


@pytest.fixture(scope="module")
def resume(site):
    site.go_to_section("resume")
    link = site.resume_download_link()
    return {
        "titles": site.resume_titles(),
        "headings": site.resume_item_headings(),
        "href": link.get_attribute("href"),
        "download": link.get_attribute("download"),
    }


def test_resume_column_titles(resume):
    """The right-hand column repeats the heading for layout and is aria-hidden,
    so it should not show up as a fourth title."""
    assert resume["titles"] == EXPECTED_COLUMN_TITLES


@pytest.mark.parametrize("qualification", EXPECTED_EDUCATION)
def test_education_entry_is_listed(resume, qualification):
    assert qualification in resume["headings"]


@pytest.mark.parametrize("role", EXPECTED_ROLES)
def test_role_is_listed(resume, role):
    assert role in resume["headings"]


@pytest.mark.smoke
def test_download_link_points_at_the_current_resume(resume):
    assert resume["href"].endswith(CURRENT_RESUME_PDF)
    assert resume["download"] == "Mark_Custard_Resume.pdf"


def test_clicking_download_saves_the_pdf(home, download_dir, browser_name):
    if browser_name == "safari":
        pytest.skip("SafariDriver cannot be pointed at a custom download directory")

    home.go_to_section("resume")
    home.js_click(home.resume_download_link())

    home.wait_until(
        lambda: any(
            name.endswith(".pdf") for name in os.listdir(download_dir)
        ),
        timeout=30,
        message=f"No PDF appeared in {download_dir}",
    )
    saved = [n for n in os.listdir(download_dir) if n.endswith(".pdf")]
    assert saved, "resume PDF was not written to disk"
    assert os.path.getsize(os.path.join(download_dir, saved[0])) > 0
