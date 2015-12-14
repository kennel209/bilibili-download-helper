#! /usr/bin/env python3
# coding: utf8

import sys
import os
import re
from html import unescape
from .utils import escape_seps
from .utils import debug,set_debug
from .utils import get_url

DEBUG=False

def extract_bilibili(data):
    u'''使用re解析html，获取title和index'''

    titles = []
    # 非贪婪搜索
    title_pattern = re.compile(r'<h1\s+title="([^"]+?)">')
    title_match = title_pattern.search(data)
    if title_match:
        title = title_match.group(1)
        # unquote html entities
        title = unescape(title.strip())
        # replace / to _
        title = escape_seps(title)
    else:
        title = ""
    titles.append(title)

    index = 0
    # 非贪婪搜索
    text_pattern = re.compile(r'<div id="plist">(.*?)</div>',re.S)
    text_match = text_pattern.search(data)
    if text_match:
        #debug(text_match.groups())
        parts_data = text_match.group(1)
        index = parts_data.count(r"<option")
    debug(index)

    # have multi pages
    page_pattern = re.compile(r'<option.*?>(.*?)</option>')
    id_pattern = re.compile(r"^\d+、\s*")
    if index > 0:
        for page_match in page_pattern.finditer(parts_data):
            page_title = page_match.group(1)
            # unquote html entities
            page_title = unescape(page_title.strip())
            # replace / to _
            page_title = escape_seps(page_title)
            # delete bilibli page prefix
            page_title = id_pattern.sub("",page_title)
            titles.append(page_title)

    debug(titles)

    return titles,index

def extract_info(url):
    u'''info extract wrapper'''
    data = get_url(url)
    title,index = extract_bilibili(data)

    return title,index

if __name__=="__main__":
    pass

