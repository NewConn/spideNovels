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

# 延迟
def delay():
    delayTime = random.uniform(1, 3)
    time.sleep(delayTime)

# 下载网页
def getHtml(url):
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r

# 解析小说链接
def parasLink(r):

    r = etree.HTML(r)

    div = r'//div[1]/div/div/div[1]/div[1]/li/a/@href'
    novel_link = r.xpath(div)

    domain = r'https://www.owllook.net'
    novel_link = domain + novel_link[0]
    return novel_link

# 解析章节链接
def getchapter(index_page):
    chapter = {}

    # bs解析
    soup = BeautifulSoup(index_page.text, 'html.parser')

    # source_url = soup.find_all('div', class_="container all-chapter")

    content_url = soup.find('input', id="content_url")['value']
    content_url = r'https://www.owllook.net/owllook_content?url=' + content_url

    url = soup.find('input', id="url")['value']

    novels_name = soup.find('input', id="novels_name")['value']

    dd = soup.find_all('dd')
    for i in dd:
        i = str(i)
        i = i.split(r'<dd> <a href="')[1].split(r'</a></dd>')[0]
        # show_url = "owllook_content?url=" + content_url + url + "&name=" + name + "&chapter_url=" + chapter_url + "&novels_name=" + novels_name
        title = i.split(r'">')[1]
        href = content_url + i.split(r'">')[0] + r'&name=' + title + r'&chapter_url=' + url + r'&novels_name=' + novels_name

        chapter[title] = href
    return chapter
# 下载及解析章节内容
def getText(chapter):
    text = ''
    i = 1
    for title, href in chapter.items():
        i = i + 1

        htmlChapter = getHtml(href)
        # // *[ @ id = "BookText"]
        chap = BeautifulSoup(htmlChapter.text, 'html.parser')
        text = chap.find('div', id="content")
        text = str(text)
        text = text.replace(r'[<div id="content"><script>readx();</script>', '')
        text = text.replace(r'<br/>', '')
        # text = text.replace(r'<br/>', '')
        text = title + '\n' + text + '\n\n'
        if i >20:
            return text
    return text

# 保存
def save(path, title, text):
    # with open(path + title + '.txt', 'w', encoding='utf-8') as output:
    with open(title + '.txt', 'w', encoding='utf-8') as output:
        output.write(text)

# 主进程
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

# 图形界面
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
        # main(name)
        # p.join()
        main(name)
        messagebox.showinfo('Message', '%s下载成功！请查看' % name)


app = Application(main)
# 设置窗口标题:
app.master.title('小说下载器')
# 主消息循环:
app.mainloop()

# 雪中悍刀行