#! /usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
from you_get_downlist_helper import generate_urls
import you_get_json_handler
import you_get_downloader
from video_process import merge_video
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
    you_get_json_handler.set_debug(flag)
    you_get_downloader.set_debug(flag)

def extract_index(s,regex=r"index_(\d+)"):
    u'''获取自动命名index'''
    pattern = re.compile(regex)
    res = pattern.search(s)
    if res is not None:
        return res.group(1)
    print("ERROR in extract INDEX, EXIT")
    sys.exit(1)

def download(baseurl,
            range=1,
            start=1,
            name_prefix="",
            info_extract=you_get_json_handler.handler,
            downloader=you_get_downloader.Aria2_Downloader,
            fixed_prefix=False,
            dry_run=False):
    u'''主函数，批量生成url，使用下载器下载'''
    url_gen = generate_urls(baseurl,range,start)
    for url in url_gen:
        info = info_extract(url)
        
        # 根据不同情况生成文件名
        ext = info[1]
        index = extract_index(url)
        if name_prefix == "":
            filename = index
        elif fixed_prefix:
            filename = name_prefix
        else:
            filename = "_".join([name_prefix,index])
        file_name = ".".join([filename,ext])

        print("{} -> {}".format(url,file_name))
        print("Split URL part: {}".format(len(info[0])))

        if len(info[0]) > 1:
            # 多分段
            parts=[]
            for part,part_url in enumerate(info[0]):
                part_index = "[{:02d}]".format(part)
                part_name = ".".join([filename,part_index,ext])
                parts.append(part_name)

                if dry_run:
                    print("URL part: {} -> {}".format(part_index,part_name))
                    continue

                debug("URL part: {} -> {}".format(part_url,part_name))
                downloader.download(part_url,filename=part_name)

            if dry_run:
                print("Try Merging: {}".format(file_name))
                continue

            debug("Try Merging: {}".format(file_name))

            result = merge_video(ext,parts,file_name)
            
            # successful merged, delete parts_file
            if result:
                for f in parts:
                    os.remove(f)

        else:
            # 单分段
            if dry_run:
                continue

            downloader.download(info[0][0],filename=file_name)
            
def do_work(args):
    u'''分配命令，调用下载主函数'''

    # url采集函数和下载器
    extractor = you_get_json_handler.handler
    downloader = you_get_downloader.DOWNLOADERS[args.downloader]

    download(args.baseurl,
            range=args.range,
            start=args.start,
            name_prefix=args.prefix,
            info_extract=extractor,
            downloader=downloader,
            fixed_prefix=args.fixed_prefix,
            dry_run=args.dry_run)


def main():
    u'''解析命令行参数'''

    parser = argparse.ArgumentParser(description=u"A small script to help downloading Bilibily video via you-get & aria2")
    parser.add_argument("baseurl", 
                        help="bash to generate bilibili urls")
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
    set_debug( args.verbose)
    debug(args)
    do_work(args)
    

if __name__=="__main__":
    main()

