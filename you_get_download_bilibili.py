#! /usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
from you_get_downlist_helper import generate_urls
import you_get_json_handler
import you_get_downloader
import re

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)
        
def extract_index(s,regex=r"index_(\d+)"):
    u'''获取自动命名index'''
    pattern = re.compile(regex)
    res = pattern.search(s)
    if res is not None:
        return res.group(1)
    print("ERROR in extract INDEX, EXIT")
    sys.exit(1)

def do_work(args,info_extract=print,downloader=None):
    u'''主函数，批量生成url，使用下载器下载'''
    url_gen = generate_urls(args.baseurl,args.range,args.start)
    name_prefix = args.prefix
    for url in url_gen:
        info = info_extract(url)
        
        # 根据不同情况生成文件名
        ext = info[1]
        index = extract_index(url)
        if name_prefix == "":
            filename = index
        elif args.fixed_prefix:
            filename = name_prefix
        else:
            filename = "_".join([name_prefix,index])
        file_name = ".".join([filename,ext])
        debug("{} -> {}".format(url,file_name))

        # 模拟执行，展示信息
        if args.dry_run:
            debug(info)
            print("{} -> {}".format(url,file_name))
            continue

        #debug(info)
        # TODO 单P多分段支持
        if len(info[0]) != 1:
            print("NOT IMPLENTED MultiURL part")
            sys.exit(1)
            raise NotImplemented

        downloader.download(info[0][0],filename=file_name)
            
def main():
    u'''解析命令行参数'''

    parser = argparse.ArgumentParser()
    parser.add_argument("baseurl", 
                        help="bash to generate bilibi urls")
    parser.add_argument("-i","--range", 
                        type=int, 
                        default=1,
                        help="range to generate, 1 to index")
    parser.add_argument("-s","--start", 
                        type=int, 
                        default=1,
                        help="start point , int, Default: +1")
    parser.add_argument("-o","--prefix", 
                        default="", 
                        help="output filename prefix")
    parser.add_argument("-d","--downloader", 
                        default="aria2", 
                        help="external downloader, default aria2, [aria2,wget,fake]")
    parser.add_argument("-f","--fixed-prefix", 
                        action="store_true", 
                        help="fixed filename, do not use index to auto rename. NO effect if prefix NOT set")
    parser.add_argument("-n","--dry-run", 
                        action="store_true", 
                        help="just print info, do not actually downdloading")
    parser.add_argument("-v","--verbose", 
                        action="store_true", 
                        help="more info")
    
    args = parser.parse_args()

    # 调试模式全局变量
    global DEBUG
    DEBUG = args.verbose
    you_get_json_handler.DEBUG = args.verbose
    you_get_downloader.DEBUG = args.verbose
    
    debug(args)

    # url采集函数和下载器
    extractor = you_get_json_handler.handler
    downloader = you_get_downloader.DOWNLOADERS[args.downloader]

    do_work(args,extractor,downloader)
    

if __name__=="__main__":
    main()

