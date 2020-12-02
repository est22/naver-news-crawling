'''
======================= Required Library =========================
$ pip install bs4
$ pip install lxml
$ pip install requests

========================== Description ===========================
Latest Top Ten News Crawler of three sectors from Naver Economy

@ author: Lia An <anlia.seoul@gmail.com>
@ date: 2020-12-03

'''

from bs4 import BeautifulSoup
import bs4.element
import bs4
import requests
#requests.packages.urllib3.disable_warnings()
from datetime import datetime
import json



# Function: BeautifulSoup object creator
def get_soup_obj(sec_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'}
    res = requests.get(sec_url, verify=False, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    return soup



# Function: Get basic news Info
def get_top10_news_info(sec, sid):
    sec_url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101" + "&sid2=" + sid
    # get corresponding HTML links
    soup = get_soup_obj(sec_url)

    # get latest 10 articles
    news_list10 = []
    lis10 = soup.find('ul', class_='type06_headline').find_all("li", limit=10)

    for li in lis10:
        # 1.news title   2.press   3.news_url   4.oid   5.aid
        news_info = {
            "title": li.dl.dt.a.img.attrs.get('alt') if li.dl.dt.a.img else li.dl.dt.find('a').text.replace("\n", "").replace("\t", "").replace("\r", ""),
            "press": li.find('span', class_="writing").text.replace("\n", "").replace("\t", "").replace("\r", ""),
            "news_url": li.dl.dt.a.attrs.get('href'),
            "oid": li.dl.dt.a.attrs.get('href').split("oid=")[1].split("&")[0],
            "aid": li.dl.dt.a.attrs.get('href').split("aid=")[1].split("&")[0]
        }
        news_list10.append(news_info)

    return news_list10



# Function: Get news content
def get_news_contents(url):
    soup = get_soup_obj(url)
    body = soup.find('div', class_="_article_body_contents")

    news_contents = ''
    for content in body:
        if type(content) is bs4.element.NavigableString and len(content) > 50:
            news_contents += content.strip() + ' '

    return news_contents



# Function: Crawl three categories of 'Finance(금융)', 'Stock(증권)', 'Industry(산업/재계)'
def get_naver_news_top10():
    # a dictionary to save crawling results
    news_dic = dict()
    sections = ["금융", "증권", "산업/재계"]
    # url id
    section_ids = ['259', '258', '261']

    for sec, sid in zip(sections, section_ids):
        # call function: basic news info
        news_info = get_top10_news_info(sec, sid)

        for news in news_info:
            # call function: news contents
            news_url = news['news_url']
            news_contents = get_news_contents(news_url)

            # a dictionary to save all news contents data
            news['news_contents'] = news_contents

        news_dic[sec] = news_info

    return news_dic



def save_as_json():
    # file name standardization
    now = datetime.now()
    outputFileName = '{%s-%s-%s}-{%s시 %s분 %s초}.json' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    # save file as json
    with open(outputFileName, 'w') as outputFileName:
        json.dump(get_naver_news_top10(),outputFileName, indent=4, ensure_ascii = False)



save_as_json()
