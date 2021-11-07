### 210625 크롤링
## 공공데이터 포털 API 연결 및 데이터 수집
'''
import requests
import time
from xml.etree import ElementTree
from datetime import date
from dateutil.relativedelta import relativedelta

input_file_name = 'region_code5.csv'
secret_key = 'HkBEdLGc%2B44x7cXI3zfMTxhM2I5rkFcUdgQU4W4LmgBr3GWyJdhyZ9Y0Wynazhy5gpgBPk7xl0ceR72cxRXVsg%3D%3D'

date_start = date(2021, 6, 1)
date_end = date(2021, 5, 1)

output_file_name = "trade_apt_api_" + time.strftime("%y%m%d_%H%M%S") + ".txt"
output_file = open(output_file_name, "w", encoding = "utf-8")
output_file.write = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('기준년월','지역명','지역코드','법정동','아파트','거래금액','년','월','일','건축년도','전용면적','층'))
output_file.close()

def fget_list() :
    input_file = open(input_file_name, "r", encoding = "euc-kr")
    input_text = input_file.read()
    lines = input_text.splitlines()
    lists = []
    for line in lines :
        line = line.replace('"', '')
        elms = line.strip().split(",")
        region_name = elms[0]
        region_code = elms[1]
        if region_code[:4] == "4128" :
            lists.append([region_name, region_code])

    return lists

def fget_html(region_name, region_code, this_ym) :
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    page_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD="+str(region_code)+"&DEAL_YMD="+str(this_ym)+"&serviceKey="+secret_key
    print(page_url)
    response = requests.get(page_url, headers = headers)
    tree = ElementTree.fromstring(response.content)
    elements = tree.iter(tag = "item")

    for element in elements :
        price = element.find("거래금액").text
        const_year = element.find("건축년도").text
        year = element.find("년").text
        month = element.find("월").text
        day = element.find("일").text
        dong = element.find("법정동").text
        apt_name = element.find("아파트").text
        square = element.find("전용면적").text
        stair = element.find("층").text
        elm_list = [this_ym, region_name,region_code,dong,apt_name,price,year,month,day,const_year,square,stair]
        print(elm_list)
        output_file = open(output_file_name, "a", encoding="utf-8")
        output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(this_ym, region_name,region_code,dong,apt_name,price,year,month,day,const_year,square,stair))
        output_file.close()
    return

def fmain() :
    date_this = date_start
    lists = fget_list()

    while date_this >= date_end :
        print(date_this)
        this_year = str(date_this.year)
        this_month = str(date_this.month)

        if len(this_month) == 1 :
            this_month = "0" + str(this_month)
        this_ym = this_year + this_month

        print(this_ym)
        for list in lists :
            region_name = list[0]
            region_code = list[1]
            print(region_name, region_code)
            fget_html(region_name, region_code, this_ym)

        date_this = date_this - relativedelta(months = 1)

    return

fmain()
'''


'''
## selenium을 활용한 데이터 수집 실습

import time
import selenium.webdriver as webdriver

driver = webdriver.Chrome('C://chromedriver/chromedriver.exe')
url_start = 'https://news.naver.com'
keywords = ['킥보드', '자전거']

def finput_keyword(keyword) :
    driver.switch_to.window(driver.window_handles[0])

    driver.get(url_start)

    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//input[@class="text_index"]').send_keys(keyword)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    driver.implicitly_wait(5)
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(5)
    driver.find_elements_by_xpath('//a[@role="option"]')[1].click()
    driver.implicitly_wait(5)

    return driver

def fmake_file(keyword) :
    output_file_name = 'naver_news_' + keyword + "_" + time.strftime("%y%m%d_%H%M%S") + '.txt'
    output_file = open(output_file_name, "w", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format('페이지','키워드','제목','URL'))
    output_file.close()
    return output_file_name

def fwrite_news(i, keyword, news_title_clean, news_url, output_file_name) :
    print([i,keyword,news_title_clean,news_url])
    output_file = open(output_file_name,"a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format(i,keyword,news_title_clean,news_url))
    output_file.close()
    return

def fcrawl_news_selenium(driver, keyword, i, output_file_name) :
    bodies = driver.find_elements_by_xpath('//ul[@class="list_news"]/li')

    for body in bodies :
        news_title_elm = body.find_elements_by_xpath('.//a[@class="news_tit"]')[0]
        news_title = news_title_elm.get_attribute('title')
        try :
            news_url_elm = body.find_elements_by_xpath('.//a[@class="info"]')[0]
            news_url = news_url_elm.get_attributes('href')
        except :
            news_url = ''

        news_title_clean = news_title.replace("\n", "").replace("\t","").replace("\r","").strip()
        fwrite_news(i, keyword, news_title_clean, news_url, output_file_name)

    page_nav = driver.find_element_by_xpath('//div[@class="sc_page_inner"]')
    next_page = page_nav.find_element_by_link_text(str(int(i)+1))
    next_page.click()
    driver.implicitly_wait(10)

    return

def fmain() :
    for keyword in keywords :
        output_file_name = fmake_file(keyword)
        driver = finput_keyword(keyword)

        for i in range(1, 15) :
            print(i)
            fcrawl_news_selenium(driver, keyword, i, output_file_name)
            time.sleep(2)

        driver.close()

fmain()
'''


### Pyinstaller로 윈도우 실행파일 생성

import time
import selenium.webdriver as webdriver
import sys

driver = webdriver.Chrome('C://chromedriver/chromedriver.exe')
url_start = 'https://news.naver.com' \
            ''
if len(sys.argv) == 2 :
    keywords = list(sys.argv[1].split(','))
else :
    keywords = ['NH은행','NH증권']

def finput_keyword(keyword):
    driver.switch_to.window(driver.window_handles[0])

    driver.get(url_start)

    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//input[@class="text_index"]').send_keys(keyword)

    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//button[@type='submit']").click()

    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])

    driver.implicitly_wait(10)
    time.sleep(5)
    driver.find_elements_by_xpath('//a[@role="option"]')[1].click()
    time.sleep(5)
    driver.implicitly_wait(10)

    return driver

def fmake_file(keyword):
    output_file_name = 'naver_news_' + keyword + "_" + time.strftime("%y%m%d_%H%M%S")+'.txt'
    output_file = open(output_file_name, "w", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format('페이지','키워드','제목','URL'))
    output_file.close()
    return output_file_name


def fwrite_news(i, keyword, news_title_clean, news_url, output_file_name):
    print([i, keyword, news_title_clean, news_url])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format(i, keyword, news_title_clean, news_url))
    output_file.close()
    return

def fcrawl_news_selenium(driver, keyword, i, output_file_name):

    bodies = driver.find_elements_by_xpath('//ul[@class="list_news"]/li')

    for body in bodies:
        news_title_elm = body.find_elements_by_xpath(".//a[@class='news_tit']")[0]
        news_title = news_title_elm.get_attribute('title')
        try:
            news_url_elm = body.find_elements_by_xpath('.//a[@class="info"]')[0]
            news_url = news_url_elm.get_attribute('href')
        except:
            news_url = ' '

        news_title_clean = news_title.replace("\n","").replace("\t","").replace("r","").strip()
        fwrite_news(i, keyword, news_title_clean, news_url, output_file_name)

    page_nav = driver.find_element_by_xpath('//div[@class="sc_page_inner"]')
    next_page = page_nav.find_element_by_link_text(str(int(i)+1))
    next_page.click()
    driver.implicitly_wait(10)

    return

def famin():
    for keyword in keywords:
        output_file_name = fmake_file(keyword)
        driver = finput_keyword(keyword)

        for i in range(1, 15) :
            print(i)
            fcrawl_news_selenium(driver, keyword, i, output_file_name)
            time.sleep(2)

        driver.close()

famin()









