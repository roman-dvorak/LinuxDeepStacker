#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LDS.py

# Copyright (c) 2014-2015, Roman Dvorak, roman-dvorak@email.cz
#


import sys
import os
#from netpbmfile import *
import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy
import math
import pyfits
import numpy as np
import cv2
#from SimpleCV import *
#import cv2.cv as cv
import subprocess
import glob
import pygtk
import gtk
import random
import Image
import ImageDraw
#from skimage import data
#from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
#from skimage.color import rgb2gray
#from skimage import exposure
#from skimage.restoration import denoise_tv_chambolle, denoise_bilateral
import datetime
import stacking
import rawpy


#
#
#   sudo apt-get install python-matplotlib
#   sudo apt-get install python-scipy
#   sudo apt-get install python-pyfits
#   sudo apt-get install python-opencv
#   sudo apt-get install python-pip
#   ##sudo apt-get install dcraw##
#   sudo apt-get install libraw-dev
#   sudo pip install rawpy
#
#




class Aligmen(gtk.Window):

    def __init__(self):
        #mymodule.sayhi()
        self.SnapshotMessage=0
        self.ImgSource=False
        self.ClickNum=0
        self.ImgPath=""
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title("LiveSJ.__init__")
        self.move(100,100)
        self.set_size_request(450, gtk.ICON_SIZE_MENU+500+gtk.ICON_SIZE_MENU)
        self.kostra = gtk.VBox(homogeneous=False, spacing=2)
        self.add(self.kostra)
        self.wievScale = 100
        

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        self.kostra.pack_start(self.toolbar, False, False)

        self.show_all()

    def spust(self):
        play = False

        self.statusbar = gtk.Statusbar()
        self.kostra.pack_end(self.statusbar, False, False, 0)
        context_id = self.statusbar.get_context_id("ident")
        self.statusbar.push(context_id, "1called Write")

        self.toolbar_item01 = gtk.ToolButton("Quit")
        self.toolbar_item01.set_stock_id(gtk.STOCK_QUIT)
        self.toolbar_item01.connect("clicked", exit)
        self.toolbar.insert(self.toolbar_item01,0)

        self.toolbar_item02 = gtk.ToolButton("První")
        self.toolbar_item02.set_stock_id(gtk.STOCK_GOTO_FIRST)
        self.toolbar_item02.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item02,1)

        self.toolbar_item03 = gtk.ToolButton("Předchozí")
        self.toolbar_item03.set_stock_id(gtk.STOCK_GO_BACK)
        self.toolbar_item03.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item03,2)

        self.toolbar_item04 = gtk.ToolButton("Další")
        self.toolbar_item04.set_stock_id(gtk.STOCK_GO_FORWARD)
        self.toolbar_item04.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item04,3)

        self.toolbar_item05 = gtk.ToolButton("Poslední")
        self.toolbar_item05.set_stock_id(gtk.STOCK_GOTO_LAST)
        self.toolbar_item05.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item05,4)

        self.toolbar_item06 = gtk.ToolButton("pixel")
        self.toolbar_item06.set_stock_id(gtk.STOCK_ZOOM_100)
        self.toolbar_item06.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item06,5)

        self.toolbar_item07 = gtk.ToolButton("CelyObr")
        self.toolbar_item07.set_stock_id(gtk.STOCK_ZOOM_FIT)
        self.toolbar_item07.connect("clicked", self.ChangeIMG)
        self.toolbar.insert(self.toolbar_item07,6)

        self.toolbar_item08 = gtk.ToolButton("OK")
        self.toolbar_item08.set_stock_id(gtk.STOCK_APPLY)
        self.toolbar_item08.connect("clicked", self.ProcesChoose)
        self.toolbar.insert(self.toolbar_item08,7)

        self.toolbar_item09 = gtk.ToolButton("SnapshotRAW")
        self.toolbar_item09.set_stock_id(gtk.STOCK_PRINT)
        #self.toolbar_item09.connect("clicked", self.MakeSnap,2)
        self.toolbar.insert(self.toolbar_item09,8)

        self.toolbar_item10 = gtk.ToolButton("darkframe")
        self.toolbar_item10.set_stock_id(gtk.STOCK_EXECUTE)
        self.toolbar_item10.connect("clicked", self.DFMasterMean)
        self.toolbar.insert(self.toolbar_item10,9)

        self.toolbar_item11 = gtk.ToolButton("darkframe")
        self.toolbar_item11.set_stock_id(gtk.STOCK_PREFERENCES)
        self.toolbar_item11.connect("clicked", self.Setting)
        self.toolbar.insert(self.toolbar_item11,10)
        
        adjV = gtk.Adjustment(1, 1, 120, 1, 1, 0)
        adjH = gtk.Adjustment(1, 1, 120, 1, 1, 0)

        self.IMGkostra = gtk.HBox()
        self.kostra.pack_end(self.IMGkostra, True, True,0)
        self.scrollImgA = gtk.ScrolledWindow(adjH, adjV)
        self.IMGkostra.pack_start(self.scrollImgA, True, True)
        self.eventboxA = gtk.EventBox()
        self.scrollImgA.add_with_viewport(self.eventboxA)
        self.imageA = gtk.Image()
        self.eventboxA.add(self.imageA)

        self.scrollImgB = gtk.ScrolledWindow(adjH, adjV)
        self.IMGkostra.pack_start(self.scrollImgB, True, True)
        self.eventboxB = gtk.EventBox()
        self.eventboxB.connect("button_press_event", self.LableIMG)
        self.scrollImgB.add_with_viewport(self.eventboxB)
        self.imageB = gtk.Image()
        self.eventboxB.add(self.imageB)


        if os.path.isfile(self.root+"/LDS_data/tmp/AligmenPositions.npy") :
            self.AligmenPositions = np.load(self.root+"/LDS_data/tmp/AligmenPositions.npy")
            print "načítání pole:"
            print self.AligmenPositions
            if len(self.AligmenPositions) != len(self.raw_files):
                print "rozdílná délka:", len(self.AligmenPositions), len(self.raw_files)
                # TODO: resize array
                self.AligmenPositions.resize((len(self.raw_files),3,2))
        else:
            self.AligmenPositions=np.zeros((len(self.raw_files),3,2), dtype=numpy.float32)

        self.show_all()


    def Setting(self, widget):
        self.setWindow = gtk.Window()
        self.setWindow.set_position(gtk.WIN_POS_CENTER)
        self.setWindow.set_size_request(400, 200)
        self.setWindow.set_title("Setting")
        self.setWindow.show()

    def StackMean(self):
        print "Normální sčítání"

        image = cv2.imread(self.raw_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)
        print image.shape, image.dtype
        print image.shape
        rows, cols, ch = image.shape
        
        for rawIndex in range(0,len(self.raw_files)):
            image2 = cv2.imread(self.raw_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(numpy.uint16)

            print "počítá se obr:", rawIndex, "což je:", self.raw_files[rawIndex]
            print image2.min(), image2.max(), image2.mean(), image2.ptp(), (math.ceil(1.00/(len(self.raw_files)-1.00) * 100.00) / 100.00)

            M = cv2.getAffineTransform(self.AligmenPositions[rawIndex],self.AligmenPositions[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            image = cv2.addWeighted(image,1,image2, (math.ceil(1.00/(len(self.raw_files)-1.00) * 100.00) / 100.00) ,0)


        plt.subplot(111),plt.imshow(image),plt.title('Output')
        image = image.astype(numpy.uint16)
        cv2.imwrite('processed.tiff',image )
        print "Vysledek"
        print image2.min(), image2.max(), image2.mean(), image2.ptp()
        print "ukládání posledního obr"
        plt.show()


    def DFMasterMean(self, widget=None):
        DF_files = sorted(glob.glob(self.root+"/LDS_data/DarkFrames/*.CR2"))
        i = 0
        for DF in DF_files:
            i = i+1
            raw = rawpy.imread(DF)
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16, user_flip=0, user_wb=[0,0,0,0])
            cv2.imwrite(root+"/LDS_data/tmp/df_%02d.tiff" % i,rgb)
            print "prevod souboru:", i, " z ", len(DF_files)," -- ", DF
        DF_files = sorted(glob.glob(self.root+"/LDS_data/tmp/df_*.tiff"))

        image = cv2.imread(DF_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)
        rows, cols, ch = image.shape
        
        for rawIndex in range(0,len(DF_files)-1):
            print "počítá se obr:", rawIndex, " z ", len(DF_files)-1, "což je:", DF_files[rawIndex]
            image2 = cv2.imread(DF_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(numpy.uint16)
            image = cv2.addWeighted(image,1,image2, (math.ceil(1.00/(len(DF_files)-1.00) * 100.00) / 100.00) ,0)

        image = image.astype(numpy.uint16)
        cv2.imwrite(root+"/LDS_data/tmp/df_master.tiff", image, cv2.CV_IMWRITE_PXM_BINARY)
        plt.show()



    def StackMedian(self):
        print "Median Stacking High memory"

        image = cv2.imread(self.raw_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)

        DC = False
        if os.path.isfile(self.root+"/LDS_data/tmp/df_master.tiff"):
            imageDC = cv2.imread(self.root+"/LDS_data/tmp/df_master.tiff", cv2.IMREAD_UNCHANGED)
            imageDC = image.astype(numpy.uint16)
            DC = True
        print image.shape, image.dtype
        rows, cols, ch = image.shape
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='w+', shape=(len(self.raw_files),rows, cols, ch))
        data.flush()
        del data

        for rawIndex in range(0,len(self.raw_files)):
            data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.raw_files),rows, cols, ch))
            print "Získává se obr:", rawIndex, "což je:", self.raw_files[rawIndex]
            image2 = cv2.imread(self.raw_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(np.uint16)
            if DC:
                image2 = cv2.subtract(image2, imageDC)
            M = cv2.getAffineTransform(self.AligmenPositions[rawIndex],self.AligmenPositions[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            #image = np.concatenate((image,image2))
            data[rawIndex]=image2
            #image[rawIndex] = image2.astype(numpy.uint16)
            #image = cv2.add(image,image2)
            data.flush()
            del data

        print "medianCalc"
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.raw_files),rows, cols, ch))
        # [imrg][w][h][ch]
        print data[0][3096][2764][1]
        print data[1][3096][2764][1]
        print data[2][3096][2764][1]

        
        print data [0:12,3096,2764,:].transpose()
        print type(data [0:12,3096,2764,:].transpose())
        print data [0:12,3096,2764,0]
        print np.median(data [0:12,3096,2764,:].transpose())

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


    def StackMax(self):
        print "Maximum Stacking High memory"

        image = cv2.imread(self.raw_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)

        DC = False
        if os.path.isfile(self.root+"/LDS_data/tmp/df_master.tiff"):
            imageDC = cv2.imread(self.root+"/LDS_data/tmp/df_master.tiff", cv2.IMREAD_UNCHANGED)
            imageDC = image.astype(numpy.uint16)
            DC = True
        print image.shape, image.dtype
        rows, cols, ch = image.shape
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='w+', shape=(len(self.raw_files),rows, cols, ch))
        data.flush()
        del data

        for rawIndex in range(0,len(self.raw_files)):
            data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.raw_files),rows, cols, ch))
            print "Získává se obr:", rawIndex, "což je:", self.raw_files[rawIndex]
            image2 = cv2.imread(self.raw_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(np.uint16)
            if DC:
                image2 = cv2.subtract(image2, imageDC)
            M = cv2.getAffineTransform(self.AligmenPositions[rawIndex],self.AligmenPositions[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            data[rawIndex]=image2
            data.flush()
            del data

        print "MaxCalc"
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.raw_files),rows, cols, ch))
        # [imrg][w][h][ch]
        print data[0][3096][2764][1]
        print data[1][3096][2764][1]
        print data[2][3096][2764][1]

        
        print data [0:12,3096,2764,:].transpose()
        print type(data [0:12,3096,2764,:].transpose())
        print data [0:12,3096,2764,0]
        print np.median(data [0:12,3096,2764,:].transpose())

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

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
    def ProcesChoose(self, widget):
        np.save(self.root+"/LDS_data/tmp/AligmenPositions.npy",self.AligmenPositions)
        #self.DFMasterMean()
        #self.StackMean()
        self.StackMedian()
        #self.StackMax()


    def ChangeIMG(self, widget):
        self.ClickNum=0
        red = (255,80,80)


        if widget == self.toolbar_item06: # 1ku 1
            print "nastavit na celou obrazovku"
            #self.IMGB = len(self.raw_files)-1
            #self.SetImageB(self.raw_files[self.IMGB


        elif widget == self.toolbar_item07: # 1ku 1
            print "nastavit 1:1"
            #self.IMGB = len(self.raw_files)-1
            #self.SetImageB(self.raw_files[self.IMGB])

        elif widget == self.toolbar_item04: # další btn
            if self.IMGB != len(self.raw_files)-1:
                self.IMGB = self.IMGB+1
                self.SetImageB(self.raw_files[self.IMGB])
            else:
                print "Jses na posledním obrazku"

        elif widget == self.toolbar_item03: # předchozi btn
            if self.IMGB != 0:
                self.IMGB = self.IMGB-1
                self.SetImageB(self.raw_files[self.IMGB])
            else:
                print "Jses na prvním obrazku"

        elif widget == self.toolbar_item02: # prvni btn
            self.IMGB = 0
            self.SetImageB(self.raw_files[self.IMGB])

        elif widget == self.toolbar_item05: # posledni btn
            self.IMGB = len(self.raw_files)
            self.SetImageB(self.raw_files[self.IMGB])

        img = cv2.imread(self.raw_files[self.IMGB])

        cv2.circle(img, (int(self.AligmenPositions[self.IMGB][0][0]), int(self.AligmenPositions[self.IMGB][0][1])), 10, red)
        cv2.circle(img, (int(self.AligmenPositions[self.IMGB][1][0]), int(self.AligmenPositions[self.IMGB][1][1])), 10, red)
        cv2.circle(img, (int(self.AligmenPositions[self.IMGB][2][0]), int(self.AligmenPositions[self.IMGB][2][1])), 10, red)

        self.imageB.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))


    def LableIMG(self, widget, event):
        if event.button == 1:
            self.AligmenPositions[self.IMGB][self.ClickNum]=[event.x, event.y]
            self.ClickNum= self.ClickNum + 1
            red = (255,80,80)
            if self.ClickNum == 3:
                print self.AligmenPositions
                print "Poslední bod - při dalším klknití se bude označovat od začátku"
                self.ClickNum = 0
                if self.IMGB == 0:
                    red = (255,80,80)
                    img = cv2.imread(self.raw_files[0])
                    cv2.circle(img, (int(self.AligmenPositions[0][0][0]), int(self.AligmenPositions[0][0][1])), 10, red)
                    cv2.circle(img, (int(self.AligmenPositions[0][1][0]), int(self.AligmenPositions[0][1][1])), 10, red)
                    cv2.circle(img, (int(self.AligmenPositions[0][2][0]), int(self.AligmenPositions[0][2][1])), 10, red)
                    cv2.line(img, (int(self.AligmenPositions[0][0][0]),int(self.AligmenPositions[0][0][1])),(int(self.AligmenPositions[0][1][0]),int(self.AligmenPositions[0][1][1])), red)
                    cv2.line(img, (int(self.AligmenPositions[0][1][0]),int(self.AligmenPositions[0][1][1])),(int(self.AligmenPositions[0][2][0]),int(self.AligmenPositions[0][2][1])), red)
                    cv2.line(img, (int(self.AligmenPositions[0][2][0]),int(self.AligmenPositions[0][2][1])),(int(self.AligmenPositions[0][0][0]),int(self.AligmenPositions[0][0][1])), red)

                    
                    self.imageA.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))


            img2 = cv2.imread(self.raw_files[self.IMGB])
            cv2.circle(img2, (int(self.AligmenPositions[self.IMGB][0][0]), int(self.AligmenPositions[self.IMGB][0][1])), 10, red)
            cv2.circle(img2, (int(self.AligmenPositions[self.IMGB][1][0]), int(self.AligmenPositions[self.IMGB][1][1])), 10, red)
            cv2.circle(img2, (int(self.AligmenPositions[self.IMGB][2][0]), int(self.AligmenPositions[self.IMGB][2][1])), 10, red)

            self.imageB.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img2, gtk.gdk.COLORSPACE_RGB, 8))



    def SetImageA(self, pathTotiff):
        img = cv2.imread(pathTotiff)
        self.imageA.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))

    def SetImageB(self, pathTotiff):
        img = cv2.imread(pathTotiff)
        self.imageB.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))

    def  done(self):
        gtk.main()


def main():
    print "main načteno"
    root = sys.argv[1]
    raw_files = sorted(glob.glob(root+"/LDS_data/StackImages/*.CR2"))
    print raw_files
    i=0
    for raw in raw_files:
        i = i+1
        try:
            #os.popen("dcraw -6 -c -W -t 0 "+raw+" > "+root+"/LDS_data/tmp/sXi_%02d.ppm" % i)     #dcraw -6 -c -W IMG_8588.CR2 > ppm.ppm
            print raw
            rawi = rawpy.imread(raw)
            rgb = rawi.postprocess(no_auto_bright=True, output_bps=16, user_flip=0, user_wb=[127,127,127,127])
            cv2.imwrite(root+"/LDS_data/tmp/si_%02d.tiff" % i,rgb)
            del rawi
            del rgb
        except Exception, e:
            print e

        print "převod Light obrázků:", i, " z ", len(raw_files)
    Okno = Aligmen()
    Okno.root=root
    raw_files = sorted(glob.glob(root+"/LDS_data/tmp/si_*.tiff"))
    
    Stacking = stacking.stacking()
    Stacking.setDataPath(root)
    Stacking.setLightFrames(sorted(glob.glob(root+"/LDS_data/tmp/si_*.tiff")))
    Stacking.setDarkFrames(sorted(glob.glob(root+"/LDS_data/tmp/df_*.tiff")))


    Okno.raw_files = raw_files
    Okno.spust()
    #Okno.AligmenPositions=np.zeros((len(raw_files),3,2), dtype=numpy.float32)
    Okno.SetImageA(raw_files[0])
    Okno.SetImageB(raw_files[0])
    Okno.IMGB=0
    
    Okno.done()
