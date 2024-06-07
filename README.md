# Mark Custard's Portfolio Website

Welcome to the repository for Mark Custard's Portfolio Website. This repository contains the code for my personal portfolio website and the associated test cases.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Description

This repository hosts the source code for my personal portfolio website, which showcases my professional experience, skills, and projects. It is built using HTML, CSS, and JavaScript, and includes automated tests using Selenium and Pytest.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/markxcustard/portfolio-website.git
    cd portfolio-website
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

## Usage

To serve the website locally, you can use any static file server. Here is an example using Python's built-in HTTP server:

```bash
python -m http.server
Open your web browser and navigate to http://localhost:8000 to view the website.

Running Tests
The project includes automated tests to ensure that the website's functionality works as expected. These tests are written using Selenium and Pytest.

Setup for Running Tests
Install browser drivers:

Make sure you have the appropriate browser drivers installed (e.g., ChromeDriver for Google Chrome, GeckoDriver for Firefox).

Run the tests:

You can run all tests using the following command:

bash
Copy code
pytest tests/
To run a specific test class or method, use:

bash
Copy code
pytest tests/test_website.py::TestAboutMe
pytest tests/test_website.py::TestAboutMe::test_about_me_paragraph
Test Structure
The tests are organized into different classes based on the sections of the website:

TestNavigation: Tests for navigating between different sections of the website.
TestAboutMe: Tests for the "About Me" section, including verbiage, GitHub link, and resume download.
TestContact: Tests for the "Contact" section, including email, phone number, GitHub, and LinkedIn buttons.
TestPortfolio: Tests for the "Portfolio" section, including expanding portfolio items and verifying their content.
TestTestimonials: Tests for the "Testimonials" section, including verifying testimonial text.
