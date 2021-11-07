## 유로 2020 워느카운트

file = open('naver_news_유로 2020_210629_144330.txt', "r",encoding="utf-8")

text = file.read()

wordList = text.split()

output_file_name = '단어대체_유로2020.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\n".format(''))
output_file.close()

def fwrite_news(output_file_name, word) :
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\n".format(word))
    output_file.close()
    return

country = ['웨일스','덴마크','이탈리아','오스트리아','네덜란드','체코','벨기에','포르투갈','크로아티아','스페인','프랑스','스위스','잉글랜드','독일','스웨덴','우크라이나']
for word in wordList :
    if word not in country :
        del word
    else :
        fwrite_news(output_file_name, word)

file = open('단어대체_유로2020.txt', "r",encoding="utf-8")

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
    


