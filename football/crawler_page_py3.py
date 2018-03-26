#-*- coding: utf-8 -*-
from urllib.request import urlopen, Request
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
import time
import pandas as pd

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    req = Request(url, headers=headers)
    try:
        html = urlopen(req).read()
    except URLError as e:
        return None
    return html

def getData(baseUrl):
    dataList=[]
    authors = []
    content = []
    url = baseUrl
    html = getHtml(url)
    bsObj = BeautifulSoup(html,"lxml")
    for sibling in bsObj.findAll('section',{'class':'box answer '}):
        # for sib in sibling.find('header',{'class':'wrap answer_detail'}).findAll('p'):

        content.append(sibling.find('header',{'class':'wrap answer_detail'}).p.get_text())
        authors.append(sibling.find('div',{'class':'box-aw user_info'}).a.get_text())
    dataList.append(authors)
    dataList.append(content)
    return dataList

def saveFile(dataList,path):
    labels = ['author','content']
    df = pd.DataFrame(data={'author':dataList[0], 'content':dataList[1]},
                      columns=['author','content'])
    df.to_csv(path,index=False)



    # print(dataList)


def main():
    baseUrl= 'http://www.oschina.net/question/12_9507'
    dataList = getData(baseUrl)
    time.sleep(1)

    path = 'data/test.csv'
    saveFile(dataList,path)
    # print(dataList)

main()
