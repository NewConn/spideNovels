from bs4 import BeautifulSoup
import requests

url = r'https://www.owllook.net/owllook_content?url=http://www.biqudu.com//0_174/1220715.html&name=%E7%AC%AC%E4%B8%80%E7%AB%A0%20%E5%B0%8F%E4%BA%8C%E4%B8%8A%E9%85%92&chapter_url=http://www.biqudu.com/0_174/&novels_name=%E9%9B%AA%E4%B8%AD%E6%82%8D%E5%88%80%E8%A1%8C'
def getHtml(url):
    # head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r
r = getHtml(url)
chap = BeautifulSoup(r.text, 'html.parser')
text = chap.find_all('div', attrs={'id':r'content'})
