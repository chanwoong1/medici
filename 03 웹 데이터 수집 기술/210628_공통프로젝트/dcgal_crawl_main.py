import requests
from lxml import html
import time

keyword = 'hit'
input_file_name = 'dcgal_hit_210628_141501.txt'

output_file_main_name = 'dcgal_main_' + keyword + "_" + time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file_main = open(output_file_main_name, "w", encoding="utf-8")
output_file_main.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('번호', '글쓴이', '날짜', '조회수', '추천수', '댓글수', '제목', 'URL', '본문'))
output_file_main.close()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}


def fget_list():
    input_file = open(input_file_name, "r", encoding="utf-8")
    input_text = input_file.read()
    lines = input_text.splitlines()
    lists = []
    for line in lines[:]:
        elms = line.strip().split("\t")
        page_num = elms[0]
        title = elms[1]
        try:
            url = elms[2]
        except:
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
        article_media = tree.xpath('//span[@class="nickname in"]/@title')[0]
    except:
        article_media = ''
    try:
        article_date = tree.xpath('//span[@class="gall_date"]/@title')[0]
    except:
        article_date = ''
    try:
        view_cnt = tree.xpath('//span[@class="gall_count"]/text()')[0].replace('조회 ', '')
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
        time.sleep(6)
        count += 1


fmain()