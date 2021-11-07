'''
import requests
from lxml import html

url = "https://news.naver.com"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}

html_req = requests.get(url, headers = headers)
tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class="hdline_article_tit"]/a/text()')
print (titles)
results = []
for title in titles:
    print(title)
    title_clean = title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
    results.append(title_clean)
    print('------------------------')
    print(title_clean)
    print('========================\n')
print(len(results))
print(results)

'''
import time

'''
import requests
from lxml import html

url = "http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=005930"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

html_req = requests.get(url, headers = headers)
tree = html.fromstring(html_req.content)
titles = tree.xpath('//p[@class="tit"]/a/text()')
print (titles)
results = []
for title in titles:
    print(title)
    title_clean = title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
    results.append(title_clean)
    print('------------------------')
    print(title_clean)
    print('========================\n')
print(len(results))
print(results)
'''

'''
import requests
from lxml import html
keyword = '킥보드'
#url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge& 킥보드 &sort=1&photo=0&field=0&pd=3'\
#'&ds=2021.01.01&de=2021.04.30&mynews=0&office_type=0&office_section_code=0&news_office_checked='\
#'&nso=so:dd,p:from20210101to20210430,a:all&start=1
url = 'https://search.naver.com/search.naver?where=news&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds=2021.01.01&de=2021.04.30&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20210101to20210430&is_sug_officeid=0'
print (url)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
html_req = requests.get(url, headers = headers)
tree = html.fromstring(html_req.content)
bodies = tree.xpath('//ul[@class="list_news"]/li')
print(len(bodies))
results = []
for body in bodies:
    news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
    try :
        news_url = body.xpath('.//a[@class="info"]/@href')[0]
    except :
        news_url = ''
    news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
    results.append([news_title_clean, news_url])
        
#print(results)
for i in range(len(results)) :
    print(results[i])
'''

''' #3번
import requests
from lxml import html

keyword = '킥보드'
page_num = 1
url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds=2021.01.01&de=2021.04.30&cluster_rank=48&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20210430,a:all&start='+str(page_num)
print(url)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
html_req = requests.get(url, headers=headers)
tree = html.fromstring(html_req.content)
bodies = tree.xpath('//ul[@class="list_news"]/li')
print(len(bodies))
results = []
for body in bodies:
    news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
    news_url =''
    try:
        news_url = body.xpath('.//a[@class="info"]/@href')[0]
    except:
        media_url = body.xpath('.//a[@class="info press"]/@href')[0]
    news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
    if news_url != '' :
        results.append([news_title_clean, news_url])
    else :
        results.append([news_title_clean, media_url])

# print(results)
for i in range(len(results)):
    print(results[i])

'''

'''
# 4번
import requests
from lxml import html
import time

keywords = ['킥보드','자전거']

def fcrawl_news(keyword, page_num) :
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds=2021.01.01&de=2021.04.30&cluster_rank=48&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20210430,a:all&start='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//ul[@class="list_news"]/li')
    results = []
    for body in bodies:
        news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
        news_url =''
        try:
            news_url = body.xpath('.//a[@class="info"]/@href')[0]
        except:
            media_url = body.xpath('.//a[@class="info press"]/@href')[0]
        news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
        if news_url != '' :
            results.append([news_title_clean, news_url])
        else :
            results.append([news_title_clean, '*', media_url])
    return results

def fmain() :
    for keyword in keywords :
        for i in range(1, 4) :
            print(keyword, i)
            page_num = (i-1) * 10 + 1
            results = fcrawl_news(keyword, page_num)
            for i in range(len(results)):
                print(results[i])
            time.sleep(6)

fmain()
# print(results)
#for i in range(len(results)):
#    print(results[i])

'''




'''
# 5번
import requests
from lxml import html
import time

keywords = ['킥보드','자전거']

output_file_name = 'naver_news_list.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\t{} | {}\n".format('페이지','키워드','제목','NEWS_URL', 'MEDIA_URL'))
output_file.close()

def fwrite_news(i, keyword, news_title_clean, news_url = '', media_url = '') :
    print([i, keyword, news_title_clean, news_url, media_url])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{} | {}\n".format(i, keyword, news_title_clean, news_url, media_url))
    output_file.close()
    return

def fcrawl_news(keyword, i) :
    page_num = (i - 1) * 10 + 1
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds=2021.01.01&de=2021.04.30&cluster_rank=48&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20210430,a:all&start='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//ul[@class="list_news"]/li')
    results = []
    for body in bodies:
        news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
        news_url =''
        media_url = ''
        try:
            news_url = body.xpath('.//a[@class="info"]/@href')[0]
        except:
            media_url = body.xpath('.//a[@class="info press"]/@href')[0]
        news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
        if news_url != '' :
            results.append([i, keyword, news_title_clean, news_url, ''])
            fwrite_news(i, keyword, news_title_clean, news_url,'')
        else :
            results.append([i, keyword, news_title_clean, '', media_url])
            fwrite_news(i, keyword, news_title_clean,'', media_url)

    return results

def fmain() :
    for keyword in keywords :
        for i in range(1, 4) :
            print(keyword, i)
            results = fcrawl_news(keyword, i)
            time.sleep(2)

fmain()
'''




# 6번
import requests
from lxml import html
import time

keywords = ['킥보드','자전거']

def fmake_file(keyword) :
    output_file_name = 'naver_news_'+keyword+'_'+time.strftime("%y%m%d_%H%M%S")+'.txt'
    output_file = open(output_file_name, "w", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{} | {}\n".format('페이지','키워드','제목','NEWS_URL', 'MEDIA_URL'))
    output_file.close()
    return output_file_name

def fwrite_news(output_file_name, i, keyword, news_title_clean, news_url = '', media_url = '') :
    print([i, keyword, news_title_clean, news_url, media_url])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{} | {}\n".format(i, keyword, news_title_clean, news_url, media_url))
    output_file.close()
    return

def fcrawl_news(keyword, i, output_file_name) :
    page_num = (i - 1) * 10 + 1
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds=2021.01.01&de=2021.04.30&cluster_rank=48&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20210430,a:all&start='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//ul[@class="list_news"]/li')
    results = []
    for body in bodies:
        news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
        news_url =''
        media_url = ''
        try:
            news_url = body.xpath('.//a[@class="info"]/@href')[0]
        except:
            media_url = body.xpath('.//a[@class="info press"]/@href')[0]
        news_title_clean = news_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
        if news_url != '' :
            results.append([i, keyword, news_title_clean, news_url, ''])
            fwrite_news(output_file_name, i, keyword, news_title_clean, news_url,'')
        else :
            results.append([i, keyword, news_title_clean, '', media_url])
            fwrite_news(output_file_name, i, keyword, news_title_clean,'', media_url)

    return results

def fmain() :
    for keyword in keywords :
        output_file_name = fmake_file(keyword)
        for i in range(1, 4) :
            print(keyword, i)
            results = fcrawl_news(keyword, i, output_file_name)
            time.sleep(2)

fmain()



# 뉴스 페이지로 가져오기

import requests
from lxml import html
import time

keyword = '킥보드'
input_file_name = 'naver_news_킥보드_210624.txt'

output_file_main_name = 'naver_news_main_' + keyword + '_' + time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file_main = open(output_file_main_name, "w", encoding="utf-8")
output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('번호','키워드','매체','날짜','제목','URL','본문'))
output_file_main.close()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}

def fget_list() :
    input_file = open(input_file_name, "r", encoding="utf-8")
    input_text = input_file.read()
    lines = input_file.splitlines()
    lists = []
    for line in lines[:] :
        elms = line.strip().split("\t")
        news_title = elms[2]
        try :
            url = elms[3]
        except :
            url = ''
        lists.append([news_title, url])

    return lists[1:]

def fwrite_news_main(count, news_media, news_date, news_title, news_url, news_article) :
    print([count, keyword, news_media, news_date, news_title, news_url, news_article])
    output_file_main = open(output_file_main_name, "a", encoding="utf-8")
    output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(count, keyword, news_media,news_date,news_title,news_url,news_article))
    return

def fcrawl_news_main(count, news_title, news_url) :
    html_req = requests.get(news_url, headers = headers)
    tree = html.fromstring(html_req.content)

    try :
        news_media = tree.xpath('//div[@class="press_logo"]/a/img/@title')[0]
    except :
        news_media = ''
    try :
        news_date = tree.xpath('//div[@class="sponsor"]/span[@class="t11"]/text()')[0]
    except :
        news_date = ''
    try :
        news_article = tree.xpath('//div[@id="articleBodyContents"]/descendant-or-self::text()[not(ancestor::script)]')
    except :
        news_article = ''
    news_article = " ".join(news_article).replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()
    fwrite_news_main(count, news_media, news_date, news_title, news_url, news_article)

    return

def fmain() :
    lists = fget_list()
    count = 1
    for list in lists[:] :
        print(list)
        news_title = list[0]
        news_url = list[1]
        if len(news_url) == 0 :
            continue
        fcrawl_news_main(count, news_title, news_url)
        time.sleep(2)
        count += 1

fmain()





