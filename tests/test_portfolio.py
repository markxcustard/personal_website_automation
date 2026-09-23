"""Portfolio grid: cards, tags, GitHub links and the Isotope filters."""

import pytest

EXPECTED_CARDS = [
    {
        "title": "Personal Website Automation",
        "filter": "filter-automation",
        "tags": ["Selenium", "Python", "Automation"],
        "url": "https://github.com/markxcustard/personal_website_automation",
    },
    {
        "title": "BDD Personal Website",
        "filter": "filter-bdd",
        "tags": ["BDD", "Gherkin", "Selenium"],
        "url": "https://github.com/markxcustard/bdd_personal_website",
    },
    {
        "title": "Pandas Filtering Films",
        "filter": "filter-data",
        "tags": ["Python", "Pandas", "Data Analysis"],
        "url": "https://github.com/markxcustard/pandas_filtering_films",
    },
    {
        "title": "Films CRUD API",
        "filter": "filter-api",
        "tags": ["API", "SQLAlchemy", "SQLite"],
        "url": "https://github.com/markxcustard/database_crud",
    },
]

# (filter label, number of cards that should remain visible)
FILTERS = [("All", 4), ("Automation", 1), ("BDD", 1), ("API", 1), ("Data", 1)]


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
    from page_objects.home_page import HomePage

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
    "label, title",
    [
        ("Automation", "Personal Website Automation"),
        ("BDD", "BDD Personal Website"),
        ("Data", "Pandas Filtering Films"),
        ("API", "Films CRUD API"),
    ],
)
def test_filter_keeps_the_right_card(portfolio, label, title):
    portfolio.filter_portfolio(label, 1)
    assert portfolio.visible_portfolio_titles() == [title]


def test_all_restores_the_full_grid(portfolio):
    portfolio.filter_portfolio("Automation", 1)
    portfolio.filter_portfolio("All", 4)
    assert sorted(portfolio.visible_portfolio_titles()) == sorted(
        card["title"] for card in EXPECTED_CARDS
    )
