from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd

# get_result = re.compile(r'<td class="zentriert">\d*</td>')

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}


#B1:https://www.transfermarkt.com/1-bundesliga/torverteilungminuten/wettbewerb/L1/plus/1?saison_id=
#B2:https://www.transfermarkt.com/2-bundesliga/torverteilungminuten/wettbewerb/L2/plus/1?saison_id=2006
#J1:https://www.transfermarkt.com/j1-league/torverteilungminuten/wettbewerb/JAP1/plus/1?saison_id=2005
#En1:https://www.transfermarkt.com/premier-league/torverteilungminuten/wettbewerb/GB1/plus/1?saison_id=2006
#En2:https://www.transfermarkt.com/championship/torverteilungminuten/wettbewerb/GB2/plus/1?saison_id=2015
#It1:https://www.transfermarkt.com/serie-a/torverteilungminuten/wettbewerb/IT1/plus/1?saison_id=2015
#Sp1:https://www.transfermarkt.com/laliga/torverteilungminuten/wettbewerb/ES1/plus/1?saison_id=2015
df_total = []
#start_year = year, end_year = year+1
for j in range(2006,2017):
    baseUrl = 'https://www.transfermarkt.com/laliga/torverteilungminuten/wettbewerb/ES1/plus/1?saison_id='+str(j)
    req = urllib.request.Request(baseUrl,headers=headers)
    response = urlopen(req).read().decode("utf-8")
    bsObj = BeautifulSoup(response,"lxml")
    content =bsObj.find('table',{'class':'items'})
    rows = content.findAll("tr")

    # for tr in content.findAll("tr"):
    #     print(tr.td)

    for i in range(2,len(rows)):
        df= []
        results = rows[i].find_all("td",{"class":'zentriert'})
        team = rows[i].find("td",{"class":"hauptlink"})
        df.append(j)
        df.append(team.get_text())
        for result in results:


            df.append(result.get_text())

        df_total.append(list(df))
# print(df_total)
labeles = ['season','team','none','15min','30min','45min','45min+','60min','75min','90min','90min+','team_total']
df_goals = pd.DataFrame.from_records(df_total, columns=labeles)

def transformTeam(df):
    teams = []
    for i in range(len(df)):
        teams.append(df.team[i].split(' ')[0]+' '+df.team[i].split(' ')[1])
    df['team2'] = teams
    return df
# print(df_goals.head())

transformTeam(df_goals)

df_goals.to_csv('data/df_goals_Sp1.csv', index=False,)








