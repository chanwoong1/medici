import requests
import time
from lxml import html

keyword = 'hit'

output_file_name = 'dcgal_'+keyword + "_" + time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\n".format('페이지', '제목', 'URL'))
output_file.close()


def fwrite_news(i, article_title, article_url):
    print([i, article_title, article_url])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\n".format(i, article_title, article_url))
    return


def fcrawl_news(i):
    page_num = i

    url = 'https://gall.dcinside.com/board/lists/?id='+keyword+'&page='+str(page_num)+'&list_num=100&sort_type=N&search_head='
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    html_req = requests.get(url, headers=headers)

    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//td[@class="gall_tit ub-word"]')
    print(len(bodies))

    results = []

    for body in bodies:
        try:
            article_title = body.xpath('a/text()')[0]
        except:
            article_title = ''
        print(article_title)
        try:
            article_url = body.xpath('a/@href')[0]
            article_url = 'https://gall.dcinside.com'+article_url
        except:
            article_url = ''
        print(article_url)

        if article_title != '':
            article_title_clean = article_title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
            results.append([article_title_clean, article_url])
            fwrite_news(i, article_title_clean, article_url)

    output_file.close()

    return results


def fmain():

    for i in range(1, 3):
        print(i)
        results = fcrawl_news(i)
        print(results)
        time.sleep(6)


fmain()