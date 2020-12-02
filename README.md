# naver-news-crawling
## 설명
'''
*네이버 뉴스 기사의 경제 섹션 중 '금융', '증권', '산업/재계' 분류 뉴스를 크롤링하는 크롤러입니다.

*크롤링된 결과물에는 제목, 언론사, oid, aid, 뉴스 본문내용의 메타정보를 포함합니다.

*크롤링은 요청할 때마다 이루어지는 작업으로 합니다. 

*한 번 요청에 가장 최근 10개 뉴스를 크롤링합니다.

*크롤링 결과물은 파일명: {날짜}-{시간}.json으로 저장됩니다.
'''

## 개발환경
Mac OS, Pycharm, Pythoon 3.8


## 라이브러리
'''
$ pip install bs4

$ pip install lxml

$ pip install requests
'''
