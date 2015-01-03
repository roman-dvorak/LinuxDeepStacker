#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LDS.py

# Copyright (c) 2014-2015, Roman Dvorak, roman-dvorak@email.cz
#

import sys
import os
from netpbmfile import *
import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy
import math
import pyfits
import numpy as np
import cv2
from SimpleCV import *
import cv2.cv as cv
import subprocess
import glob
import pygtk
import gtk
import random
import Image
import ImageDraw
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
from skimage import exposure
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral
import datetime






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
        

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        self.kostra.pack_start(self.toolbar, False, False)

        self.show_all()

    def spust(self):
        play = False

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

        self.toolbar_item07 = gtk.ToolButton("CelýObr")
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
        
        adjV = gtk.Adjustment(1, 1, 120, 1, 1, 0)
        adjH = gtk.Adjustment(1, 1, 120, 1, 1, 0)

        self.IMGkostra = gtk.HBox()
        self.kostra.pack_end(self.IMGkostra, True, True,10)
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
        else:
            self.AligmenPositions[self.IMGB][self.ClickNum]=[event.x, event.y]


        self.show_all()

    def StackSum(self):
        print "Normální sčítání"

        image = cv2.imread(self.raw_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)
        print image.shape, image.dtype
        print image.shape
        rows, cols, ch = image.shape
        
        for rawIndex in range(0,len(self.raw_files)):
            print "počítá se obr:", rawIndex, "což je:", self.raw_files[rawIndex]
            image2 = cv2.imread(self.raw_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(numpy.uint16)

            sb = np.zeros((image2.shape[1], image2.shape[0]), numpy.uint16)
            sg = np.zeros((image2.shape[1], image2.shape[0]), numpy.uint16)
            sr = np.zeros((image2.shape[1], image2.shape[0]), numpy.uint16)
            (sb, sg, sr) = cv2.split(image2)
            #sb = cv2.equalizeHist(sb)
            #sg = cv2.equalizeHist(sg)
            #sr = cv2.equalizeHist(sr)
            gamma = 1 / 2.2
            sr = sr * 2 # pow(value, power)
            sg = sg * 2
            sb = sb * 2
            image2 = cv2.merge((sb, sg, sr))


            print image2.min(), image2.max(), image2.mean(), image2.ptp(), (math.ceil(1.00/(len(self.raw_files)-1.00) * 100.00) / 100.00)
            M = cv2.getAffineTransform(self.AligmenPositions[rawIndex],self.AligmenPositions[0])
            image2 = cv2.warpAffine(image2,M,(cols,rows))
            image = cv2.addWeighted(image,1,image2, (math.ceil(1.00/(len(self.raw_files)-1.00) * 100.00) / 100.00) ,0)
            #image = cv2.add(image,image2)

        #M = cv2.getAffineTransform(pts1,pts2)
    #    M = cv2.getAffineTransform(self.AligmenPositions[1],self.AligmenPositions[0])
    #    print self.AligmenPositions[0], " a ", self.AligmenPositions[1]
    #    print self.raw_files[0], " a ", self.raw_files[1]

    #    rows,cols,ch = image2.shape
    #    print rows, cols
    #    dst = cv2.warpAffine(image2,M,(cols,rows))
        
    #    image = cv2.add(image,dst)
        #dst = ccv2.absdiff(image, dst)

        #plt.subplot(122),plt.imshow(image),plt.title('Output')
        plt.subplot(111),plt.imshow(image),plt.title('Output')
        image = image.astype(numpy.uint16)
        cv2.imwrite('processed.tif',image )
        print "Vysledek"
        print image2.min(), image2.max(), image2.mean(), image2.ptp()
        print "ukládání posledního obr"
        plt.show()

    def StackMedian(self):
        print "Median Stacking High memory"

        image = cv2.imread(self.raw_files[0], cv2.IMREAD_UNCHANGED)
        image = image.astype(numpy.uint16)
        image = cv2.addWeighted(image, 0, image, 0, 0)
        print image.shape, image.dtype
        rows, cols, ch = image.shape
        data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='w+', shape=(len(self.raw_files),rows, cols, ch))
        data.flush()
        del data

        for rawIndex in range(0,len(self.raw_files)):
            data = np.memmap(self.root+"/LDS_data/tmp/mem.map", dtype='uint16', mode='r+', shape=(len(self.raw_files),rows, cols, ch))
            print "Získává se obr:", rawIndex, "což je:", self.raw_files[rawIndex]
            image2 = cv2.imread(self.raw_files[rawIndex], cv2.IMREAD_UNCHANGED)
            image2 = image2.astype(numpy.uint16)
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
        cv2.imwrite(self.root+"/LDS_data/OUT/"+now.strftime("%Y-%m-%dT%H:%M")+".tiff",image )
        print "ukládání výsledného obr"
        del data


    def ProcesChoose(self, widget):
        np.save(self.root+"/LDS_data/tmp/AligmenPositions.npy",self.AligmenPositions)
        #self.StackSum()
        self.StackMedian()


    def ChangeIMG(self, widget):
        self.ClickNum=0
        if widget == self.toolbar_item05: # poslední btn
            self.IMGB = len(self.raw_files)-1
            self.SetImageB(self.raw_files[self.IMGB])

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

        img = cv2.imread(self.raw_files[self.IMGB])
        mapa = gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8)
        w,h = mapa.get_width(), mapa.get_height()
        pixmap,mask = mapa.render_pixmap_and_mask() # Function call
        cm = pixmap.get_colormap()
        red = cm.alloc_color('red')
        gc = pixmap.new_gc(foreground=red )
        #pixmap.draw_line(gc,0,0,w,h)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][0][0])-12, int(self.AligmenPositions[self.IMGB][0][1])-12, 24, 24, 0, 23040)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][1][0])-12, int(self.AligmenPositions[self.IMGB][1][1])-12, 24, 24, 0, 23040)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][2][0])-12, int(self.AligmenPositions[self.IMGB][2][1])-12, 24, 24, 0, 23040)
        self.imageB.set_from_pixmap(pixmap,mask)


    def LableIMG(self, widget, event):
        self.AligmenPositions[self.IMGB][self.ClickNum]=[event.x, event.y]
        self.ClickNum= self.ClickNum + 1
        if self.ClickNum == 3:
            print self.AligmenPositions
            print "Poslední bod - při dalším klknití se bude označovat od začátku"
            self.ClickNum = 0
            if self.IMGB == 0:
                #mapa = self.imageA.get_pixbuf()
                img = cv2.imread(self.raw_files[0])
                
                img = img/255.000000
                img = cv2.pow(img, .85)
                img = np.uint8(img*255.000000)

                mapa = gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8)
                w,h = mapa.get_width(), mapa.get_height()
                pixmap,mask = mapa.render_pixmap_and_mask() # Function call
                cm = pixmap.get_colormap()
                red = cm.alloc_color('red')
                gc = pixmap.new_gc(foreground=red )
                pixmap.draw_line(gc,int(self.AligmenPositions[0][0][0]),int(self.AligmenPositions[0][0][1]),int(self.AligmenPositions[0][1][0]),int(self.AligmenPositions[0][1][1]))
                pixmap.draw_line(gc,int(self.AligmenPositions[0][1][0]),int(self.AligmenPositions[0][1][1]),int(self.AligmenPositions[0][2][0]),int(self.AligmenPositions[0][2][1]))
                pixmap.draw_line(gc,int(self.AligmenPositions[0][2][0]),int(self.AligmenPositions[0][2][1]),int(self.AligmenPositions[0][0][0]),int(self.AligmenPositions[0][0][1]))
                pixmap.draw_arc(gc, 0, int(self.AligmenPositions[0][0][0])-12, int(self.AligmenPositions[0][0][1])-12, 24, 24, 0, 23040)
                pixmap.draw_arc(gc, 0, int(self.AligmenPositions[0][1][0])-12, int(self.AligmenPositions[0][1][1])-12, 24, 24, 0, 23040)
                pixmap.draw_arc(gc, 0, int(self.AligmenPositions[0][2][0])-12, int(self.AligmenPositions[0][2][1])-12, 24, 24, 0, 23040)
                self.imageA.set_from_pixmap(pixmap,mask)
            
        img = cv2.imread(self.raw_files[self.IMGB])
        mapa = gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8)
        w,h = mapa.get_width(), mapa.get_height()
        pixmap,mask = mapa.render_pixmap_and_mask() # Function call
        cm = pixmap.get_colormap()
        red = cm.alloc_color('red')
        gc = pixmap.new_gc(foreground=red )
        #pixmap.draw_line(gc,0,0,w,h)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][0][0])-12, int(self.AligmenPositions[self.IMGB][0][1])-12, 24, 24, 0, 23040)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][1][0])-12, int(self.AligmenPositions[self.IMGB][1][1])-12, 24, 24, 0, 23040)
        pixmap.draw_arc(gc, 0, int(self.AligmenPositions[self.IMGB][2][0])-12, int(self.AligmenPositions[self.IMGB][2][1])-12, 24, 24, 0, 23040)
        self.imageB.set_from_pixmap(pixmap,mask)





    def SetImageA(self, pathToppm):
        img = cv2.imread(pathToppm)
        self.imageA.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))

    def SetImageB(self, pathToppm):
        img = cv2.imread(pathToppm)
        self.imageB.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8))

    def  done(self):
        gtk.main()


if __name__ == "__main__":
    root = sys.argv[1]
    raw_files = sorted(glob.glob(root+"/LDS_data/StackImages/*.CR2"))
    print raw_files
    i=0
    for raw in raw_files:
        i = i+1
        #os.popen("dcraw -6 -c -W "+raw+" > "+root+"/LDS_data/tmp/si_%02d.ppm" % i)     #dcraw -6 -c -W IMG_8588.CR2 > ppm.ppm
    Okno = Aligmen()
    Okno.root=root
    raw_files = sorted(glob.glob(root+"/LDS_data/tmp/si_*.ppm"))
    Okno.raw_files = raw_files
    Okno.spust()
    #Okno.AligmenPositions=np.zeros((len(raw_files),3,2), dtype=numpy.float32)
    Okno.SetImageA(str(raw_files[0]))
    Okno.SetImageB(raw_files[0])
    Okno.IMGB=0
    
    Okno.done()






    #Okno.gtk.main()


    #imag =cv2.imread(root, cv2.CV_LOAD_IMAGE_COLOR)
    #rows,cols,ch = imag.shape

    ####
        #image = cv2.imread(sys.argv[1], cv2.CV_LOAD_IMAGE_COLOR)
        #image2 = cv2.imread(sys.argv[2], cv2.CV_LOAD_IMAGE_COLOR)


        ##im = NetpbmFile("ppm.ppm").asarray()
        ##im2 = NetpbmFile("ppm2.ppm").asarray()
        ##green = numpy.zeros((im.shape[0],im.shape[1]),dtype=numpy.uint16)
        ##for row in xrange(0,im.shape[0]) :
        ##  for col in xrange(0,im.shape[1]) :
        ##      green[row,col] = im[row,col][0]
        ##      print "data:", row, col
        ##hdu = pyfits.PrimaryHDU(green)
        ##hdu.writeto('GreenChannel.fits')


        #plt.subplot(121),plt.imshow(image2),plt.title('Input')

        #pts1 = np.float32([[1474,312],[1420,4852],[2309,3059]])
        #pts2 = np.float32([[1522,310],[1467,4850],[2357,3057]])

        #M = cv2.getAffineTransform(pts1,pts2)

        #dst = cv2.warpAffine(image2,M,(cols,rows))
        
        #dst = cv2.addWeighted(image,0.8,dst,0.8,0)
        ##dst = ccv2.absdiff(image, dst)

        ##plt.subplot(121),plt.imshow(img),plt.title('Input')
        #plt.subplot(122),plt.imshow(dst),plt.title('Output')
        #plt.show()
        #cv2.imwrite("aa.jpg", image)
    ####