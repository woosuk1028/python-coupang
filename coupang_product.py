import time, sys, os, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook

def only_number(string):
    number = re.sub(r"[^0-9]", "", string)
    return number


wb = Workbook()
ws = wb.active
ws.append(['id', 'name', 'img', 'url', 'price', 'star', 'review'])

options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

page = 1

while True:
    coupang_url = 'https://www.coupang.com/np/categories/498704?page='+str(page)
    driver.get(coupang_url)

    time.sleep(2)

    productList = driver.find_elements(By.ID, 'productList')
    babyProduct = driver.find_elements(By.CLASS_NAME, 'baby-product')

    pageElement = driver.find_element(By.ID, 'product-list-paging')
    totalPage   = pageElement.get_attribute('data-total')

    for babyProductList in babyProduct:
        productId   = babyProductList.get_attribute('id')
        productUrl  = babyProductList.find_element(By.CLASS_NAME, 'baby-product-link').get_attribute('href')
        productName = babyProductList.find_element(By.CLASS_NAME, 'name').get_attribute('innerText')
        print(str(page) + "=" + productName)
        productImg  = babyProductList.find_element(By.CLASS_NAME, 'image').find_element(By.TAG_NAME, 'img').get_attribute('src')

        reviewStarTag = babyProductList.find_elements(By.CLASS_NAME, 'rating')
        reviewStar = reviewStarTag[0].get_attribute('innerText') if reviewStarTag else 0

        reviewCntTag = babyProductList.find_elements(By.CLASS_NAME, 'rating-total-count')
        reviewCnt = only_number(reviewCntTag[0].get_attribute('innerText')) if reviewCntTag else 0

        try:
            priceTag = babyProductList.find_element(By.CLASS_NAME, 'price-value')
            price = priceTag.get_attribute('innerText')
            price = only_number(price) if price else 0
        except NoSuchElementException:
            price = 0

        if productId:
            price       = priceTag.get_attribute('innerText')
            if price:
                price = only_number(price)

            if productId:
                ws.append([productId, productName, productImg, productUrl, int(price), str(reviewStar), int(reviewCnt)])

    page += 1
    if int(page) > int(totalPage):
        break

wb.save('C:/python/product.xls')
wb.close()

# 브라우저 닫기
driver.quit()