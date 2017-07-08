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



def getHtml(url):
    # head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r

