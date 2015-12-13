#! /usr/bin/env python3
# coding: utf8

import subprocess as sb
import shlex
import sys
from .utils import check_cmd

DEBUG=False

# check command
if not check_cmd('youtube-dl'):
    raise ImportError("Cannot found youtube-dl in Path")

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag

def handler(url):
    u'''打包处理函数'''
    data = handler_command(url)
    info = extract_urls(data)
    return info

def handler_command(url, encoding="utf8"):
    u'''通过 ``youtube-dl -g`` 获得相关下载内容'''
    cmd = "youtube-dl -g " + shlex.quote(url)
    args = shlex.split(cmd)
    debug(args)
    # return output data. -> b'string'
    # 如果下载超时（20s）报错退出
    # TODO 更好的修正下载
    try:
        data = sb.check_output(args,timeout=20)
    except sb.TimeoutExpired as err:
        print("command run timeout")
        print(err)
        sys.exit(1)
    except sb.CalledProcessError as err:
        print("Called Process Error")
        print(err)
        sys.exit(1)
    # 编码转换
    data_u = data.decode(encoding)
    debug(data_u)
    return data_u

def extract_urls(data):
    u'''解析 json 对象， 获取下载url和后缀'''
    debug("extract useful data")
    urls = [l.strip() for l in data.split()]
    debug(urls)
    if ".flv" in urls[0]:
        video_format="flv"

    # TODO dirty return
    return urls,video_format,None

if __name__=="__main__":
    DEBUG=True
    url = "http://www.bilibili.com/video/av1036563/index_04.html"
    url = "http://www.bilibili.com/video/av2807449/index_4.html"
    debug(handler(url))

