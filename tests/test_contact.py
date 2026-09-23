"""Contact section.

The form posts to a live Formspree endpoint, so nothing here ever submits it
with valid data — that would deliver a real email on every test run. The
validation tests either ask the browser directly via ``checkValidity()`` or
submit the form *empty*, which the browser blocks before any request is sent.
"""

import pytest

from page_objects.home_page import HomePage

EXPECTED_INFO = {
    "Address": ["Ridgefield, Washington, 98642"],
    "Call Me": ["🇺🇸 +1 (360) 771-0564", "🇬🇧 +44 7441 343276"],
    "Email Me": ["mark.a.custard@gmail.com"],
    "LinkedIn": ["linkedin.com/in/mark-custard"],
    "GitHub": ["github.com/markxcustard"],
}

FORM_FIELDS = ["name", "email", "subject", "message"]
FORM_ENDPOINT = "https://formspree.io/f/mpwkzpjv"


@pytest.fixture(scope="module")
def details(site):
    site.go_to_section("contact")
    site.contact_form()
    return {
        "headings": site.contact_info_headings(),
        "info": site.contact_info_map(),
        "action": site.form_action(),
        "required": site.required_field_names(),
        "submit_label": site.text_of(site.wait_visible(HomePage.SUBMIT_BUTTON)),
        "email_type": site.find(HomePage.FIELD_EMAIL).get_attribute("type"),
        "link_hrefs": [
            a.get_attribute("href")
            for item in site.find_all(HomePage.CONTACT_INFO_ITEMS)
            for a in item.find_elements("css selector", "a")
        ],
    }


@pytest.fixture
def contact(home):
    home.go_to_section("contact")
    home.contact_form()
    return home


def test_info_blocks_are_listed_in_order(details):
    assert details["headings"] == list(EXPECTED_INFO)


@pytest.mark.parametrize("heading, lines", sorted(EXPECTED_INFO.items()))
def test_info_block_contents(details, heading, lines):
    assert details["info"][heading] == lines


@pytest.mark.smoke
def test_both_phone_numbers_are_shown(details):
    numbers = details["info"]["Call Me"]
    assert any("+1 (360) 771-0564" in n for n in numbers)
    assert any("+44 7441 343276" in n for n in numbers)


def test_linkedin_and_github_are_real_links(details):
    assert "https://www.linkedin.com/in/mark-custard/" in details["link_hrefs"]
    assert "https://github.com/markxcustard" in details["link_hrefs"]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "locator",
    [
        HomePage.FIELD_NAME,
        HomePage.FIELD_EMAIL,
        HomePage.FIELD_SUBJECT,
        HomePage.FIELD_MESSAGE,
    ],
    ids=FORM_FIELDS,
)
def test_form_field_is_present(contact, locator):
    assert contact.wait_visible(locator).is_displayed()


@pytest.mark.smoke
def test_submit_button_label(details):
    # CSS uppercases the button, so compare the source text, not the rendered text.
    assert details["submit_label"] == "Send Message"


def test_every_field_is_required(details):
    assert sorted(details["required"]) == sorted(FORM_FIELDS)


def test_email_field_uses_the_email_type(details):
    assert details["email_type"] == "email"


def test_form_posts_to_the_expected_endpoint(details):
    assert details["action"] == FORM_ENDPOINT


def test_empty_form_is_invalid(contact):
    assert contact.form_is_valid() is False


def test_submitting_an_empty_form_does_not_leave_the_page(contact):
    """Browser-side validation should stop the POST before it is sent."""
    url_before = contact.driver.current_url
    contact.js_click(contact.find(HomePage.SUBMIT_BUTTON))
    assert contact.driver.current_url == url_before
    assert contact.form_is_valid() is False


def test_a_malformed_email_keeps_the_form_invalid(contact):
    """Fills every field in, but never submits."""
    contact.find(HomePage.FIELD_NAME).send_keys("Test Runner")
    contact.find(HomePage.FIELD_EMAIL).send_keys("not-an-email")
    contact.find(HomePage.FIELD_SUBJECT).send_keys("Automated check")
    contact.find(HomePage.FIELD_MESSAGE).send_keys("Validation only — not submitted.")
    assert contact.form_is_valid() is False
    assert contact.driver.execute_script(
        "return arguments[0].validity.typeMismatch;",
        contact.find(HomePage.FIELD_EMAIL),
    ) is True


def test_a_well_formed_entry_satisfies_validation(contact):
    """Confirms the form *would* be submittable, without submitting it."""
    contact.find(HomePage.FIELD_NAME).send_keys("Test Runner")
    contact.find(HomePage.FIELD_EMAIL).send_keys("runner@example.com")
    contact.find(HomePage.FIELD_SUBJECT).send_keys("Automated check")
    contact.find(HomePage.FIELD_MESSAGE).send_keys("Validation only — not submitted.")
    assert contact.form_is_valid() is True
    # Deliberately no submit: the endpoint delivers real email.
