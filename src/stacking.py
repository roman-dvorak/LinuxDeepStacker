#!/usr/bin/env python
# -*- coding: utf-8 -*-
# stacking.py

# Copyright (c) 2014-2015, Roman Dvorak, roman-dvorak@email.cz
#


import sys
import os
import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy
import math
import pyfits
import numpy as np
import cv2
import subprocess
import glob
import pygtk
import gtk
import random
import Image
import ImageDraw
from math import sqrt
import datetime





class Stacking(object):
    """docstring for Stacking"""
    def __init__(self, arg):
        super(Stacking, self).__init__()
        self.arg = arg

    def setDataPath(self, root):
        self.root = root

    def setLightFrames(self, LightFrames):
        self.LightFrames = LF

    def setDarkFrames(self, DarkFrames):
        self.DarkFrames = DarkFrames

    def setDarkFrameMaster(self, DarkFrameMaster):
        self.DarkFrameMaster = DarkFrameMaster

    def setBiasFrames(self, BiasFrames):
        self.BiasFrames = BiasFrames

    def setBiasFrameMaster(self, BiasFrameMaster):
        self.BiasFrameMaster = BiasFrameMaster

    def setAlignmentType(self, AlignmentType):
        self.AlignmentType = AlignmentType

    def setAlignmentPoints(self, AlignmentPoints):
        self.AlignmentPoints = AlignmentPoints



    def Mean(self):
        print "Průměr sčítání"

        image = cv2.imread(self.LightFrames[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)
        print image.shape, image.dtype
        print image.shape
        rows, cols, ch = image.shape
        
        for rawIndex in range(0,len(self.LightFrames)):
            print "počítá se obr:", rawIndex, "což je:", self.LightFrames[rawIndex]
            image2 = cv2.imread(self.LightFrames[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(numpy.uint16)
            M = cv2.getAffineTransform(self.AlignmentPoints[rawIndex],self.AlignmentPoints[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            image = cv2.addWeighted(image,1,image2, (math.ceil(1.00/(len(self.LightFrames)-1.00) * 100.00) / 100.00) ,0)

        cv2.imwrite('processed.tif',image )
        print "ukládání vysledneho obr"
        plt.show()

    def Median(self):
        print "Median Stacking High memory"

        image = cv2.imread(self.LightFrames[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)

        DC = False
        if os.path.isfile(self.root+"/LDS_data/tmp/df_master.ppm"):
            imageDC = cv2.imread(self.root+"/LDS_data/tmp/df_master.ppm", cv2.IMREAD_UNCHANGED)
            imageDC = image.astype(numpy.uint16)
            DC = True
        print image.shape, image.dtype
        rows, cols, ch = image.shape
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='w+', shape=(len(self.LightFrames),rows, cols, ch))
        data.flush()
        del data

        for rawIndex in range(0,len(self.LightFrames)):
            data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.LightFrames),rows, cols, ch))
            print "Získává se obr:", rawIndex, "což je:", self.LightFrames[rawIndex]
            image2 = cv2.imread(self.LightFrames[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(np.uint16)
            if DC:
                image2 = cv2.subtract(image2, imageDC)
            M = cv2.getAffineTransform(self.AlignmentPoints[rawIndex],self.AlignmentPoints[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            data[rawIndex]=image2
            data.flush()
            del data

        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.LightFrames),rows, cols, ch))

        for row in range(0,rows):
            print row, " of ", rows
            for col in range(0,cols):
                image.itemset((row,col,0),np.median(data [0:12,row,col,0]))
                image.itemset((row,col,1),np.median(data [0:12,row,col,1]))
                image.itemset((row,col,2),np.median(data [0:12,row,col,2]))

        now = datetime.datetime.now()
        print now.strftime("%Y-%m-%dT%H:%M")

        image = image.astype(numpy.uint16)
        cv2.imwrite(self.root+"/LDS_data/OUT/"+now.strftime("%Y-%m-%dT%H:%M")+"_median.tiff",image )
        print "ukládání výsledného obr"
        del data


    def Max(self):
        print "Maximum Stacking High memory"

        image = cv2.imread(self.LightFrames[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)

        DC = False
        if os.path.isfile(self.root+"/LDS_data/tmp/df_master.ppm"):
            imageDC = cv2.imread(self.root+"/LDS_data/tmp/df_master.ppm", cv2.IMREAD_UNCHANGED)
            imageDC = image.astype(numpy.uint16)
            DC = True
        print image.shape, image.dtype
        rows, cols, ch = image.shape
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='w+', shape=(len(self.LightFrames),rows, cols, ch))
        data.flush()
        del data

        for rawIndex in range(0,len(self.LightFrames)):
            data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.LightFrames),rows, cols, ch))
            print "Získává se obr:", rawIndex, "což je:", self.LightFrames[rawIndex]
            image2 = cv2.imread(self.LightFrames[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(np.uint16)
            if DC:
                image2 = cv2.subtract(image2, imageDC)
            M = cv2.getAffineTransform(self.AlignmentPoints[rawIndex],self.AlignmentPoints[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            data[rawIndex]=image2
            data.flush()
            del data

        print "MaxCalc"
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.LightFrames),rows, cols, ch))

        for row in range(0,rows):
            print row, " of ", rows
            for col in range(0,cols):
                image.itemset((row,col,0),np.amax(data [0:12,row,col,0]))
                image.itemset((row,col,1),np.amax(data [0:12,row,col,1]))
                image.itemset((row,col,2),np.amax(data [0:12,row,col,2]))

        now = datetime.datetime.now()
        print now.strftime("%Y-%m-%dT%H:%M")

        image = image.astype(numpy.uint16)
        cv2.imwrite(self.root+"/LDS_data/OUT/"+now.strftime("%Y-%m-%dT%H:%M")+"_max.tiff",image )
        print "ukládání výsledného obr"
        del data

        