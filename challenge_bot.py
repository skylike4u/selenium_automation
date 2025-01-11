# sign-in automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time


url = "https://secure-retreat-92358.herokuapp.com/"
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # 묵시적 대기
driver.maximize_window()  # 최대창


# 웹페이지 가져오기
driver.get(url)


first_name = driver.find_element(By.NAME, "fName")
first_name.send_keys("JH")
last_name = driver.find_element(By.NAME, "lName")
last_name.send_keys("Choi")
email = driver.find_element(By.NAME, "email")
email.send_keys("skylike4u@naver.com")

submit = driver.find_element(By.CSS_SELECTOR, "form button")
submit.click()

time.sleep(3)

# Quit the driver
driver.quit()
