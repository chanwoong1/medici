## 유로 2016 기사 수집
import requests
from lxml import html
import time

keyword = '유로 2016'
#ds , de 는 yyyy.mm.dd 형식 사용
ds = '20160101'
de = '20160624'

def fmake_file(keyword) :
    output_file_name = 'naver_news_'+keyword+'_'+time.strftime("%y%m%d_%H%M%S")+'.txt'
    output_file = open(output_file_name, "w", encoding="utf-8")
    output_file.write("{}\t{}\n".format('제목','본문요약'))
    output_file.close()
    return output_file_name

def fwrite_news(output_file_name, news_title_clean, news_text_clean) :
    print([news_title_clean, news_text_clean])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\n".format(news_title_clean, news_text_clean))
    output_file.close()
    return

def fcrawl_news(keyword, i, output_file_name, ds, de) :
    page_num = (i - 1) * 10 + 1
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=0&photo=0&field=0&pd=3&ds='+str(ds)+'&de='+str(de)+'&cluster_rank=90&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20160101to20160610,a:all&start='+str(page_num)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    bodies = tree.xpath('//ul[@class="list_news"]/li')
    results = []
    for body in bodies:
        news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
        '''
        news_url =''
        media_url = ''
        try:
            news_url = body.xpath('.//a[@class="info"]/@href')[0]
        except:
            media_url = body.xpath('.//a[@class="info press"]/@href')[0]
        '''
        news_text = body.xpath('.//a[@class="api_txt_lines dsc_txt_wrap"]/text()')
        news_text = " ".join(news_text)

        news_title_clean = news_title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
        news_text_clean = news_text.replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("■"," ").replace("▲"," ").replace("ⓒ"," ").strip()

        '''
        if news_url != '' :
            results.append([i, keyword, news_title_clean, news_url, ''])
            fwrite_news(output_file_name, i, keyword, news_title_clean, news_url,'')
        else :
            results.append([i, keyword, news_title_clean, '', media_url])
            fwrite_news(output_file_name, i, keyword, news_title_clean,'', media_url)
        '''

        results.append([i, news_title_clean, news_text_clean])
        fwrite_news(output_file_name, news_title_clean, news_text_clean)


    return results

def fmain() :
    output_file_name = fmake_file(keyword)
    i = 1
    while i < 402 :
        print(keyword, i)
        results = fcrawl_news(keyword, i, output_file_name, ds, de)
        time.sleep(2)
        i += 1
    print('끝')

fmain()









