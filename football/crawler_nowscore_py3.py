#-*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

date = []
weekday = []
league = []
home_away = []
half = []
half_goals = []
overtime = []
over_goals =[]

#bundesliga : search_league=37
#bundesliga2: search_league=34
#premier league: search_league=25
#champions_league: search_league=20
#England_jiaji: search_league=21
#J-1：search_league=42
#J-2：search_league=43
#Italian_A: search_league=40
#Spanish_A: search_league=62


#采集竞彩网页数据
for j in range(1,120):
    baseUrl = 'http://info.sporttery.cn/football/match_result.php?page='+str(j)+'&search_league=62&start_date=2007-08-01&end_date=2017-05-22&dan='
    # req = urllib2.Request(baseUrl)
    response = urlopen(baseUrl).read()
    soup = BeautifulSoup(response, 'lxml')
    contents= []
    for content in soup.find_all('tr'):
        contents.append(content.get_text())
        # for x in len(contents):
        # contents2 = contents[2:len(contents)-6]
    # print len(contents)
    for x in range(1,(len(contents)-4)):
        contents[x]=contents[x].split()
        date.append(contents[x][0])
        weekday.append(contents[x][1])
        league.append(contents[x][2])
        home_away.append(contents[x][3])
        half.append(contents[x][4])
        # half_goals.append(pd.to_numeric(contents[x][4][0])+pd.to_numeric(contents[x][4][2]))
        overtime.append(contents[x][5])
        # over_goals.append(pd.to_numeric(contents[x][5][0]) + pd.to_numeric(contents[x][5][2]))
        # results['date'] = date

results=pd.DataFrame(data={'date':date,'weekday':weekday,'league':league,'home_away':home_away,
                           'half':half,'overtime':overtime},
                     columns=['date','weekday','league','home_away','half','overtime'])
# print results.head()
# results.to_csv('data/results_bundesliga2_2009-2017.txt',index=False,encoding='gbk')
# results.to_csv('data/results_PremierLeague_2009-2017.txt',index=False,encoding='gbk')
# results.to_csv('data/results_PremierLeague2_2009-2017.txt',index=False,encoding='gbk')
results.to_csv('data/results_Spanish_A_2009-2017.txt',index=False,encoding='gbk')

