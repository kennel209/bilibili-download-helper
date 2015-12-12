#! /usr/bin/env python3
# coding: utf8

import sys
import os
from urllib.request import urlopen
from urllib.error import URLError
from html import unescape
import gzip
import re

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag

def get_url(url,encoding='utf-8'):
    u'''urlopen to getdata'''
    try:
        r = urlopen(url)
        debug((r.geturl(),r.status,r.reason))
        if r.status == 200:
            data = r.read()
            # gzip to decompress
            comp = r.getheader("Content-Encoding")
            if "gzip" == comp:
                data = gzip.decompress(data)
            # b'string' -> 'string'
            data_u = data.decode(encoding)
            #debug(data_u)
            return data_u
        else:
            print(r.status,r.reason,"OPEN URL ERROR")
            sys.exit(1)
    except URLError as err:
        print(err)
        sys.exit(1)

def extract_bilibili(data):
    u'''使用re解析html，获取title和index'''

    title = ""
    # 非贪婪搜索
    title_pattern = re.compile(r'<h1\s+title="([^"]+?)">')
    title_match = title_pattern.search(data)
    if title_match:
        title = title_match.group(1)
        # unquote html entities
        title = unescape(title.strip())
    debug(title)

    index = 0
    # 非贪婪搜索
    text_pattern = re.compile(r'<div id="plist">(.*?)</div>',re.S)
    text_match = text_pattern.search(data)
    if text_match:
        #debug(text_match.groups())
        index = text_match.group(1).count(r"<option")
    debug(index)

    return title,index

def extract_info(url):
    u'''info extract wrapper'''
    data = get_url(url)
    title,index = extract_bilibili(data)

    return title,index

if __name__=="__main__":
    pass

