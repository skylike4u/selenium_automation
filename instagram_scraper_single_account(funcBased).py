from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
instagram_account = os.getenv("INSTAGRAM_ACCOUNT")
instagram_password = os.getenv("INSTAGRAM_PASSWORD")

# ChromeDriver setup
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
driver.maximize_window()


# Login to Instagram
def instagram_login():
    print("\nLogging into Instagram...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    username.send_keys(instagram_account)
    password.send_keys(instagram_password)
    password.send_keys(Keys.RETURN)
    time.sleep(8)


# Process a single post
def process_post(post):
    try:
        post_url = post.get_attribute("href")
        if not post_url:
            post_url = driver.execute_script(
                "return arguments[0].getAttribute('href');", post
            )
        print(f"Post URL: {post_url}")

        post.click()
        time.sleep(3)

        id_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.xjp7ctv > div > a.x1i10hfl")
            )
        )
        caption_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.xt0psk2 > h1._ap3a"))
        )
        like_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.x1lliihq > a.x1i10hfl > span.x193iq5w")
            )
        )
        timeinfo_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "time.x1p4m5qa"))
        )

        return {
            "URL": post_url,
            "id": id_element.text,
            "Caption": caption_element.text,
            "Likes": like_element.text,
            "Datetime": timeinfo_element.text,
        }

    except Exception as e:
        print(f"Error processing post: {e}")
        return None

    finally:
        # Close post view
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x160vmok"))
            )
            close_button.click()
        except Exception as e:
            print(f"Error closing post: {e}")


# Main scraping logic
def scrape_account(target_account):
    print(f"\nScraping account: {target_account}")
    driver.get(f"https://www.instagram.com/{target_account}/")
    time.sleep(5)

    data = []

    try:
        posts = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div._ac7v > div.x1lliihq")
            )
        )
        print(f"Found {len(posts)} posts.")

        for index, post in enumerate(posts):
            post_data = process_post(post)
            if post_data:
                data.append(post_data)
    except Exception as e:
        print(f"Error scraping account: {e}")

    return data


# Main script
instagram_login()
target_account = "millakindie"
collected_data = scrape_account(target_account)

# Save collected data to Excel
if collected_data:
    df = pd.DataFrame(collected_data)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    excel_filename = f"{target_account}_data_{current_datetime}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Data saved to Excel: {excel_filename}")
else:
    print("No data collected.")

# Quit the driver
driver.quit()
