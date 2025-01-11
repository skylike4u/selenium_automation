from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
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


# ChromeDriver 설정
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
driver.maximize_window()

# Instagram 로그인
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)
username = driver.find_element(By.NAME, "username")
password = driver.find_element(By.NAME, "password")
username.send_keys(instagram_account)
password.send_keys(instagram_password)
password.send_keys(Keys.RETURN)
time.sleep(8)  # 5에서 8로 변경

# 타겟 계정으로 이동
driver.get("https://www.instagram.com/millakindie/")
time.sleep(5)

data = []

# 첫 번째 줄의 3개 포스트 처리 (스크롤 전에 첫 번째 줄의 포스트를 명시적으로 처리)
try:
    first_row_posts = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div._ac7v > div.x1lliihq")
        )
    )
    print(f"Found {len(first_row_posts)} posts in the first row.")

    for index, post in enumerate(first_row_posts[:3]):  # 첫 번째 줄의 3개 포스트만 처리
        try:
            post_url = post.get_attribute("href")
            if not post_url:
                post_url = driver.execute_script(
                    "return arguments[0].getAttribute('href');", post
                )
            print(f"Post {index + 1} URL: {post_url}")

            post.click()
            time.sleep(3)  # 포스트 로드 대기

            # contents elements 추출
            try:
                id_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "span.xjp7ctv > div > a.x1i10hfl",
                        )
                    )
                )
                caption_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.xt0psk2 > h1._ap3a")
                    )
                )

                like_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span.x1lliihq > a.x1i10hfl > span.x193iq5w")
                    )
                )

                timeinfo_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "time.x1p4m5qa"))
                )

                id_info = id_element.text
                caption = caption_element.text
                likes = like_element.text
                timeinfo = timeinfo_element.text

                # 데이터 추가
                data.append(
                    {
                        "URL": post_url,
                        "id": id_info,
                        "Caption": caption,
                        "Likes": likes,
                        "Datetime": timeinfo,
                    }
                )
                print(f"Post {index + 1} data: {data[-1]}")

            except Exception as e:
                print(f"Error extracting caption for post {index + 1}: {e}")
                caption = "No Caption"

            # 닫기 버튼 처리
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x160vmok"))
            )
            close_button.click()

        except Exception as e:
            print(f"Error processing first-row post {index + 1}: {e}")

except Exception as e:
    print(f"Error locating first-row posts: {e}")


# 스크롤 및 나머지 포스트 처리
for _ in range(3):  # 스크롤 반복 횟수
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


# (두번째 줄-4번째 포스트부터) 나머지 포스트 처리
# (요렇게 변수 정의 해도 됨) posts = driver.find_elements(By.CSS_SELECTOR, "div._ac7v > div.x1lliihq")
posts = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._ac7v > div.x1lliihq"))
)
print(f"Total posts found: {len(posts)}")


# 첫 번째 줄 이후의 포스트만 처리하면 - for index, post in enumerate(posts[3:], start=4): 로 slicing 후에 arguments를 넣어야되나, 인스타그램 로딩문제로 첫줄이 안나와서 아래와 같이 코딩
for index, post in enumerate(posts):
    try:
        post_url = post.get_attribute("href")
        if not post_url:
            post_url = driver.execute_script(
                "return arguments[0].getAttribute('href');", post
            )

        print(f"Post {index} URL: {post_url}")
        post.click()
        time.sleep(3)

        # contents elements 추출
        id_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "span.xjp7ctv > div > a.x1i10hfl",
                )
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

        # text 추출
        id_info = id_element.text
        caption = caption_element.text
        likes = like_element.text
        timeinfo = timeinfo_element.text
        # tag_id = tag_id_element.text

        # 데이터 추가 (더 추가 할 것)
        data.append(
            {
                "URL": post_url,
                "id": id_info,
                "Caption": caption,
                "Likes": likes,
                "Datetime": timeinfo,
            }
        )
        print(f"Post {index} data: {data[-1]}")

    except Exception as e:
        print(f"Error on post {index}: {e}")

    finally:
        # 닫기 버튼 처리
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x160vmok"))
            )
            close_button.click()
        except Exception as e:
            print(f"Error clicking close button: {e}")

# 루프 후 데이터 확인
print(f"Collected data: {data}")


# 날짜 포매팅 (날짜 및 시간 데이터는 strtime을 통해 다룰 수 있음)
current_datetime = datetime.now()
# formatted_now = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# 데이터 엑셀로 저장
if data:
    df = pd.DataFrame(data)
    df.to_excel("{}_data.xlsx".format(id_info), index=False)
    print("Data saved to Excel successfully.")
else:
    print("No data to save.")


print("Scraping complete. Data saved to {}_data.xlsx.".format(id_info))

# 드라이버 종료
driver.quit()
