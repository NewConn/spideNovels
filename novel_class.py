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


class novel():
    def __init__(self, name):
        name = self.name

    def getHtml(self):
        head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        r = requests.get(url, headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r

    def parasLink(html):
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
        domain = 'https://www.owllook.net'
        novel_link = domain + novel_link[0]
        return novel_link

    def