#! /usr/bin/env python3
# coding: utf8

import sys
import os
import subprocess
import signal
import time
import shlex
import random
from .utils import check_cmd
from .utils import debug,set_debug

DEBUG=False

class Downloader():
    '''abstract class for Downloader'''
    def __init__(self, urls=None, filenames=None, *args, **kwargs):
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
    def download(urls, filenames):
        for u,f in zip(urls,filenames):
            print("Downloading (fake) {}, save as {} ".format(u,f))
        return True

class Aria2_Downloader(Downloader):
    u'''aria2下载器，通过subprocess模块调用'''
    @staticmethod
    def download(urls, filenames, options="-x5 -s5 -j5 -c --auto-file-renaming=false --daemon=false"):

        # check command
        if not check_cmd('aria2c'):
            print("Cannot found aria2c in Path")
            print("Use wget or you-get directly")
            sys.exit(1)

        # suppress verbose output
        if not DEBUG:
            options = " ".join([options,
                                #"--console-log-level=error",
                                "--summary-interval=0"])

        # 创建并行任务 input_file
        input_file = Aria2_Downloader.make_input_file(urls,filenames,
                        temp_name="."+os.path.basename(filenames[0])+".input")

        cmd = " ".join(["aria2c",options,"-i"])
        cmd = " ".join([cmd,shlex.quote(input_file)])

        args = shlex.split(cmd)
        debug("Downloading (aria2c) {}".format(cmd))

        try:
            proc = subprocess.Popen(args)
            return_code = proc.wait()
            if return_code != 0:
                raise subprocess.CalledProcessError(proc.returncode,proc.args)
        except KeyboardInterrupt as err:
            proc.send_signal(signal.SIGINT)
            # wait for aria2 output
            time.sleep(3)
            print("\nKEYINTERRUPTED in Downloading {}".format(filenames))
            print("Please Try again manually")
            sys.exit(1)
        except subprocess.CalledProcessError as err:
            print(err)
            print("Some Error Occured in Downloading {}".format(filenames))
            #print("Please Try again manually")
            return False
        finally:
            os.remove(input_file)
        return True

    @staticmethod
    def make_input_file(urls, filenames, temp_name='temp.input'):
        u'''write tempfile to generate filelist for aria2'''
        with open(temp_name, 'w') as out:
            for url,filename in zip(urls,filenames):
                if type(url) == type([]):
                    out.write("\t".join(url))
                else:
                    out.write(url)
                out.write('\n\t')
                out.write('out='+filename)
                out.write('\n')

        return temp_name

class Wget_Downloader(Downloader):
    u'''wget下载器，通过subprocess模块调用'''
    @staticmethod
    def download(urls, filenames, options="-c"):

        # check command
        if not check_cmd('wget'):
            print("Cannot found wget in Path")
            print("Use you-get directly")
            sys.exit(1)

        # 依次下载
        for url,filename in zip(urls,filenames):
            if type(url) == type([]):
                # just choose one to download
                url = random.choice(url)

            cmd = " ".join(["wget",options,"-O"])
            cmd = " ".join([cmd,shlex.quote(filename),shlex.quote(url)])
            args = shlex.split(cmd)
            debug("Downloading (wget) {}".format(cmd))

            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError as err:
                print(err)
                print("Some Error Occured in Downloading {}".format(filename))
                print("Please Try again manually")
                return False
        return True

DOWNLOADERS={"fake":Fake_Downloader,
            "aria2":Aria2_Downloader,
            "wget":Wget_Downloader,
            }

if __name__=="__main__":
    DEBUG=True
    Fake_Downloader.download(["abd","EFG"], ["1","2"])

