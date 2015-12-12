.. -*- coding: utf-8 -*-

===========================================
you-get-downloader-helper
===========================================

:Author: Eric Cai
:Contact: kennel209@gmail.com
:Version: 0.3
:License: GPL 3

这是什么？
============

you_get_download_bilibili.py
只是一个使用 ``you-get`` 和 ``aria2`` 下载的包装器。

你需要保证路径中可以使用 ``you-get`` 和 ``aria2c`` 来使用这个脚本。

为了支持分段合并转化，你同样需要 ``ffmpeg`` 或者 ``avconv`` 来使用这个脚本。

当然还有 ``python3.4`` -_-b

特性
------------

* 为了方便使用多线程下载（ aria2 ）预设10段10线程(-x 10 -s 10)
* 单线程也可使用wget
* 批量下载bilibili多P
* 通过 libav 支持合并多段（暂时支持合并flv）
* 通过 libav 转化为mp4

TODO
------------

* 更多合并格式
* 更多option支持
* 直接you-get集成（PR）

用法
------------

.. code:: console

    # 多P
    $ ./you_get_download_bilibili.py URL -i RANGE -o SAVE_FILE_NAME_PREFIX

    # 单P
    $ ./you_get_download_bilibili.py URL -f -o SAVE_FILE_NAME

    # help
    $ ./you_get_download_bilibili.py -h

    usage: you_get_download_bilibili.py [-h] [-i RANGE] [-s START] [-o PREFIX]
                                        [-d DOWNLOADER] [-f] [-t TO_EXT] [-n] [-v]
                                        baseurl

    A small script to help downloading Bilibily video via you-get & aria2

    positional arguments:
      baseurl               bash to generate bilibili urls

    optional arguments:
      -h, --help            show this help message and exit
      -i RANGE, --range RANGE
                            range to generate, 1 to index
      -s START, --start START
                            start point, int, Default: +1
      -o PREFIX, --prefix PREFIX
                            output filename prefix
      -d DOWNLOADER, --downloader DOWNLOADER
                            external downloader, default aria2, [aria2,wget,fake]
      -f, --fixed-prefix    fixed filename, do not use index to auto rename. NO
                            effect if prefix NOT set
      -t TO_EXT, --to-ext TO_EXT
                            output file extension, auto converted, default mp4
      -n, --dry-run         just print info, do not actually downdloading
      -v, --verbose         more info

用法例子
-----------

.. code:: console

    $ ./you_get_download_bilibili.py http://www.bilibili.com/video/av2149245/

    http://www.bilibili.com/video/av2149245/index_01.html -> 01.flv

    $ ./you_get_download_bilibili.py http://www.bilibili.com/video/av2149245/ -i 2 -o "Animelo Summer"

    http://www.bilibili.com/video/av2149245/index_01.html -> Animelo Summer_01.flv
    http://www.bilibili.com/video/av2149245/index_02.html -> Animelo Summer_02.flv

    $ ./you_get_download_bilibili.py http://www.bilibili.com/video/av2149245/ -f -s 2 -o "Animelo Summer LIVE"

    http://www.bilibili.com/video/av2149245/index_02.html -> Animelo Summer LIVE.flv

.. code:: console

    $ ./you_get_download_bilibili.py -a http://www.bilibili.com/video/av1242782/

    Title: 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆
    Parts: 5
    http://www.bilibili.com/video/av1242782/index_01.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_01.flv
    http://www.bilibili.com/video/av1242782/index_02.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_02.flv
    http://www.bilibili.com/video/av1242782/index_03.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_03.flv
    http://www.bilibili.com/video/av1242782/index_04.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_04.flv
    http://www.bilibili.com/video/av1242782/index_05.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_05.flv


