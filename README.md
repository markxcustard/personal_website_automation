# Portfolio Website Automation (Selenium + pytest)

End-to-end UI tests for [markcustard.com](https://markcustard.com/) — my portfolio
site — written with Selenium WebDriver, pytest and the Page Object Model.

140 tests covering navigation, the resume section and its PDF download, the
Isotope-filtered portfolio grid, technical skills, skill percentages, the
testimonials carousel, the contact form's validation, and the mobile
off-canvas sidebar.

## Why this suite looks the way it does

The site is a single page built on an animated Bootstrap template, which makes a
few things non-obvious. Each one is handled in the page objects rather than
sprinkled through the tests:

| Behaviour | How it's handled |
| --- | --- |
| **AOS reveal animations** — elements exist in the DOM but report `is_displayed() == False` and empty `.text` until scrolled to | `BasePage.reveal()` scrolls each match into view and waits for it to render |
| **`scroll-behavior: smooth`** — a nav click starts an animation that outlives the click, and scrollspy only sets the active menu item once it lands | `BasePage.wait_for_scroll_to_settle()` polls `window.scrollY` until it stops changing |
| **`text-transform: uppercase`** — `.text` returns `"AUTOMATION"` where the markup says `"Automation"` | `BasePage.text_of()` reads `textContent` instead |
| **Swiper carousel** — only the active slides are rendered, so off-screen testimonials come back blank | Testimonials are read via `textContent` for all five slides |
| **ChromeDriver key ordering** — a JS object returned from `execute_script` comes back with its keys alphabetised, silently destroying document order | Anything order-sensitive returns an **array**, not an object |
| **Isotope filtering** — cards animate in and out | `filter_portfolio()` waits for the grid to settle on the expected count |

## The contact form is never submitted

The form posts to a live Formspree endpoint, so submitting it with valid data
would deliver a real email on every run. The validation tests instead ask the
browser via `checkValidity()`, or submit the form **empty** so browser-side
validation blocks the request. `test_a_well_formed_entry_satisfies_validation`
confirms a good entry *would* pass, and stops there.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

No driver binaries to install: Selenium Manager (built into Selenium 4.6+)
resolves chromedriver and geckodriver automatically.

## Running

```bash
pytest                                   # Chrome, visible
pytest --headless                        # Chrome, headless
pytest --headless --browser=firefox      # Firefox
pytest --headless -m smoke               # 16 checks, ~20s
pytest --headless -m responsive          # mobile viewport only
pytest --headless --base-url=http://localhost:8000/
pytest --headless --html=report.html --self-contained-html
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--base-url` | `https://markcustard.com/` | Point the suite at a local or staging copy |
| `--browser` | `chrome` | `chrome`, `firefox` or `safari` |
| `--headless` | off | Ignored for Safari, which has no headless mode |

A full Chrome run takes roughly 90 seconds.

## Layout

```
conftest.py                     CLI options, driver and page fixtures
page_objects/base_page.py       waits, scroll/reveal helpers, textContent reads
page_objects/home_page.py       locators and accessors for every section
tests/test_navigation.py        menu, section headings, scrollspy, footer
tests/test_hero.py              hero heading and typed role rotation
tests/test_about.py             headline and the fact list
tests/test_resume.py            roles, education, PDF download
tests/test_portfolio.py         cards, tags, repo links, Isotope filters
tests/test_technical_skills.py  the ten skill groups
tests/test_skills.py            percentages vs aria-valuenow
tests/test_testimonials.py      carousel contents and pagination
tests/test_contact.py           info blocks and form validation
tests/test_responsive.py        off-canvas sidebar, toggle state, no overflow
```

### Fixture scope

Read-only assertions share one page load via the session-scoped `site` fixture,
with each module caching what it scrapes. Anything that clicks, types or resizes
takes `home` instead, which loads the page fresh. That split cut the full run
from just over three minutes to about ninety seconds.

## CI

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs the suite
against Chrome and Firefox on every push and pull request, and nightly at 07:00
UTC — the tests target the deployed site, so a scheduled run catches content
drift even when this repository hasn't changed. An HTML report is uploaded as an
artifact for each browser.

## License

[MIT](LICENSE)
