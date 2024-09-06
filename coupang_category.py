import time, sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
coupang_url = 'https://www.coupang.com/'
driver.get(coupang_url)

time.sleep(2)

# 'third-depth-list' 클래스의 모든 요소를 찾기
third_depth_lists = driver.find_elements(By.CLASS_NAME, 'third-depth-list')

# 파일 열기 (쓰기 모드)
with open("output.txt", "w", encoding="utf-8") as file:
    # 각 'third-depth-list' 요소 내의 모든 'a' 태그의 href 속성 추출 및 파일에 쓰기
    for third_depth_list in third_depth_lists:
        a_tags = third_depth_list.find_elements(By.TAG_NAME, 'a')  # 각 third-depth-list 내의 모든 a 태그 찾기
        for a in a_tags:
            href = a.get_attribute('href')
            if href:  # href가 존재하는 경우에만 파일에 쓰기
                file.write(href + "\n")  # 한 줄씩 파일에 저장

# 브라우저 닫기
driver.quit()