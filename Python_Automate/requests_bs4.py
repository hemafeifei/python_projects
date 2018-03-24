import requests,bs4
res = requests.get('http://xkcd.com')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'lxml')
comic = soup.select('#comic img')
prevlink = soup.select('a[rel="prev"]')
print(prevlink[0].get('href'))