'''

### 디시인사이드 웹크롤링

import requests
import time
from lxml import html

def fcrawl_news(i) :
    page_num = i
    url = 'https://gall.dcinside.com/board/lists/?id=hit&page='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    html_req = requests.get(url, headers = headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//td[@class="gall_tit ub-word"]')
    results = []
    for body in bodies :
        try :
            news_title = body.xpath('.//a/text()')[0]
        except :
            news_title = ''

        try:
            article_url = body.xpath('a/@href')[0]
            article_url = 'https://gall.dcinside.com'+article_url
        except:
            article_url = ''

        if news_title != '':
            #news_title_clean = news_title.replace("\n", "").strip()

            results.append([news_title,article_url])

    return results

def fmain() :
    for i in range(1, 3) :
        print(i)
        results = fcrawl_news(i)
        for i in results :-
            print(i)
        time.sleep(3)

fmain()
'''




'''
### 네이트판

import requests
import time
from lxml import html

output_file_name = 'pann_nate_' +time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\n".format('페이지','제목','URL'))
output_file.close()

def fwrite_news(i, article_title, article_url) :
    print([i, article_title, article_url])
    output_file = open(output_file_name,"a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\n".format(i, article_title, article_url))
    return

def fcrawl_news(i) :
    page_num = i
    url = 'https://pann.nate.com/talk/c20048?page='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    html_req = requests.get(url, headers = headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//td[@class="subject"]')
    results = []
    for body in bodies :
        if body.xpath('.//img[@class="ico"]') :
            article_title = body.xpath('.//a/b/text()')
        else :
            article_title = body.xpath('.//a/text()')
        if body.xpath('.//strong[@class="channel"]') :
            article_url = body.xpath('./a/@href')[0]
        else :
            article_url = body.xpath('.//a/@href')[0]
        article_url = 'https://pann.nate.com' + article_url
        #print(article_url)
        for article in article_title :
            article_clean = article.replace("\n", "").replace("\t", "").replace("\r", "").strip()
            if article_clean.find("[") :
                article_clean = article_clean
                results.append([page_num, article_clean, article_url])
                fwrite_news(i, article_clean, article_url)
    output_file.close()


    return results

def fmain() :
    for i in range(1, 3) :
        print(i)
        results = fcrawl_news(i)
        print(results)
        time.sleep(3)

fmain()
'''



### 네이트판 main
import requests
import time
from lxml import html

input_file_name = 'pann_nate_210629_095921.txt'

output_file_main_name = 'pann_nate_main_'+ time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file_main = open(output_file_main_name, "w", encoding="utf-8")

output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('번호', '글쓴이', '날짜', '조회수', '추천수', '댓글수', '제목', 'URL', '본문'))
output_file_main.close()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

def fget_list() :
    input_file = open(input_file_name, "r", encoding="utf-8")
    input_text = input_file.read()
    lines = input_text.splitlines()
    lists = []
    for line in lines[:] :
        elms = line.strip().split("\t")
        page_num = elms[0]
        title = elms[1]
        try :
            url = elms[2]
        except :
            url = ''
        lists.append([page_num, title, url])

    return lists[1:]

def fwrite_article_main(count, article_media, article_date, view_cnt, thumb_cnt, reply_cnt, article_title, article_url, article_article):
    print([count, article_media, article_date, view_cnt, thumb_cnt, reply_cnt, article_title, article_url, article_article])
    output_file_main = open(output_file_main_name, "a", encoding="utf-8")
    output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(count, article_media, article_date, view_cnt, thumb_cnt, reply_cnt, article_title, article_url, article_article))
    return

def fcrawl_article_main(count, article_title, article_url):
    html_req = requests.get(article_url, headers=headers)
    tree = html.fromstring(html_req.content)

    try:
        article_media = tree.xpath('//a[@class="writer"]/text()')[0]
    except:
        article_media = ''
    try:
        article_date = tree.xpath('//span[@class="date"]/text()')[0]
    except:
        article_date = ''
    try:
        view_cnt = tree.xpath('//span[@class="count"]/text()')[0].replace('조회 ', '')
    except:
        view_cnt = 0
    try:
        thumb_cnt = tree.xpath('//span[@class="gall_reply_num"]/text()')[0].replace('추천 ', '')
    except:
        thumb_cnt = 0
    try:
        reply_cnt = tree.xpath('//span[@class="gall_comment"]/a/text()')[0].replace('댓글 ', '')
    except:
        reply_cnt = 0
    try:
        article_article = tree.xpath('//div[@class="writing_view_box"]/descendant-or-self::text()[not(ancestor::script)]')
    except:
        article_article = ''
    article_article = ''.join(article_article)
    article_article = article_article.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\xa0', ' ').strip()

    fwrite_article_main(count, article_media, article_date, view_cnt, thumb_cnt, reply_cnt, article_title, article_url, article_article)

    return

def fmain():
    lists = fget_list()
    count = 1
    for list in lists[:]:
        print(list)
        article_title = list[1]
        article_url = list[2]
        if len(article_url) == 0:
            continue
        fcrawl_article_main(count, article_title, article_url)
        time.sleep(2)
        count += 1


fmain()
















'''
### 네이버 이미지 크롤링
import requests
import time
import json

project = 'naver_openapi_image'
keyword = input("키워드 입력 :")
display = 10
sort = 'date'

image_path = 'images/'

output_file_name = project + "_list_" + time.strftime("%y%m%d_%H%M%S") + ".txt"
output_file = open(output_file_name,"w", encoding="utf-8")
output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('start','num','title','link','thumbnail','sizeheight','sizewidth'))
output_file.close()

def fwrite_news(start, num, title, link, thumbnail, sizeheight, sizewidth) :
    print([start, num, title, link,thumbnail, sizeheight, sizewidth])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(start, num, title, link, thumbnail, sizeheight, sizewidth))
    return

def fcrawl_news(start) :
    
    url = 
'''













