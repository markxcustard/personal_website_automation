"""Page object for the single-page portfolio at https://markcustard.com/."""

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class HomePage(BasePage):
    TITLE = "Mark Custard - QA & Automation Engineering Lead"

    # Every section the navigation menu links to, in menu order.
    SECTIONS = (
        "hero",
        "about",
        "resume",
        "portfolio",
        "technical-skills",
        "skills",
        "testimonials",
        "contact",
    )

    # ------------------------------------------------------------------ header
    HEADER = (By.ID, "header")
    SITENAME = (By.CSS_SELECTOR, "#header .sitename")
    PROFILE_IMAGE = (By.CSS_SELECTOR, "#header .profile-img img")
    HEADER_TOGGLE = (By.CSS_SELECTOR, ".header-toggle")
    HEADER_SOCIAL_LINKS = (By.CSS_SELECTOR, "#header .social-links a")
    NAV = (By.ID, "navmenu")
    NAV_LINKS = (By.CSS_SELECTOR, "#navmenu ul li a")
    ACTIVE_NAV_LINK = (By.CSS_SELECTOR, "#navmenu ul li a.active")

    # -------------------------------------------------------------------- hero
    HERO_HEADING = (By.CSS_SELECTOR, "#hero h2")
    HERO_TYPED = (By.CSS_SELECTOR, "#hero .typed")

    # ------------------------------------------------------------------- about
    ABOUT_HEADLINE = (By.CSS_SELECTOR, "#about .content h2")
    ABOUT_FACTS = (By.CSS_SELECTOR, "#about .content ul li")

    # ------------------------------------------------------------------ resume
    RESUME_TITLES = (By.CSS_SELECTOR, "#resume .resume-title")
    RESUME_ITEMS = (By.CSS_SELECTOR, "#resume .resume-item")
    RESUME_ITEM_HEADINGS = (By.CSS_SELECTOR, "#resume .resume-item h4")
    RESUME_DOWNLOAD = (By.CSS_SELECTOR, "#resume a.btn-download-resume")

    # --------------------------------------------------------------- portfolio
    PORTFOLIO_FILTERS = (By.CSS_SELECTOR, "#portfolio .portfolio-filters li")
    ACTIVE_FILTER = (By.CSS_SELECTOR, "#portfolio .portfolio-filters li.filter-active")
    PORTFOLIO_ITEMS = (By.CSS_SELECTOR, "#portfolio .portfolio-item")
    PORTFOLIO_CARDS = (By.CSS_SELECTOR, "#portfolio .portfolio-card")
    PORTFOLIO_GITHUB_LINKS = (By.CSS_SELECTOR, "#portfolio a.github-link")

    # -------------------------------------------------------- technical skills
    SERVICE_ITEMS = (By.CSS_SELECTOR, "#technical-skills .service-item")

    # ------------------------------------------------------------------ skills
    SKILL_ROWS = (By.CSS_SELECTOR, "#skills .progress")

    # ------------------------------------------------------------ testimonials
    TESTIMONIAL_ITEMS = (By.CSS_SELECTOR, "#testimonials .testimonial-item")
    TESTIMONIAL_SLIDES = (By.CSS_SELECTOR, "#testimonials .swiper-slide")
    TESTIMONIAL_BULLETS = (By.CSS_SELECTOR, "#testimonials .swiper-pagination-bullet")
    ACTIVE_TESTIMONIAL = (
        By.CSS_SELECTOR,
        "#testimonials .swiper-slide-active .testimonial-item h3",
    )

    # ----------------------------------------------------------------- contact
    CONTACT_INFO_ITEMS = (By.CSS_SELECTOR, "#contact .info-item")
    CONTACT_FORM = (By.CSS_SELECTOR, "#contact form")
    FIELD_NAME = (By.ID, "name-field")
    FIELD_EMAIL = (By.ID, "email-field")
    FIELD_SUBJECT = (By.ID, "subject-field")
    FIELD_MESSAGE = (By.ID, "message-field")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#contact form button[type='submit']")

    # ------------------------------------------------------------------ footer
    FOOTER = (By.ID, "footer")

    # ================================================================ navigation
    def open(self):
        self.driver.get(self.base_url)
        # The portfolio grid is the last thing Isotope lays out, so its presence
        # is a reliable signal that the page's JavaScript has run.
        self.wait_present(self.PORTFOLIO_ITEMS)
        return self

    def nav_link(self, section):
        return self.find((By.CSS_SELECTOR, f"#navmenu a[href='#{section}']"))

    def nav_labels(self):
        return [self.text_of(link) for link in self.reveal(self.NAV_LINKS)]

    def nav_targets(self):
        return [
            link.get_attribute("href").split("#")[-1]
            for link in self.find_all(self.NAV_LINKS)
        ]

    def go_to_section(self, section):
        self.js_click(self.nav_link(section))
        self.wait_visible((By.ID, section))
        self.wait_for_scroll_to_settle()
        return self

    def active_nav_section(self):
        link = self.wait_visible(self.ACTIVE_NAV_LINK)
        return link.get_attribute("href").split("#")[-1]

    def section(self, section):
        return self.reveal_one((By.ID, section))

    def section_heading(self, section):
        return self.text_of((By.CSS_SELECTOR, f"#{section} .section-title h2"))

    # ====================================================================== hero
    def hero_heading(self):
        return self.text_of(self.reveal_one(self.HERO_HEADING))

    def hero_typed_items(self):
        typed = self.wait_present(self.HERO_TYPED)
        return [
            item.strip()
            for item in typed.get_attribute("data-typed-items").split(",")
        ]

    # ===================================================================== about
    def about_headline(self):
        return self.text_of(self.reveal_one(self.ABOUT_HEADLINE))

    def about_facts(self):
        """The two-column fact list, as ``{"Degree": "Bachelor of Laws (LLB)", ...}``."""
        return self.driver.execute_script(
            """
            const out = {};
            document.querySelectorAll(arguments[0]).forEach(li => {
              const label = li.querySelector('strong');
              const value = li.querySelector('span');
              if (label && value) {
                out[label.textContent.trim().replace(/:$/, '')] = value.textContent.trim();
              }
            });
            return out;
            """,
            self.ABOUT_FACTS[1],
        )

    # ==================================================================== resume
    def resume_titles(self):
        """Visible column headings; the duplicate right-hand one is aria-hidden."""
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll(arguments[0]))
              .filter(e => e.getAttribute('aria-hidden') !== 'true')
              .map(e => e.textContent.trim());
            """,
            self.RESUME_TITLES[1],
        )

    def resume_item_headings(self):
        return self.texts_of(self.RESUME_ITEM_HEADINGS)

    def resume_download_link(self):
        return self.reveal_one(self.RESUME_DOWNLOAD)

    # ================================================================= portfolio
    def open_portfolio(self):
        """Go to the portfolio and let AOS finish revealing the grid."""
        self.go_to_section("portfolio")
        self.reveal(self.PORTFOLIO_FILTERS)
        self.reveal(self.PORTFOLIO_ITEMS)
        return self

    def portfolio_filter_labels(self):
        return [self.text_of(f) for f in self.reveal(self.PORTFOLIO_FILTERS)]

    def portfolio_cards(self):
        """Every card's title, tags and GitHub URL, in DOM order."""
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#portfolio .portfolio-item')).map(item => ({
              title: item.querySelector('.portfolio-card-header h3').textContent.trim(),
              tags: Array.from(item.querySelectorAll('.portfolio-tags .tag')).map(t => t.textContent.trim()),
              description: item.querySelector('.portfolio-card-body p').textContent.trim(),
              url: item.querySelector('a.github-link').href,
              filter: Array.from(item.classList).find(c => c.startsWith('filter-')),
            }));
            """
        )

    def visible_portfolio_titles(self):
        return [
            self.text_of(card.find_element(By.TAG_NAME, "h3"))
            for card in self.find_all(self.PORTFOLIO_CARDS)
            if card.is_displayed()
        ]

    def filter_portfolio(self, label, expected_count):
        """Click a filter chip and wait for Isotope to settle on ``expected_count`` cards."""
        chip = next(
            f for f in self.reveal(self.PORTFOLIO_FILTERS) if self.text_of(f) == label
        )
        self.js_click(chip)
        self.wait_until(
            lambda: len(self.visible_portfolio_titles()) == expected_count,
            message=(
                f"Filter {label!r} settled on "
                f"{len(self.visible_portfolio_titles())} cards, expected {expected_count}"
            ),
        )
        return self

    def portfolio_link_labels(self):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll('#portfolio a.github-link'))"
            ".map(a => a.getAttribute('aria-label'));"
        )

    def portfolio_heading_levels(self):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll('#portfolio h1,#portfolio h2,"
            "#portfolio h3,#portfolio h4,#portfolio h5,#portfolio h6'))"
            ".map(h => h.tagName);"
        )

    def filter_chip_a11y(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#portfolio .portfolio-filters li')).map(l => ({
              label: l.textContent.trim(),
              tabindex: l.tabIndex,
              role: l.getAttribute('role'),
              pressed: l.getAttribute('aria-pressed'),
            }));
            """
        )

    def active_filter_label(self):
        return self.text_of(self.find(self.ACTIVE_FILTER))

    # ======================================================== technical skills
    def technical_skill_groups(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#technical-skills .service-item')).map(i => ({
              title: i.querySelector('h4.title').textContent.trim(),
              description: i.querySelector('p.description').textContent.trim(),
            }));
            """
        )

    # ==================================================================== skills
    def skills(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#skills .progress')).map(row => ({
              name: row.querySelector('.skill > span').textContent.trim(),
              label: row.querySelector('.skill .val').textContent.trim(),
              value: Number(row.querySelector('.progress-bar').getAttribute('aria-valuenow')),
            }));
            """
        )

    # ============================================================== testimonials
    def testimonials(self):
        """All testimonials, read via ``textContent``.

        Swiper only renders the active slides, so anything else would come back
        blank from ``.text``.
        """
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#testimonials .testimonial-item')).map(t => ({
              name: t.querySelector('h3').textContent.trim(),
              role: t.querySelector('h4').textContent.trim(),
              linkedin: t.querySelector('h3 a') ? t.querySelector('h3 a').href : null,
              quote: t.querySelector('p').textContent.trim(),
            }));
            """
        )

    def active_testimonial_name(self):
        return self.text_of(self.find(self.ACTIVE_TESTIMONIAL))

    def show_testimonial(self, index):
        bullets = self.find_all(self.TESTIMONIAL_BULLETS)
        current = self.active_testimonial_name()
        self.js_click(bullets[index])
        self.wait_until(
            lambda: self.active_testimonial_name() != current,
            message="Swiper never advanced to the requested slide",
        )
        return self.active_testimonial_name()

    # =================================================================== contact
    def contact_info(self):
        """Info blocks in DOM order.

        Returned as a list, not a dict: ChromeDriver serialises JS objects with
        their keys alphabetised, which silently destroys document order.
        """
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#contact .info-item')).map(i => ({
              heading: i.querySelector('h3').textContent.trim(),
              lines: Array.from(i.querySelectorAll('p')).map(p => p.textContent.trim()),
            }));
            """
        )

    def contact_info_map(self):
        return {block["heading"]: block["lines"] for block in self.contact_info()}

    def contact_info_headings(self):
        return [block["heading"] for block in self.contact_info()]

    def contact_form(self):
        return self.reveal_one(self.CONTACT_FORM)

    def form_action(self):
        return self.find(self.CONTACT_FORM).get_attribute("action")

    def required_field_names(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#contact form [required]'))
              .map(f => f.getAttribute('name'));
            """
        )

    def form_is_valid(self):
        """Ask the browser, without posting anything to the form's endpoint."""
        return self.driver.execute_script(
            "return document.querySelector('#contact form').checkValidity();"
        )
