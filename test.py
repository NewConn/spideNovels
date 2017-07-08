# coding:utf-8
import requests
from bs4 import BeautifulSoup

def getHtml(url):
    #head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    head = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers = head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r

r = getHtml(r'https://www.owllook.net/chapter?url=http://www.biqudu.com/0_174/&novels_name=%E9%9B%AA%E4%B8%AD%E6%82%8D%E5%88%80%E8%A1%8C')


#print(r.text)
chapter = {}
soup = BeautifulSoup(r.text, 'html.parser')
soup = soup.find_all('dd')
for i in soup:
    href = r'https://www.owllook.net' + i.a['href']
    title = i['title']
    chapter[title] = href
