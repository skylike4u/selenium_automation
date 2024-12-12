from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import time

# 온통청년_청년정책검색url
# URL and ChromeDriver path
url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1"
chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # 묵시적 대기
driver.maximize_window()  # 최대창

results = []


# page_url = (
#     f"https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1"
# )

# Navigate to page
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.result-list > li"))
)

# Loop through items on the page
for i in range(1, 13):
    try:
        # Locate each card
        item = driver.find_element(
            By.CSS_SELECTOR, f"ul.result-list > li:nth-child({i}) > div.result-card-box"
        )
        # Extract details
        title = item.find_element(By.CSS_SELECTOR, ".tit-wrap").text
        organ_name = item.find_element(By.CSS_SELECTOR, ".organ-name").text
        support_field = item.find_element(By.CSS_SELECTOR, ".badge").text
        # Extract text from the <p> tag inside the <div class="cover"> using JavaScript
        description = driver.execute_script(
            "return arguments[0].textContent;",
            item.find_element(By.CSS_SELECTOR, ".cover > p"),
        )

        # Append results as a tuple
        results.append((title, organ_name, support_field, description))
    except Exception as e:
        print(f"Error with item {i}: {e}")

# Print results
pprint(results)

## 엑셀 저장
print(["온통청년-청년정책 데이터 저장완료"])
excel_name = "온통청년_청년정책"
import pandas as pd  # pandas, openpyxl

data_frame = pd.DataFrame(results)
data_frame.to_excel(
    "{}.xlsx".format(excel_name),
    sheet_name="{}".format(excel_name),
    startrow=0,
    header=True,
)

# Quit the driver
driver.quit()
