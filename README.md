# Portfolio Website Automated Tests

This repository contains the automated tests for Mark Custard's portfolio website. These tests ensure that the website's functionality works as expected.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Contributing](#contributing)
- [License](#license)

## Description

This project includes automated tests for the portfolio website. The tests are written using Selenium and Pytest and cover various sections of the website, such as "About Me," "Contact," "Portfolio," and "Testimonials."

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/markxcustard/portfolio-website-tests.git
    cd portfolio-website-tests
    ```

2. **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

### Setup for Running Tests

1. **Install browser drivers:**

    Make sure you have the appropriate browser drivers installed (e.g., ChromeDriver for Google Chrome, GeckoDriver for Firefox).

2. **Run the tests:**

    You can run all tests using the following command:

    ```bash
    pytest tests/
    ```

    To run a specific test class or method, use:

    ```bash
    pytest tests/test_website.py::TestAboutMe
    pytest tests/test_website.py::TestAboutMe::test_about_me_paragraph
    ```

## Test Structure

The tests are organized into different classes based on the sections of the website:

- `TestNavigation`: Tests for navigating between different sections of the website.
- `TestAboutMe`: Tests for the "About Me" section, including verbiage, GitHub link, and resume download.
- `TestContact`: Tests for the "Contact" section, including email, phone number, GitHub, and LinkedIn buttons.
- `TestPortfolio`: Tests for the "Portfolio" section, including expanding portfolio items and verifying their content.
- `TestTestimonials`: Tests for the "Testimonials" section, including verifying testimonial text.

### Example Tests

#### `TestAboutMe`

- **test_about_me_paragraph:** Verifies specific text in the "About Me" section.
- **test_github_link:** Checks that the GitHub link redirects to the correct URL.
- **test_resume_download:** Ensures that the resume can be downloaded.

#### `TestContact`

- **test_contact_details:** Verifies the email, phone number, GitHub, and LinkedIn buttons in the "Contact" section.

#### `TestPortfolio`

- **test_portfolio_expansion:** Tests expanding portfolio items and verifying their content.

#### `TestTestimonials`

- **test_testimonial_paragraph:** Verifies specific text in the "Testimonials" section.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
