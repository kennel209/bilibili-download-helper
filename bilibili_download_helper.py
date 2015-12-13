#! /usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
from helpers.url_generater import generate_urls, get_url_index
from helpers import downloaders as you_get_downloader
from helpers import bilibili_info_extractor
from helpers import video_process
try:
    from helpers import youtube_dl_handler as url_handler
except ImportError:
    from helpers import you_get_json_handler as url_handler

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag
    url_handler.set_debug(flag)
    you_get_downloader.set_debug(flag)
    video_process.set_debug(flag)

def download(baseurl,
            range_=0,
            start=0,
            name_prefix="",
            info_extract=url_handler.handler,
            downloader=you_get_downloader.Aria2_Downloader,
            dry_run=False,
            to_ext='mp4'):
    u'''主函数，批量生成url，使用下载器下载'''

    # correct start
    if start <= 0:
        start = 1

    if range_ <= 0:
        fixed_prefix = True
        range_ = 1
    else:
        fixed_prefix = False

    url_gen = generate_urls(baseurl,range_,start)
    for url in url_gen:
        info = info_extract(url)

        # 根据不同情况生成文件名
        ext = info[1]
        index = get_url_index(url)
        if index is None:
            print("ERROR in extract INDEX, EXIT")
            sys.exit(1)

        if name_prefix == "":
            filename = index
        elif fixed_prefix:
            filename = name_prefix
        else:
            filename = "_".join([name_prefix,index])

        file_name = ".".join([filename,ext])

        # print INFO
        print("-"*40)
        print("{} -> {}".format(url,file_name))
        print("Split URL part: {}".format(len(info[0])))
        print("-"*40)
        print("")

        if len(info[0]) > 1:
            # 多分段

            # check if file existed
            # treat as downloaded
            if to_ext != ext:
                file_name = ".".join([filename,to_ext])

            if os.path.exists(file_name):
                print("{} has downloaded, skip".format(file_name))
                continue

            parts=[]
            for part,part_url in enumerate(info[0]):
                part_index = "[{:02d}]".format(part)
                part_name = ".".join([filename,part_index,ext])
                parts.append(part_name)

                print("URL part: {} -> {}".format(part_index,part_name))
                if dry_run:
                    continue

                downloader.download(part_url,filename=part_name)

            # POST process, merge & convert

            print("Try Merging: {}".format(file_name))

            if dry_run:
                continue

            result = video_process.merge_video(ext,parts,filename,to_ext)

            # successful merged, delete parts_file
            if result:
                for f in parts:
                    debug("removing {}".format(f))
                    os.remove(f)

        else:
            # 单分段

            # TODO file duplication leave to external_downloader
            if dry_run:
                continue

            # support auto ext converter, check downloaded file
            if to_ext != ext:
                new_name = ".".join([filename,to_ext])
                if os.path.exists(new_name):
                    print("{} has downloaded, skip".format(new_name))
                    continue

            downloader.download(info[0][0],filename=file_name)

            # POST process, convert
            if to_ext != ext:
                old_name = file_name
                file_name = ".".join([filename,to_ext])

                print("Try converting: {} -> {}".format(old_name,file_name))

                result = video_process.merge_video(ext,[old_name],filename,to_ext)

                # successful converted
                if result:
                    debug("removing {}".format(old_name))
                    os.remove(old_name)

        # print INFO
        print("")
        print("-"*40)
        print("Done: {}".format(file_name))
        print("-"*40)
        print("")

def do_work(args):
    u'''分配命令，调用下载主函数'''

    # url采集函数和下载器
    extractor = url_handler.handler
    downloader = you_get_downloader.DOWNLOADERS[args.downloader]

    if args.auto:
        # auto mode
        title,index = bilibili_info_extractor.extract_info(args.baseurl)

        # print INFO
        print("-"*40)
        print("Title: {}".format(title))
        print("Parts: {}".format(1 if index == 0 else index))
        print("-"*40)
        print("")

        # add start selector
        if index == 0:
            # do not worry about single part
            range_ = index
            start = 1
        else:
            start = args.start
            if args.range > 0:
                range_ = args.range
            else:
                range_ = index-start+1

        download(args.baseurl,
                range_=range_,
                start=start,
                name_prefix=title,
                info_extract=extractor,
                downloader=downloader,
                dry_run=args.dry_run,
                to_ext=args.to_ext)

    else:
        # normal mode
        download(args.baseurl,
                range_=args.range,
                start=args.start,
                name_prefix=args.prefix,
                info_extract=extractor,
                downloader=downloader,
                dry_run=args.dry_run,
                to_ext=args.to_ext)


def main():
    u'''解析命令行参数'''

    parser = argparse.ArgumentParser(description=u"A small script to help downloading Bilibily video via you-get & aria2")
    parser.add_argument("baseurl",
                        help="bash to generate bilibili urls")
    parser.add_argument("-a","--auto",
                        action="store_true",
                        help="automatic download all")
    parser.add_argument("-i","--range",
                        type=int,
                        default=0,
                        help="range to generate, 1 to index, 0 for current, no auto naming, default 0")
    parser.add_argument("-s","--start",
                        type=int,
                        default=1,
                        help="start point, int, Default: +1")
    parser.add_argument("-o","--prefix",
                        default="",
                        help="output filename prefix")
    parser.add_argument("-t","--to-ext",
                        default="mp4",
                        help="output file extension, auto converted, default mp4")
    parser.add_argument("-d","--downloader",
                        default="aria2",
                        help="external downloader, default aria2, [aria2,wget,fake]")
    parser.add_argument("-n","--dry-run",
                        action="store_true",
                        help="just print info, do not actually downdloading")
    parser.add_argument("-v","--verbose",
                        action="store_true",
                        help="more info")

    args = parser.parse_args()

    assert args.start >= 1
    assert args.range >= 0

    # 调试模式全局变量
    set_debug( args.verbose)
    debug(args)
    do_work(args)


if __name__=="__main__":
    main()

