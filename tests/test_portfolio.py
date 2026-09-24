"""Portfolio grid: cards, tags, GitHub links, Isotope filters and accessibility."""

import pytest

from page_objects.home_page import HomePage

EXPECTED_CARDS = [
    {
        "title": "Personal Website Automation",
        "filter": "filter-automation",
        "tags": ["Selenium", "pytest", "Page Objects"],
        "url": "https://github.com/markxcustard/personal_website_automation",
    },
    {
        "title": "BDD Personal Website",
        "filter": "filter-bdd",
        "tags": ["BDD", "Gherkin", "Behave"],
        "url": "https://github.com/markxcustard/bdd_personal_website",
    },
    {
        "title": "Cypress Portfolio Tests",
        "filter": "filter-automation",
        "tags": ["Cypress", "JavaScript", "E2E"],
        "url": "https://github.com/markxcustard/cypress_personal_website",
    },
    {
        "title": "Pandas Filtering Films",
        "filter": "filter-data",
        "tags": ["Python", "Pandas", "pytest"],
        "url": "https://github.com/markxcustard/pandas_filtering_films",
    },
    {
        "title": "Films CRUD",
        "filter": "filter-database",
        "tags": ["SQLAlchemy", "SQLite", "pytest"],
        "url": "https://github.com/markxcustard/database_crud",
    },
]

# (filter label, number of cards that should remain visible)
FILTERS = [("All", 5), ("Automation", 2), ("BDD", 1), ("Data", 1), ("Database", 1)]


@pytest.fixture
def portfolio(home):
    return home.open_portfolio()


@pytest.mark.smoke
def test_every_card_is_shown_by_default(portfolio):
    assert len(portfolio.visible_portfolio_titles()) == len(EXPECTED_CARDS)


def test_card_order(portfolio):
    titles = [card["title"] for card in portfolio.portfolio_cards()]
    assert titles == [card["title"] for card in EXPECTED_CARDS]


@pytest.mark.parametrize("expected", EXPECTED_CARDS, ids=lambda c: c["title"])
def test_card_contents(portfolio, expected):
    card = next(
        c for c in portfolio.portfolio_cards() if c["title"] == expected["title"]
    )
    assert card["tags"] == expected["tags"]
    assert card["filter"] == expected["filter"]
    assert card["description"], "card is missing its description"


@pytest.mark.smoke
@pytest.mark.parametrize("expected", EXPECTED_CARDS, ids=lambda c: c["title"])
def test_card_links_to_its_repository(portfolio, expected):
    card = next(
        c for c in portfolio.portfolio_cards() if c["title"] == expected["title"]
    )
    assert card["url"] == expected["url"]


def test_repository_links_open_in_a_new_tab(portfolio):
    for link in portfolio.reveal(HomePage.PORTFOLIO_GITHUB_LINKS):
        assert link.get_attribute("target") == "_blank"
        # Without noopener, the opened tab keeps a handle on window.opener.
        assert "noopener" in link.get_attribute("rel")


def test_filter_labels(portfolio):
    assert portfolio.portfolio_filter_labels() == [label for label, _ in FILTERS]


@pytest.mark.parametrize("label, visible", FILTERS)
def test_filter_narrows_the_grid(portfolio, label, visible):
    portfolio.filter_portfolio(label, visible)
    assert len(portfolio.visible_portfolio_titles()) == visible
    assert portfolio.active_filter_label() == label


@pytest.mark.parametrize(
    "label, titles",
    [
        ("Automation", ["Personal Website Automation", "Cypress Portfolio Tests"]),
        ("BDD", ["BDD Personal Website"]),
        ("Data", ["Pandas Filtering Films"]),
        ("Database", ["Films CRUD"]),
    ],
)
def test_filter_keeps_the_right_cards(portfolio, label, titles):
    portfolio.filter_portfolio(label, len(titles))
    assert sorted(portfolio.visible_portfolio_titles()) == sorted(titles)


def test_all_restores_the_full_grid(portfolio):
    portfolio.filter_portfolio("Automation", 2)
    portfolio.filter_portfolio("All", len(EXPECTED_CARDS))
    assert sorted(portfolio.visible_portfolio_titles()) == sorted(
        card["title"] for card in EXPECTED_CARDS
    )


class TestAccessibility:
    """The template shipped these filters as bare <li> elements with click
    handlers, so they could not be reached or operated by keyboard at all."""

    def test_every_filter_chip_is_focusable(self, portfolio):
        chips = portfolio.filter_chip_a11y()
        assert chips, "no filter chips found"
        assert all(chip["tabindex"] == 0 for chip in chips), chips

    def test_every_filter_chip_exposes_a_button_role(self, portfolio):
        assert all(c["role"] == "button" for c in portfolio.filter_chip_a11y())

    def test_only_the_active_filter_is_pressed(self, portfolio):
        chips = portfolio.filter_chip_a11y()
        assert [c["pressed"] for c in chips] == ["true", "false", "false", "false", "false"]

    def test_activating_a_filter_moves_aria_pressed(self, portfolio):
        portfolio.filter_portfolio("BDD", 1)
        pressed = {c["label"]: c["pressed"] for c in portfolio.filter_chip_a11y()}
        assert pressed["BDD"] == "true"
        assert pressed["All"] == "false"

    def test_each_repository_link_has_a_distinct_accessible_name(self, portfolio):
        """All five links read 'View on GitHub', so without aria-label a screen
        reader announces the same name five times."""
        labels = portfolio.portfolio_link_labels()
        assert all(labels), f"a link is missing aria-label: {labels}"
        assert len(set(labels)) == len(EXPECTED_CARDS)

    @pytest.mark.parametrize("expected", EXPECTED_CARDS, ids=lambda c: c["title"])
    def test_link_label_names_its_project(self, portfolio, expected):
        assert (
            f"View {expected['title']} on GitHub" in portfolio.portfolio_link_labels()
        )

    def test_heading_levels_do_not_skip(self, portfolio):
        """Section heading is h2, so the cards must be h3, not h4."""
        levels = portfolio.portfolio_heading_levels()
        assert levels[0] == "H2"
        assert set(levels[1:]) == {"H3"}
