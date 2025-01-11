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

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 읽기
instagram_account = os.getenv("INSTAGRAM_ACCOUNT")
instagram_password = os.getenv("INSTAGRAM_PASSWORD")

print(instagram_account, instagram_password)

# Hardcoded list of Instagram accounts to scrape
INSTAGRAM_ACCOUNTS = [
    "millakindie",  # 민락인디트레이닝센터
    "jakdangso_busan",  # 청년작당소
    # "busan_dodream",  # 청년두드림센터
    # "cats_sasang_",  # 사상인디스테이션
    # "youthcenterbusan",  # 부산청년센터
    # "jobcafe.busan",  # 부산청년잡성장카페
    # Add more accounts here
]

# ChromeDriver setup
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
driver.maximize_window()


# Login to Instagram
def instagram_login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    username.send_keys("instagram_account")  # dotenv 사용하여 중요정보/환경변수 숨기기
    password.send_keys("instagram_password")  # dotenv 사용하여 중요정보/환경변수 숨기기
    password.send_keys(Keys.RETURN)
    time.sleep(8)  # Increase wait time for slow login


# Function to scrape a single Instagram account
def scrape_account(account):
    print(f"\n=== Starting scraping for account: {account} ===")
    account_data = []

    try:
        # Navigate to the target account
        driver.get(f"https://www.instagram.com/{account}/")
        time.sleep(5)

        # Ensure we're on the correct account page
        current_url = driver.current_url
        if account not in current_url:
            print(
                f"Navigation failed for account: {account}. Current URL: {current_url}"
            )
            return []

        # Process posts
        posts = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div._ac7v > div.x1lliihq")
            )
        )
        print(f"Found {len(posts)} posts.")

        for index, post in enumerate(posts):
            try:
                post_data = process_post(post)
                if post_data:
                    account_data.append(post_data)
            except Exception as e:
                print(f"Error processing post {index + 1}: {e}")

    except Exception as e:
        print(f"Error scraping account {account}: {e}")

    print(f"Finished scraping account: {account}, collected {len(account_data)} posts.")
    return account_data


# Function to process a single post
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
                (By.CSS_SELECTOR, "div.x9f619 > span.xt0psk2 > div > a.x1i10hfl")
            )
        )
        caption_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._a9zs > h1._ap3a"))
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
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x160vmok"))
            )
            close_button.click()
        except Exception as e:
            print(f"Error closing post: {e}")


# Main script
instagram_login()
all_data = []

for account in INSTAGRAM_ACCOUNTS:
    try:
        print(f"\nSwitching to account: {account}")
        account_data = scrape_account(account)
        # extend() : 두개의 리스트를 하나의 리스트로 만들 때 사용 -> 리스트.extend(리스트) 형태로 사용함
        all_data.extend(account_data)
    except Exception as e:
        print(f"Error handling account {account}: {e}")


# Save all data to Excel
if all_data:
    df = pd.DataFrame(all_data)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_excel(f"instagram_data_{current_datetime}.xlsx", index=False)
    print("Data saved to Excel successfully.")
else:
    print("No data to save.")

# Quit driver
driver.quit()
