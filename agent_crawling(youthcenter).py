# 웹사이트(온통청년) 스크래핑
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import pandas as pd  # pandas, openpyxl
from datetime import datetime
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


for page_num in range(1, 293):

    page_url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex={}".format(
        page_num
    )

    # Navigate to page
    driver.get(page_url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.result-list > li"))
    )

    # Loop through items on the page
    for i in range(1, 13):
        try:
            # Locate each card
            item = driver.find_element(
                By.CSS_SELECTOR,
                f"ul.result-list > li:nth-child({i}) > div.result-card-box",
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


print(["온통청년-청년정책 데이터 저장 완료"])


## 엑셀 저장
# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Include the current date and time in the Excel file name
excel_name = f"온통청년_청년정책_{current_datetime}"


# Define column names
columns = ["사업명", "주관기관명", "지원분야", "사업내용(요약)"]

# Create DataFrame with column names
data_frame = pd.DataFrame(results, columns=columns)


# Save to Excel
data_frame.to_excel(
    f"{excel_name}.xlsx",
    sheet_name=f"{excel_name}",
    startrow=0,
    header=True,
    index=False,
)

# Quit the driver
driver.quit()
