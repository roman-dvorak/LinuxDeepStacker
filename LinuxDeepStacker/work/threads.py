#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import sys
import wx
import wx.lib.agw.flatnotebook as wxfnb
import gettext
import time
import datetime
import h5py
import configparser
import numpy as np
import logging
import threading
import Queue

logger = logging.getLogger('main.py')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

gettext.bindtextdomain('cs_CZ')
gettext.textdomain('cs_CZ')
_ = gettext.gettext


class Importer(threading.Thread):
    def __init__(self, input_q, output_q, classes):
        super(Importer, self).__init__()
        self.dir_q = input_q
        self.result_q = output_q
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
            	pass
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Importer, self).join(timeout)



class UiUpdater(threading.Thread):
    def __init__(self, input_q, output_q, classes):
        super(UiUpdater, self).__init__()
        self.dir_q = input_q
        self.result_q = output_q
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
            	pass
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(UiUpdater, self).join(timeout)



class Processer(threading.Thread):
    def __init__(self, input_q, output_q, classes):
        super(Processer, self).__init__()
        self.dir_q = input_q
        self.result_q = output_q
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
            	pass
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Processer, self).join(timeout)


def main(arg):
    while True:
        item = q.get()
        print(item)
        q.task_done()