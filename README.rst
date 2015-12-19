.. -*- coding: utf-8 -*-

===========================================
bilibili-download-helper
===========================================

:Author: Eric Cai
:Contact: kennel209@gmail.com
:Version: 0.9-alpha
:License: GPL 3

这是什么？
============

只是一个使用 ``aria2`` 加速下载bilibli视频的包装器。

为了支持分段合并转化，你同样需要 ``ffmpeg`` 或者 ``avconv`` 来使用这个脚本。(可选，不然就是一堆flv)

当然还有 ``python3.4`` -_-b

特性
------------

* 批量下载bilibili多P
* 懒人自动模式，自动重命名，建立文件夹，下载全P（可选P）
* 为了方便使用多线程下载（ aria2 ）预设5段5线程5并行任务(-x5 -s5 -j5)
* aria2 多url下载优化
* 对于某P多分段进行并行下载
* 通过 -o DIR/NAME_ROOT 下载到其他目录
* 默认使用原生api解析下载路径（效率高，使用youtube-dl的appkey）
* 支持使用 youtube-dl 或者 you-get 解析下载路径, 可以使用-b 切换
* 通过 libav 支持合并多段（暂时支持合并flv）
* 通过 libav 转化为mp4
* 单线程也可使用wget
* 下载自动化重试N次(默认N=3)

TODO
------------

* 片源选择（mp4 & size展示）

用法例子
-----------

.. code:: console

    # 懒人模式（一键）
    $ ./bilibili_download_helper.py -a http://www.bilibili.com/video/av3316724/

    http://www.bilibili.com/video/av3316724/index_01.html -> 【合集】LoveLive！第二季【bilibili正版】/01 再一次 LoveLive！.mp4
    http://www.bilibili.com/video/av3316724/index_02.html -> 【合集】LoveLive！第二季【bilibili正版】/02 向着胜利前进.mp4
    http://www.bilibili.com/video/av3316724/index_03.html -> 【合集】LoveLive！第二季【bilibili正版】/03 梦想之门扉.mp4
    http://www.bilibili.com/video/av3316724/index_04.html -> 【合集】LoveLive！第二季【bilibili正版】/04 宇宙第一偶像.mp4
    http://www.bilibili.com/video/av3316724/index_05.html -> 【合集】LoveLive！第二季【bilibili正版】/05 全新的自我.mp4
    http://www.bilibili.com/video/av3316724/index_06.html -> 【合集】LoveLive！第二季【bilibili正版】/06 万圣节快乐.mp4
    http://www.bilibili.com/video/av3316724/index_07.html -> 【合集】LoveLive！第二季【bilibili正版】/07 不做些什么的话.mp4
    http://www.bilibili.com/video/av3316724/index_08.html -> 【合集】LoveLive！第二季【bilibili正版】/08 我的愿望.mp4
    http://www.bilibili.com/video/av3316724/index_09.html -> 【合集】LoveLive！第二季【bilibili正版】/09 心之旋律.mp4
    http://www.bilibili.com/video/av3316724/index_10.html -> 【合集】LoveLive！第二季【bilibili正版】/10 μ's.mp4
    http://www.bilibili.com/video/av3316724/index_11.html -> 【合集】LoveLive！第二季【bilibili正版】/11 我们决定的事情.mp4
    http://www.bilibili.com/video/av3316724/index_12.html -> 【合集】LoveLive！第二季【bilibili正版】/12 Last Live.mp4
    http://www.bilibili.com/video/av3316724/index_13.html -> 【合集】LoveLive！第二季【bilibili正版】/13 实现吧！大家的梦想――.mp4

    # 选择区域-s Start／ -i Range ／修正分P前缀 -f
    $ ./bilibili_download_helper.py -a http://www.bilibili.com/video/av1358908/  -s 2 -i 3 -f

    http://www.bilibili.com/video/av1358908/index_02.html -> 【合集】我的妹妹不可能那么可爱 第二季【Bilibili正版】/02 我信任的大哥哪有可能因为沉迷于便携式美少女游戏而来性骚扰我.mp4
    http://www.bilibili.com/video/av1358908/index_03.html -> 【合集】我的妹妹不可能那么可爱 第二季【Bilibili正版】/03 我的朋友哪有可能摘下眼镜.mp4
    http://www.bilibili.com/video/av1358908/index_04.html -> 【合集】我的妹妹不可能那么可爱 第二季【Bilibili正版】/04 我妹妹的对手哪有可能来日本.mp4

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

    usage: bilibili_download_helper.py [-h] [-a] [-f] [-i RANGE] [-s START]
                                       [-o PREFIX] [-t TO_EXT] [-d DOWNLOADER]
                                       [-n] [-b BACKEND] [-v]
                                       baseurl

    A small script to help downloading Bilibily video via you-get & aria2

    positional arguments:
      baseurl               bash to generate bilibili urls

    optional arguments:
      -h, --help            show this help message and exit
      -a, --auto            automatic download all
      -f, --add-index-prefix
                            add index to Page auto naming
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
      -b BACKEND, --backend BACKEND
                            info extractor, default native, [native,youtube-
                            dl,you-get]
      -r RETRY, --retry RETRY
                            retry counts when download failed, default 3
      -v, --verbose         more info
