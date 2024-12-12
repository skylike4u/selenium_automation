# image_crawling
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import urlretrieve  # 다운로드

# from tqdm import tqdm

# 데이터가 많으면 pprint로 출력하면 좀 더 편하다
# from pprint import pprint


# 네이버 고슴도치 검색url
keyword = input("수집할 이미지 : ")
url = "https://search.naver.com/search.naver?ssc=tab.image.all&where=image&query={}".format(
    keyword
)

chromedriver_path = r"C:\Users\SAMSUNG\selenium\chromedriver.exe"
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # 묵시적 대기, 활성화를 최대 5초까지 기다린다.
driver.maximize_window()  # 최대창

# 웹페이지 가져오기
driver.get(url)

# scroll down(스크롤 다운)
body = driver.find_element(By.TAG_NAME, "body")  # body 태그 driver 객체 생성
for i in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

# 이미지 요소(elements) 수집하기
imgs = driver.find_elements(
    By.CSS_SELECTOR, "img._fe_image_tab_content_thumbnail_image"
)
# print(len(imgs))

links = []

# for 루프를 통해 src 속성 값을(링크)을 가져옴
for img in imgs:
    link = img.get_attribute("src")
    # 잘못가져와진 값들을 조건식으로 필터링
    if "http" in link:
        links.append(link)

# 폴더 생성
import os

if not os.path.isdir("./{}".format(keyword)):  # 폴더가 겹치는지 확인
    os.mkdir("./{}".format(keyword))
print("[폴더생성]")


# 다운로드 - 파일이름(확장자), 파일저장위치
## rfind() : 뒤에서부터 탐색해서 인덱스 반환 / find() : 앞에서부터 탐색해서 인덱스 반환
for index, link in enumerate(links):
    # 확장자가 무엇인지 추출
    start = link.rfind(".")
    end = link.rfind("&")
    filetype = link[start:end]  # 확장자 : .jpg
    # 파일이름이 길어지는 일부 현상 조치
    if "%" in filetype:
        end = filetype.find("%")
        filetype = filetype[:end]

    # print(filetype)
    # 키워드가 들어갈 자리는 0번으로 두고, index가 들어갈 자리를 1번으로 둘건데 001, 002 등 이런식으로 세자리 정수를 만듬(03d). 2번 자리에는 확장자가 들어감
    filename = "./{0}/{0}{1:03d}{2}".format(keyword, index, filetype)
    # ulretrieve(경로URL, 저장 파일 경로) 함수를 이용해서 다운로드
    urlretrieve(link, filename)

# tqdm 사용하는 버전
"""for index, link in tqdm(enumerate(links),total=len(links)):
    # 확장자가 무엇인지 추출
    start = link.rfind('.')
    end = link.rfind('&')

    file_type = link[start:end] # 확장자 : .jpg
    filename = './{0}/{0}{1:03d}{2}'.format(keyword, index, file_type)  # 파일명 : 아이스크림001.jpg
    urlretrieve(link, filename)

print('[ 다운로드 완료 ] ')
"""

print("[다운로드 완료]")

# 압축
import zipfile

zip_file = zipfile.ZipFile("./{}.zip".format(keyword), "w")
# os.listdir는 폴더안에 들어있는 파일 목록들을 전부 수집해준다.
for image in os.listdir("./{}".format(keyword)):  ## image : 방탄소년단000.jpg
    print(image, "압축파일에 추가중")
    zip_file.write("./{}/{}".format(keyword, image))
zip_file.close()
print("[압축 완료]")

time.sleep(3)
# driver.quit() # 웹 브라우저 종료. driver.close()는 탭 종료
driver.quit()
