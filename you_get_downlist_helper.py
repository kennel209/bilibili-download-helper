#! /usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
from urllib.parse import *

def generate_urls(baseurl,indexs,index_modify=1,path_pattern="index_{:02d}.html"):
    u'''生成url播放列表'''
    for i in range(indexs):
        yield urljoin(baseurl,path_pattern.format(i+index_modify))

def handle_url(args,func=print):
    urlgen = generate_urls(args.baseurl, args.index, args.modify, args.pattern)
    for url in urlgen:
        func(url)

def main():
    u'''解析命令行'''
    parser = argparse.ArgumentParser()
    parser.add_argument("baseurl", help="baseurl to build URLS")
    parser.add_argument("index", help="range to generate, 1 to index", type=int)
    parser.add_argument("-p","--pattern", default="index_{:02d}.html",help="python format pattern. Default: 'index_{:02d}.html'")
    parser.add_argument("-m","--modify", type=int, default=1,help="modifier to index, int, Default: +1")

    args = parser.parse_args()
    handle_url(args)

if __name__ == '__main__':
    main()
    
