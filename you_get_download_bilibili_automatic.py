#! /usr/bin/env python3
# coding: utf8

import sys
import os
from urllib.request import urlopen
from urllib.error import URLError
from html import unescape
import argparse
import gzip
import re
import you_get_download_bilibili

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag
    you_get_download_bilibili.set_debug(flag)

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

def extract_info(data):
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

    index = 1
    # 非贪婪搜索
    text_pattern = re.compile(r'<div id="plist">(.*?)</div>',re.S)
    text_match = text_pattern.search(data)
    if text_match:
        #debug(text_match.groups())
        index = text_match.group(1).count(r"<option")
    if index == 0:
        index = 1
    debug(index)

    return title,index
        
def do_work(args):
    u'''args dispatch'''
    download(args.baseurl,args.dry_run)

def download(baseurl,dry_run):
    u'''use core downloader'''
    url = baseurl
    data = get_url(url)
    title,index = extract_info(data)
    fixed_prefix = True if index == 1 else False

    # print INFO
    print("-"*40)
    print("Title: {}".format(title))
    print("Parts: {}".format(index))
    print("-"*40)
    print("")

    you_get_download_bilibili.download(url,
                                        range=index,
                                        name_prefix=title,
                                        fixed_prefix=fixed_prefix,
                                        dry_run=dry_run)

def main():
    u'''解析命令行参数'''

    parser = argparse.ArgumentParser(description=u'''Bilibili One URL automatic Downloader Via you-get & aria2''')
    parser.add_argument("baseurl", 
                        help="bash to generate bilibili urls")
    parser.add_argument("-n","--dry-run", 
                        action="store_true", 
                        help="just print info, do not actually downdloading")
    parser.add_argument("-v","--verbose", 
                        action="store_true", 
                        help="more info")
    
    args = parser.parse_args()

    # 调试模式全局变量
    set_debug(args.verbose)
    debug(args)
    do_work(args)

    
if __name__=="__main__":
    main()

