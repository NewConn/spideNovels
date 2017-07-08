# coding:utf-8
import requests
import time
import random
from lxml import etree
import re
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from multiprocessing import Process
import os


def delay():
    delayTime = random.uniform(1, 3)
    time.sleep(delayTime)


def getHtml(url):
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r


def parasLink(r):
    # lxml-xpath 提取
    # /html/body/div[1]/div/div/div[1]/div[1]/li/a
    # /html/body/div[1]/div/div/div[1]/div[1]/li  /html/body/div[1]/div/div/div[1]/div[1]/li/div[2]/span[2]
    r = etree.HTML(r)
    # if r.xpath(r'/div[1]/div/div/div[1]/div[1]/li/div[2]/span[2]') == '已解析':
    div = r'//div[1]/div/div/div[1]/div[1]/li/a/@href'
    novel_link = r.xpath(div)
    # else:
    #     # 未解析
    #     pass
    domain = r'https://www.owllook.net'
    novel_link = domain + novel_link[0]
    return novel_link


    # BeautifulSoup 提取
    # soup = BeautifulSoup(r, 'html.parser')
    # each_info = soup.find('div', attrs={'class': 'result_item col-sm-9 col-xs-12'})
    # novel_link = each_info.find_all('a')
    # for each in novel_link:
    #     getHtml(each)


def getchapter(index_page):
    chapter = {}
    # # //*[@id="list"]/dl/dd[35]/a
    # # / html / body / div[2] / dl / dd[1] / a
    # index_page = etree.HTML(index_page.content)
    # # div = r'//div[2]/dl/dd[1]/@href'     //*[@id="list"]/dl/dd[13]/a
    # div = r'//*[@id="list"]/dl/dd'
    # chapterList = index_page.xpath(div)
    # for each in chapterList:
    #     each = each.split(r'<a href="')[1]
    #     each = each.split(r'</a></dd>')[0]
    #     href = each.split(r'">')[0]
    #     title = each.split(r'">')[1]
    #     chapter[title] = href
    # return chapter

    # bs解析
    soup = BeautifulSoup(index_page.text, 'html.parser')
    # <div class="container all-chapter">
    # <input id="content_url" type="hidden" value="http://www.biqudu.com/">
    # <input id="url" type="hidden" value="http://www.biqudu.com/0_174/">
    # <input id="novels_name" type="hidden" value="雪中悍刀行">
    source_url = soup.find_all('div', attrs={'class':r'container all-chapte'})
    url = source_url.find_all('input', attrs={'id':'content_url'})

    dd = soup.find_all('dd')
    for i in dd:
        href = r'https://www.owllook.net/owllook_content?url=' +  + i['href']
        title = i['title']
        chapter[title] = href
    return chapter

    # re解析
    # index_page = index_page.text
    # index_page = index_page.replace(' ', '')
    # index_page = index_page.replace('\n', '')
    # for each in range(index_page.count(r'<dd>')):
    #     index_page = index_page.split(r'<dd><ahref="')[1]
    #     index_page = index_page.split(r'</a></dd>')[0]
    #     href = index_page.split(r'">')[0]
    #     title = index_page.split(r'</a></dd>')[0]
    #     chapter[title] = href
    # return chapter

# 2017.7.2 进度到此  for each in range(index_page.count(r'<dd>')):   'int' object has no attribute 'split'

def getText(chapter):
    text = ''
    for title, href in chapter:
        htmlChapter = getHtml(href)
        # // *[ @ id = "BookText"]
        # htmlChapter = etree.HTML(htmlChapter.text)
        # div = r'//*[@id="BookText"]'
        # htmlChapter = htmlChapter.xpath(div)
        # htmlChapter = htmlChapter.replace(r'<p>', "")
        # htmlChapter = htmlChapter.replace(r'</p>', "")
        # htmlChapter = htmlChapter.split(r'<script src=')[0]

        text = text + title + '\n' + htmlChapter + '\n\n'
        # text = htmlChapter
    return text


def save(path, title, text):
    # with open(path + title + '.txt', 'w', encoding='utf-8') as output:
    with open(title + '.txt', 'w', encoding='utf-8') as output:
        output.write(text)


def main(name):
    # 拼接搜索链接
    start_url = r'https://www.owllook.net/search?wd='
    novel_name = name
    link_url = start_url + novel_name

    path = r'./'

    # 获取页面
    r = getHtml(link_url)
    novel_link = parasLink(r.text)
    novel_index_page = getHtml(novel_link)
    chapter = getchapter(novel_index_page)
    text = getText(chapter)
    save(path, novel_name, text)


class Application(Frame):
    def __init__(self, main, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='下载', command=self.download)
        self.alertButton.pack()

    def download(self):
        name = self.nameInput.get()
        # p = Process(target=main, args=(name,))
        # p.start()
        # # main(name)
        # p.join()
        main(name)
        messagebox.showinfo('Message', '%s下载成功！请查看' % name)


app = Application(main)
# 设置窗口标题:
app.master.title('小说下载器')
# 主消息循环:
app.mainloop()

# 雪中悍刀行