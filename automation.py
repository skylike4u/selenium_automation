from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time


# Path to the chromedriver executable
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)

# Keep Chrome browser open after program finishes
chorome_options = webdriver.ChromeOptions()
chorome_options.add_experimental_option("detach", True)

# Initialize Chrome browser
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=service, options=chorome_options)


try:
    # Open Google
    driver.get("https://www.google.com")
    print("Page title is:", driver.title)
    assert "Python" in driver.title

    # Find the search box, enter a query, and submit
    search_box = driver.find_element(By.NAME, value="q")
    search_box.clear()
    search_box.send_keys("Selenium Python automation")
    search_box.send_keys(Keys.RETURN)

    assert "No results found." not in driver.page_source

    # Wait for results to load
    time.sleep(5)

    # Print current URL
    print("Current URL:", driver.current_url)
finally:
    # Close the browser
    driver.quit()
