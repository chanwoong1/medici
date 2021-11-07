## 유로 2016 워드카운트

file = open('naver_news_유로 2016_210629_140520.txt', "r",encoding="utf-8")

text = file.read()

wordList = text.split()

output_file_name = '단어대체_유로2016.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\n".format(''))
output_file.close()

def fwrite_news(output_file_name, word) :
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\n".format(word))
    output_file.close()
    return

country = ['스위스','폴란드','크로아티아','포르투갈','웨일스','북아일랜드','헝가리','벨기에','독일','슬로바키아','이탈리아','스페인','프랑스','아일랜드','잉글랜드','아이슬란드']
for word in wordList :
    if word not in country :
        del word
    else :
        fwrite_news(output_file_name, word)

file = open('단어대체_유로2016.txt', "r",encoding="utf-8")

text = file.read()

wordList = text.split()


wordCount = {}

for word in wordList:
    # Get 명령어를 통해, Dictionary에 Key가 없으면 0리턴

    wordCount[word] = wordCount.get(word, 0) + 1
    keys = sorted(wordCount.keys())

wordCount_sort = dict(sorted(wordCount.items(), key = lambda x:x[1] ,reverse=True))

for word in wordCount_sort.keys():
    print(word + ':' + str(wordCount_sort[word]))
    


