#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tables
import time
import datetime
from tables import *
from process import *
from gui.FileChooser import *
import Image
from rawkit.raw import Raw
import matplotlib.pyplot as plt
import numpy as np
try:
    import pygtk
    pygtk.require("2.0")
    import gtk
except:
    print "Error: PyGTK and GTK 2.xx must be installed to run this application. Exiting"
    sys.exit(1)




class LDS_mainSession:

    def __init__(self):
        print (os.path.expanduser("~"))
        self.LDS_projectFolder = None
        self.LDS_projectFile = None
        self.LDS_projectName = None

        self.LDS_data_Light =  np.array((5,))
        self.LDS_data_Dark  =  np.array((5,))
        self.LDS_data_Flat  =  np.array((5,))

        self.TYPE_IMG_WHITE = 0
        self.TYPE_IMG_DARK  = 1
        self.TYPE_IMG_FLAT  = 2

    def ChooseProject(self):

        self.mWinToolBox = gtk.Window()
        self.mWinToolBox.set_border_width(10)
        self.mWinToolBox.set_position(gtk.WIN_POS_CENTER)
        self.mWinToolBox.resize(200,300)
        self.mWinToolBox.set_icon_from_file('icon.png')
        self.mBtnOpenPro = gtk.Button("Otevřít projekt")
        self.mBtnNewProj = gtk.Button("Nový projekt")
        self.mBtnExit = gtk.Button("Ukončit")

        self.mVBoxTBFrame = gtk.VBox( homogeneous=True, spacing=5 )
        self.mVBoxTBFrame.pack_start(self.mBtnNewProj)
        self.mVBoxTBFrame.pack_start(self.mBtnOpenPro)
        self.mVBoxTBFrame.pack_start(self.mBtnExit)

        self.mWinToolBox.add(self.mVBoxTBFrame)
        

        self.mBtnOpenPro.connect("clicked", self.OpenProject)
        self.mBtnNewProj.connect("clicked", self.NewProject)
        self.mBtnExit.connect("clicked", gtk.main_quit)

        self.mWinToolBox.show_all()

        gtk.main()

    def OpenProject(self, widget):
        print ("Otevri projekt")

    def NewProject(self, widget):
        print ("Nový projekt")

        now = datetime.datetime.now()
        self.LDS_projectFolder = os.path.expanduser("~")
        self.LDS_projectFile = "/LDS_project" + str(now.strftime("_%Y-%m-%d_%H-%M-%S")) + ".lds"
        self.LDS_projectName = "NoName"
        print ("nazev souboru:", self.LDS_projectFolder+self.LDS_projectFile)

        class Particle(IsDescription):
            id = Int32Col() 
            srcFile = StringCol(itemsize=255)
            srcConvert =  StringCol(itemsize=255)
            ch = Int32Col() 
            type = Int32Col() 

        DataFile = open_file(self.LDS_projectFolder+self.LDS_projectFile, mode = "a", title = self.LDS_projectName)
        groupSRC = DataFile.create_group("/", 'Source', 'Source files')
        groupPRO = DataFile.create_group("/", 'Processing', 'Files processed')
        groupCFG = DataFile.create_group("/", 'Config', 'setting')
        table = DataFile.create_table("/Source", "srcFile", Particle)
        DataFile.root._v_attrs.TIME_create = datetime.datetime.utcnow().isoformat()
        DataFile.root._v_attrs.project_NAME = self.LDS_projectName
        DataFile.root._v_attrs.project_FILE = self.LDS_projectFile
        DataFile.close()

        self.LoadProject(widget)
        gtk.main()

    def LoadProject(self, widget=None):
        print ("Nahrávám projekt")

        self.DataFile = open_file(self.LDS_projectFolder+self.LDS_projectFile, mode = "a", title = self.LDS_projectName)


        self.mTBStackMenu = gtk.Notebook()
        self.mTBStackMenu.set_tab_pos(gtk.POS_TOP)

        self.mHBoxStackM1 = gtk.HBox()
        self.mHBoxStackM2 = gtk.HBox()
        self.mHBoxStackM3 = gtk.HBox()
        self.mHBoxStackM4 = gtk.HBox()
        self.mHBoxStackM5 = gtk.HBox()

        self.mScrollStackM1 = gtk.ScrolledWindow()
        self.mScrollStackM2 = gtk.ScrolledWindow()
        self.mScrollStackM3 = gtk.ScrolledWindow()
        self.mScrollStackM4 = gtk.ScrolledWindow()
        self.mScrollStackM5 = gtk.ScrolledWindow()

        self.mTBStackMenu.append_page(self.mScrollStackM1, gtk.Label("Project"))
        self.mTBStackMenu.append_page(self.mScrollStackM2, gtk.Label("Callibration"))
        self.mTBStackMenu.append_page(self.mScrollStackM3, gtk.Label("Aligment"))
        self.mTBStackMenu.append_page(self.mScrollStackM4, gtk.Label("Export"))
        self.mTBStackMenu.append_page(self.mScrollStackM5, gtk.Label("Aboute"))

        self.mScrollStackM1.add_with_viewport(self.mHBoxStackM1)                                ## Kazdou cast pridavat do toolboxu
        self.mScrollStackM2.add_with_viewport(self.mHBoxStackM2)
        self.mScrollStackM3.add_with_viewport(self.mHBoxStackM3)
        self.mScrollStackM4.add_with_viewport(self.mHBoxStackM4)
        self.mScrollStackM5.add_with_viewport(self.mHBoxStackM5)
     
        ##
        ##      ## Stránka ToolBoxu c. 1 - Project
        ##

        self.mFramH1P1 = gtk.Frame("Project")
        self.mFramH1P2 = gtk.Frame("WhiteShots")
        self.mFramH1P3 = gtk.Frame("DarkShots")
        self.mFramH1P4 = gtk.Frame("FlatShots")

        self.mHBoxStackM1.pack_start(self.mFramH1P1)
        self.mHBoxStackM1.pack_start(self.mFramH1P2)
        self.mHBoxStackM1.pack_start(self.mFramH1P3)
        self.mHBoxStackM1.pack_start(self.mFramH1P4)
        self.mTableH1P1 = gtk.Table(10,3)
        self.mTableH1P2 = gtk.Table(10,3)
        self.mTableH1P3 = gtk.Table(10,3)
        self.mTableH1P4 = gtk.Table(10,3)
        self.mFramH1P1.add(self.mTableH1P1)
        self.mFramH1P2.add(self.mTableH1P2)
        self.mFramH1P3.add(self.mTableH1P3)
        self.mFramH1P4.add(self.mTableH1P4)

        self.mTableH1P1.attach(gtk.Label("Projekt:"),0,1,0,1)
        self.mLabel_H1_prjectName = gtk.Label(self.LDS_projectName)
        self.mTableH1P1.attach(self.mLabel_H1_prjectName,1,3,0,1)

        self.mBtnShowLight = gtk.Button("Seznam Light snímků", gtk.STOCK_OPEN)
        self.mBtnConvLight = gtk.Button("Převést LightSnímky")
        self.mBtnShowLight.connect("clicked", self.FileList, self.TYPE_IMG_WHITE)
        self.mTableH1P2.attach(self.mBtnShowLight,0,3,0,1)
        self.mTableH1P2.attach(gtk.Label("Načteno:"),0,1,1,2)
        self.mLabel_H1_LightShotLoad = gtk.Label(str(0))
        self.mTableH1P2.attach(self.mLabel_H1_LightShotLoad,1,3,1,2)
        self.mTableH1P2.attach(gtk.Label("Potvrzeno:"),0,1,2,3)
        self.mLabel_H1_LightShotUsed = gtk.Label(str(0))
        self.mTableH1P2.attach(self.mLabel_H1_LightShotUsed,1,3,2,3)
        self.mTableH1P2.attach(gtk.Label("Převedeno:"),0,1,3,4)
        self.mLabel_H1_LightShotConverted = gtk.Label(str(0))
        self.mTableH1P2.attach(self.mLabel_H1_LightShotConverted ,1,3,3,4)
        self.mTableH1P2.attach(self.mBtnConvLight,1,3,9,10)

        self.mBtnShowDark = gtk.Button("Seznam Dark snímků", gtk.STOCK_OPEN)
        self.mBtnConvDark = gtk.Button("Převést Dark snímky")
        self.mBtnShowDark.connect("clicked", self.FileList, self.TYPE_IMG_DARK)
        self.mTableH1P3.attach(self.mBtnShowDark,0,3,0,1)
        self.mTableH1P3.attach(gtk.Label("Načteno:"),0,1,1,2)
        self.mLabel_H1_DarkShotLoad = gtk.Label(str(0))
        self.mTableH1P3.attach(self.mLabel_H1_DarkShotLoad,1,3,1,2)
        self.mTableH1P3.attach(gtk.Label("Potvrzeno:"),0,1,2,3)
        self.mLabel_H1_DarkShotUsed = gtk.Label(str(0))
        self.mTableH1P3.attach(self.mLabel_H1_DarkShotUsed,1,3,2,3)
        self.mTableH1P3.attach(gtk.Label("Převedeno:"),0,1,3,4)
        self.mLabel_H1_DarkShotConverted = gtk.Label(str(0))
        self.mTableH1P3.attach(self.mLabel_H1_DarkShotConverted,1,3,3,4)
        self.mTableH1P3.attach(self.mBtnConvDark,1,3,9,10)

        self.mBtnShowFlat = gtk.Button("Seznam Flat-field snímků", gtk.STOCK_OPEN)
        self.mBtnConvFlat = gtk.Button("Převést Flat-field snímky")
        self.mBtnShowFlat.connect("clicked", self.FileList, self.TYPE_IMG_FLAT)
        self.mTableH1P4.attach(self.mBtnShowFlat,0,3,0,1)
        self.mTableH1P4.attach(gtk.Label("Načteno:"),0,1,1,2)
        self.mLabel_H1_FlatShotLoad = gtk.Label(str(0))
        self.mTableH1P4.attach(self.mLabel_H1_FlatShotLoad,1,3,1,2)
        self.mTableH1P4.attach(gtk.Label("Potvrzeno:"),0,1,2,3)
        self.mLabel_H1_FlatShotUsed = gtk.Label(str(0))
        self.mTableH1P4.attach(self.mLabel_H1_FlatShotUsed,1,3,2,3)
        self.mTableH1P4.attach(gtk.Label("Převedeno:"),0,1,3,4)
        self.mLabel_H1_FlatShotConverted = gtk.Label(str(0))
        self.mTableH1P4.attach(self.mLabel_H1_FlatShotConverted,1,3,3,4)
        self.mTableH1P4.attach(self.mBtnConvFlat,1,3,9,10)


        self.mVBoxTBFrame.remove(self.mBtnNewProj)
        self.mVBoxTBFrame.remove(self.mBtnOpenPro)
        self.mVBoxTBFrame.remove(self.mBtnExit)
        self.mWinToolBox.resize(800,300)

        self.mVBoxTBFrame.pack_start(self.mTBStackMenu)
        self.mVBoxTBFrame.show_all()

        self.updateX()

        gtk.main()

    def FileList(self, widget, type=None):
        self.mFileList = FileChooser(self, widget, type)
        self.mFileList.openWindowList()

    def updateX(self, widget=None):
        self.mLabel_H1_prjectName.set_text(str(self.LDS_projectName))
        self.mLabel_H1_LightShotLoad.set_text(str(len(list(self.DataFile.root.Source.srcFile.where('type == 0')))))
        self.mLabel_H1_LightShotUsed.set_text(str(-1) + " ("+str(0)+" %)")
        self.mLabel_H1_LightShotConverted.set_text(str(-1) + " ("+str(0)+" %)")
        self.mLabel_H1_DarkShotLoad.set_text(str(len(list(self.DataFile.root.Source.srcFile.where('type == 1')))))
        self.mLabel_H1_DarkShotUsed.set_text(str(-1) + " ("+str(0)+" %)")
        self.mLabel_H1_DarkShotConverted.set_text(str(-1) + " ("+str(0)+" %)")
        self.mLabel_H1_FlatShotLoad.set_text(str(len(list(self.DataFile.root.Source.srcFile.where('type == 2')))))
        self.mLabel_H1_FlatShotUsed.set_text(str(-1) + " ("+str(0)+" %)")
        self.mLabel_H1_FlatShotConverted.set_text(str(-1) + " ("+str(0)+" %)")
        
"""
    def FileList(self, widget, type=None):
        print ("pouzivame typ: ", type, " widget: ", widget)

        #mListS = gtk.ListStore(int, str, bool, int, int)   ## id, jmeno, pouzit, kanalu, velikost
        mListS = gtk.ListStore(str, str, str, 'gboolean')   ## id, jmeno, pouzit, kanalu, velikost
        
        if type == 0:
            for id in self.LDS_data_Light:
                pass
        elif type == 1:
                pass
        else: 
            print ("neznam")
        mWinList = gtk.Window()
        mWinList.resize(300,500)
        mWinList.show_all()
       
        mFLToolBar = gtk.Toolbar()
        mFLToolBar.set_style(gtk.TOOLBAR_ICONS)

        mTBtnADD = gtk.ToolButton(gtk.STOCK_ADD)
        mTBtnREM = gtk.ToolButton(gtk.STOCK_REMOVE)
        mTBtnsep = gtk.SeparatorToolItem()
        mTBtnOPN = gtk.ToolButton(gtk.STOCK_OPEN)

        mFLToolBar.insert(mTBtnADD,0)
        mFLToolBar.insert(mTBtnREM,1)
        mFLToolBar.insert(mTBtnsep,2)
        mFLToolBar.insert(mTBtnOPN,3)
        #mFLToolBar.append_item(None,None,None, gtk.STOCK_ADD, None, None)

        mTreeView = gtk.TreeView(mListS)

        tvcolumn = gtk.TreeViewColumn('Pixbuf and Text')
        tvcolumn1 = gtk.TreeViewColumn('Text Only')

        # add a row with text and a stock item - color strings for
        # the background
        mListS.append(['Open', gtk.STOCK_OPEN, 'Open a File', True])
        mListS.append(['New', gtk.STOCK_NEW, 'New File', True])
        mListS.append(['Print', gtk.STOCK_PRINT, 'Print File', False])

        # add columns to treeview
        mTreeView.append_column(tvcolumn)
        mTreeView.append_column(tvcolumn1)

        # create a CellRenderers to render the data
        self.cellpb = gtk.CellRendererPixbuf()
        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()

        # set background color property
        self.cellpb.set_property('cell-background', 'yellow')
        self.cell.set_property('cell-background', 'cyan')
        self.cell1.set_property('cell-background', 'pink')


        # add the cells to the columns - 2 in the first
        tvcolumn.pack_start(self.cellpb, False)
        tvcolumn.pack_start(self.cell, True)
        tvcolumn1.pack_start(self.cell1, True)

        tvcolumn.set_attributes(self.cellpb, stock_id=1)
        tvcolumn.set_attributes(self.cell, text=0)
        tvcolumn1.set_attributes(self.cell1, text=2, cell_background_set=3)

        # make treeview searchable
        mTreeView.set_search_column(0)

        # Allow sorting on the column
        tvcolumn.set_sort_column_id(0)




        mWinVBox = gtk.VBox()
        mWinVBox.pack_start(mFLToolBar)
        mWinVBox.pack_start(mTreeView)
        mWinList.add(mWinVBox)
        mWinList.show_all()
        gtk.main()

"""

'''
print ("ahoj")
h5file = open_file("tutorial1.h5", mode = "a", title = "Test file")

#   group = h5file.create_group("/", 'detector', 'Detector information')


raw = Raw(filename="./../IMG_7958.CR2")
raw.save(filename="./../IMG_7958.ppm")
im = Image.open("./../IMG_7958.ppm")
os.remove("./../IMG_7958.ppm")
green = np.asarray(im)


ds = h5file.createCArray("/detector/", 'somengooogamgge', tables.Atom.from_dtype(green.dtype), green.shape)
ds[:] = green
h5file.close()


raw.save(filename="./../IMG_7958.tiff",filetype="tiff")
raw.unpack()

'''


if __name__ == "__main__" :

    aplikace = LDS_mainSession()
    aplikace.ChooseProject()