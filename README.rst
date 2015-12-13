.. -*- coding: utf-8 -*-

===========================================
bilibili-download-helper
===========================================

:Author: Eric Cai
:Contact: kennel209@gmail.com
:Version: 0.5
:License: GPL 3

这是什么？
============

只是一个使用 ``aria2`` 加速下载bilibli视频的包装器。

你需要保证路径中可以使用 ``youtube-dl`` （优先）或者 ``you-get`` 和 ``aria2c`` 来使用这个脚本。

为了支持分段合并转化，你同样需要 ``ffmpeg`` 或者 ``avconv`` 来使用这个脚本。

当然还有 ``python3.4`` -_-b

特性
------------

* 批量下载bilibili多P
* 为了方便使用多线程下载（ aria2 ）预设5段5线程5并行任务(-x5 -s5 -j5)
* 对于某P多分段进行并行下载
* 通过 -o DIR/NAME_ROOT 下载到其他目录
* 使用 youtube-dl 或者 you-get 解析下载路径
* 通过 libav 支持合并多段（暂时支持合并flv）
* 通过 libav 转化为mp4
* 单线程也可使用wget


TODO
------------

* 自动模式，重命名机制
* 非分p自动化支持
* 自己进行url解析？

用法例子
-----------

.. code:: console

    # 懒人模式（一键）
    # 懒人
    $ ./bilibili_download_helper.py -a http://www.bilibili.com/video/av1242782/

    Title: 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆
    Parts: 5
    http://www.bilibili.com/video/av1242782/index_01.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_01.mp4
    http://www.bilibili.com/video/av1242782/index_02.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_02.mp4
    http://www.bilibili.com/video/av1242782/index_03.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_03.mp4
    http://www.bilibili.com/video/av1242782/index_04.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_04.mp4
    http://www.bilibili.com/video/av1242782/index_05.html -> 【Vmoe字幕组】LiSA LiVE is Smile Always in武道馆_05.mp4

.. code:: console

    # 普通模式（自定义文件名）
    # 单P
    $ ./bilibili_dowload_helper.py http://www.bilibili.com/video/av2149245/

    http://www.bilibili.com/video/av2149245/index_01.html -> 01.mp4

    # 自定义多P
    $ ./bilibili_download_helper.py http://www.bilibili.com/video/av2149245/ -i 2 -s 2 -o "Animelo Summer"

    http://www.bilibili.com/video/av2149245/index_02.html -> Animelo Summer_02.mp4
    http://www.bilibili.com/video/av2149245/index_03.html -> Animelo Summer_03.mp4

    # 多P中某P
    $ ./bilibili_download_helper.py http://www.bilibili.com/video/av2149245/ -s 2 -o "Animelo Summer LIVE"

    http://www.bilibili.com/video/av2149245/index_02.html -> Animelo Summer LIVE.mp4

.. code:: console

    $ ./bilibili_download_helper.py -h

    usage: bilibili_download_helper.py [-h] [-a] [-i RANGE] [-s START] [-o PREFIX]
                                       [-t TO_EXT] [-d DOWNLOADER] [-n] [-v]
                                       baseurl

    A small script to help downloading Bilibily video via you-get & aria2

    positional arguments:
      baseurl               bash to generate bilibili urls

    optional arguments:
      -h, --help            show this help message and exit
      -a, --auto            automatic download all
      -i RANGE, --range RANGE
                            range to generate, 1 to index, 0 for current, no auto
                            naming, default 0
      -s START, --start START
                            start point, int, Default: +1
      -o PREFIX, --prefix PREFIX
                            output filename prefix
      -t TO_EXT, --to-ext TO_EXT
                            output file extension, auto converted, default mp4
      -d DOWNLOADER, --downloader DOWNLOADER
                            external downloader, default aria2, [aria2,wget,fake]
      -n, --dry-run         just print info, do not actually downdloading
      -v, --verbose         more info

