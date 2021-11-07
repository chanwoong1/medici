import requests
from lxml import html
from konlpy.tag import Okt
from collections import Counter
from time import sleep

# 기본 url
url = 'https://gall.dcinside.com/board/lists/?id=hit&page='

# 헤더정보
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

# 게시글의 정보들을 담을 Post Class
class Post:
    
    # 멤버변수를 설정해줄 class 생성자
    def __init__(self,title,content):
        self.title = title
        self.content = content
    
    # 멤버변수들을 출력해줄 print함수
    def print_datas(self):

        print('제목=======>',self.title)
        print('내용 단어 빈도=======>',self.content)



# url을 전달받아 html element를 return 해주는 함수
def request_page(url,page=''):
    
    # page를 연결해서 새로운 url 생성 default = ''
    new_url = url+str(page)

    # url과 헤더정보를 가지고 request 하고 response 객체를 받음
    html_req = requests.get(url,headers=headers)

    # html element 객체를 저장
    tree = html.fromstring(html_req.content)
    
    return tree

# 제목들을 가진 html element를 return 해주는 함수
def get_title_tree(tree):

    bodies = tree.xpath('//tr[@class="ub-content us-post"]/td[@class="gall_tit ub-word"]/a')

    # type 'list'
    return bodies

# 제목 html element에서 제목 text를 뽑는 함수
def get_title(tree):

    title = tree.xpath('.//text()')

    return title

# 제목 html element에서 href를 타고 들어가서 내용을 보고, 단어의 빈도수를 return 하는 함수
def get_contents(tree):

    # href 옵션 안에 있는 url 생성
    base_url = 'https://gall.dcinside.com'
    url = tree.xpath('.//@href')
    url = base_url+url[0]
    
    # html 전체 페이지를 저장
    content_tree = request_page(url)
    
    # p태그 안에 있는 text를 저장
    p_text = content_tree.xpath('//div[@class="write_div"]/p/text()')

    # p태그 안에 있는 text를 정제
    p_text = [text.replace("\n", "").replace("\t", "").replace("\r", "").strip() for text in p_text]

    # div태그 안에 있는 text를 저장
    div_text = content_tree.xpath('//div[@class="write_div"]/div/text()')

    # div태그 안에 있는 text를 정제
    div_text = [text.replace("\n", "").replace("\t", "").replace("\r", "").strip() for text in p_text]
    
    # 모든 text를 다 담을 string객체 초기화
    text = ''
    
    # list마다 돌면서 text에 담아줌
    text = text_merger(text,p_text)
    text = text_merger(text,div_text)
    
    # 관심없는 단어 list 생성
    stop_words = ['이','가','는','일이','그','것','진짜','수']

    
    # konlpy의 Okt 사용하려고 객체 생성
    okt = Okt(max_heap_size=1024)
    #okt2 = Okt(max_heap_size=2048)
    
    # 명사만 고르기
    nouns = okt.nouns(text)

    # 명사 고른거 중에서 관심없는 단어 제거
    for i,v in enumerate(nouns):
        if v in stop_words:
            nouns.pop(i)
    
    # 명사 고른 list에서 빈도수 측정
    count = Counter(nouns)
    
    # 상위 5개만
    noun_list = count.most_common(5)

    return noun_list

# list를 돌면서 text를 연결해줄 함수
def text_merger(string,list):

    for item in list:
        string = string+item

    return string

def main():

    # 커스텀 하게 만든 class Post의 객체들을 담을 list생성
    post_list = []
    
    # 1 페이지만
    for i in range(1,2):
        
        # 페이지 변수 생성
        page = i
        
        # 생성된 url로 html 문서 저장
        temp_tree = request_page(url,str(page))
        
        # 제목 element 들만 모아서 list에 저장
        title_tree_list = get_title_tree(temp_tree)

        # 제목 element들을 돌면서
        for i in range(len(title_tree_list)):
            
            # 제목 element는 하나걸러 하나씩 나옴
            if i % 2 == 0:
                
                # 예외처리 
                try:
                    
                    # 제목받고
                    title = get_title(title_tree_list[i])
                    
                    # 내용 받고
                    contents = get_contents(title_tree_list[i])
                    
                    # 받은 내용을 하나의 클래스 객체로 만들어서
                    new_post = Post(title,contents)
                    
                    # 리스트에 추가
                    post_list.append(new_post)
                
                    # 만든객체 제거
                    del new_post

                except:
                    pass
        # 수면
        sleep(5)

    # 객체 리스트를 돌면서
    for post in post_list:
        
        # print하는 멤버변수 호출
        post.print_datas()
        print('\n')

# 모든것의 시작인 메인함수
main()