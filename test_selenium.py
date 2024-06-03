from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Path to your Firefox binary
firefox_binary_path = "/Applications/Firefox.app/Contents/MacOS/firefox"

# Update the path to your WebDriver
driver_path = "/usr/local/bin/geckodriver"
service = Service(executable_path=driver_path)

# Set Firefox options
options = Options()
options.binary_location = firefox_binary_path

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox(service=service, options=options)

# Open a website
driver.get("https://markxcustard.github.io/")

# Print the title of the page
print(driver.title)

# Wait for 10 seconds
time.sleep(10)

# Close the browser
driver.quit()
