# sign-in automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time


url = "https://orteil.dashnet.org/experiments/cookie/"
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # 묵시적 대기
driver.maximize_window()  # 최대창

# 웹페이지 가져오기
driver.get(url)

# 쿠키 이미지 객체 가져오기
cookie = driver.find_element(By.ID, "cookie")

time.sleep(3)
# time.sleep(60*5)  # 5 minutes sleep

# 현재 시간을 time.time()을 사용하여 UTC 기준 초 단위로 반환
timeout = time.time() + 60 * 5  # 5 minutes from now

while True:
    if time.time() <= timeout:
        cookie.click()
        time.sleep(0.1)  # Wait 0.1 seconds between clicks
    else:
        break


time.sleep(5)

driver.quit()
