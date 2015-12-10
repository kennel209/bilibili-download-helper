#! /usr/bin/env python3
# coding: utf8

import sys
import os

import subprocess
import shlex

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag

class Downloader():
    '''abstract class for Downloader'''
    def __init__(self, url="", filename="", *args, **kwargs):
        self.url = url
        self.filename = filename
        self.args=args
        self.kwargs=kwargs

    @staticmethod
    def download(url, filename):
        raise NotImplemented

class Fake_Downloader(Downloader):
    u'''用于输出调试的下载器，仅仅打印下载内容'''
    @staticmethod
    def download(url, filename):
        print("Downloading (fake) {}, save as {} ".format(url,filename))

class Aria2_Downloader(Downloader):
    u'''aria2下载器，通过subprocess模块调用'''
    @staticmethod
    def download(url, filename, options="-x 10 -s 10 -c --auto-file-renaming=false --daemon=false"):
        # TODO 解析OPTIONS
        cmd = " ".join(["aria2c",options,"--out"])
        cmd = " ".join([cmd,shlex.quote(filename),shlex.quote(url)])
        args = shlex.split(cmd)
        debug("Downloading (aria2c) {}".format(cmd))
        # TODO 异常处理
        subprocess.call(args)

class Wget_Downloader(Downloader):
    u'''wget下载器，通过subprocess模块调用'''
    @staticmethod
    def download(url, filename, options="-c"):
        # TODO 解析OPTIONS
        cmd = " ".join(["wget",options,"-O"])
        cmd = " ".join([cmd,shlex.quote(filename),shlex.quote(url)])
        args = shlex.split(cmd)
        debug("Downloading (wget) {}".format(cmd))
        # TODO 异常处理
        subprocess.call(args)

DOWNLOADERS={"fake":Fake_Downloader,
            "aria2":Aria2_Downloader,
            "wget":Wget_Downloader,
            }

if __name__=="__main__":
    DEBUG=True
    Fake_Downloader.download("abd","EFG")

