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

class FileChooser():

    def __init__(self, parent, source, Type):
        print ("Nový file chooser z externiho py souboru:")
        print (source)
        print (Type)
        print (parent)
        self.parent = parent
        self.source = source
        self.Type = Type

    def  openWindowList(self):
        print ("Nový file chooser z externiho py souboru")


        self.mTreeListS = gtk.ListStore(int, str, bool, int)   ## id, jmeno, pouzit, kanalu, velikost
        #self.mTreeListS = gtk.ListStore(str, str, str, 'gboolean')   ## id, jmeno, pouzit, kanalu, velikost
        
        if self.Type == 0:
            pass
            #for id in self.parent.LDS_data_Light:
            #for n in self.parent.DataFile.root.Source.srcFile.where('type == 0'):
            #    self.mTreeListS.append([n['id'], n['srcFile'], True, n['ch']])

        elif self.Type == 1:
            print ()
            #for n in self.parent.DataFile.root.Source.srcFile.iterrows():
            #    self.mTreeListS.append([n['id'], n['srcFile'], True, n['ch']])

        else: 
            print ("neznam")

        for n in self.parent.DataFile.root.Source.srcFile.where('type == '+ str(self.Type)):
            self.mTreeListS.append([n['id'], n['srcFile'], True, n['ch']])

        mWinList = gtk.Window()
        mWinList.resize(300,500)
        mWinList.show_all()
        mWinList.connect('destroy',self.close)
       
        mFLToolBar = gtk.Toolbar()
        mFLToolBar.set_style(gtk.TOOLBAR_ICONS)

        mTBtnADD = gtk.ToolButton(gtk.STOCK_ADD)
        mTBtnREM = gtk.ToolButton(gtk.STOCK_REMOVE)
        mTBtnsep = gtk.SeparatorToolItem()
        mTBtnOPN = gtk.ToolButton(gtk.STOCK_OPEN)

        mTBtnADD.connect("clicked", self.addfile)
        mTBtnREM.connect("clicked", self.rmfile)
        mTBtnOPN.connect("clicked", self.addfolder)

        mFLToolBar.insert(mTBtnADD,0)
        mFLToolBar.insert(mTBtnREM,1)
        mFLToolBar.insert(mTBtnsep,2)
        mFLToolBar.insert(mTBtnOPN,3)

        self.mTreeView = gtk.TreeView(self.mTreeListS)

        self.mTreeColmnID = gtk.TreeViewColumn('ID')
        self.mTreeColmnFI = gtk.TreeViewColumn('FileName')
        self.mTreeColmnUSE = gtk.TreeViewColumn('use?')
        self.mTreeColmnCH = gtk.TreeViewColumn('channels')

        # add columns to treeview
        self.mTreeView.append_column(self.mTreeColmnID)
        self.mTreeView.append_column(self.mTreeColmnFI)
        self.mTreeView.append_column(self.mTreeColmnUSE)
        self.mTreeView.append_column(self.mTreeColmnCH)

        # create a CellRenderers to render the data
        self.cell = gtk.CellRendererText()


        # add the cells to the columns - 2 in the first
        self.mTreeColmnID.pack_start(self.cell, True)
        self.mTreeColmnFI.pack_start(self.cell, True)
        self.mTreeColmnUSE.pack_start(self.cell, True)
        self.mTreeColmnCH.pack_start(self.cell, True)

        self.mTreeColmnID.set_attributes(self.cell, text=0)
        self.mTreeColmnFI.set_attributes(self.cell, text=1)
        self.mTreeColmnUSE.set_attributes(self.cell, text=2)
        self.mTreeColmnCH.set_attributes(self.cell, text=3)

        # make treeview searchable
        self.mTreeView.set_search_column(0)

        # Allow sorting on the column
        self.mTreeColmnID.set_sort_column_id(0)
        self.mTreeColmnID.set_sort_column_id(1)


        mWinVBox = gtk.VBox(False)
        mWinVBox.pack_start(mFLToolBar, False, False, 0)
        mWinVBox.pack_start(self.mTreeView)
        mWinList.add(mWinVBox)

        #self.mTreeListS.append([6, 'oe', True, 23])
        #self.mTreeListS.append([7, 'Print', True, 23])

        mWinList.show_all()
        gtk.main()


    def addfolder(self, widget):
#TODO: zde musi byt file chooseing dialog (resp. folder)
        path = "/home/roman/Dokumenty/Projects/LinuxDeepStacker/LightTest/"
        place = self.parent.DataFile.root.Source.srcFile.row
        x = 0
        for row in self.parent.DataFile.root.Source.srcFile.where('type == '+ str(self.Type)):
            print(type(row), row)
            self.parent.DataFile.root.Source.srcFile.remove_row(row)
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                print(dirpath, filename)
                self.mTreeListS.append([x, filename, True, -1])
                place['id']= x
                place['srcFile']=dirpath+filename
                place['srcConvert']= None
                place['ch']= -1
                place['type']= self.Type
                place.append()
                x += 1
        self.parent.DataFile.flush()



    def addfile(self, widget):
        self.mTreeListS.append([6, 'ooeoe', True, 23])
        print ("---",self.parent.DataFile.root.Source.srcFile, type(self.parent.DataFile.root.Source.srcFile),self.parent.LDS_data_Light.shape)
        place = self.parent.DataFile.root.Source.srcFile.row
        

        # self.parent.LDS_data_Light
       # np.append( self.parent.LDS_data_Light, [[7, 8, 9]], axis=0)

        place['srcFile']="fileaddr"
        place['srcConvert']="fileaddr"
        place['ch']= 3
        place['type']=0
        place.append()
        self.parent.DataFile.flush()


    def rmfile(self, widget):
        selection = self.mTreeView.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            itera = model.get_iter(path)
            elementID = model.get_value(itera, 0)
            model.remove(itera)

        self.parent.DataFile.root.Source.srcFile.remove_row(elementID)
        self.parent.DataFile.flush()

    def close(self,widget):
        print("close function")
        self.parent.updateX()
    #    model = self.mTreeView.get_model()
    #    for x in model:
    #        print ("model", x, x[0], x[1], x[2])


   # def save(self):
   #     print("saving function")
       # self.mTreeView.select_all()
       # self.mTreeView.get_selection.set_mode(gtk.SELECTION_MULTIPLE)
       # selection = self.mTreeView.get_selection().select_all()
       #model, paths = selection.get_selected_rows()
       # for path in paths:
       #     itera = model.get_iter(path)
       #     print (paths, itera)
       #     model.remove(itera)



