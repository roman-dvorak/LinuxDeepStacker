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
from ui import LoadProject
#from work import *

gettext.bindtextdomain('cs_CZ')
gettext.textdomain('cs_CZ')
_ = gettext.gettext


##########################################################################################################
##########################################################################################################    
##### Třída starající se o práci s projektem .. ukladaní, toření, otevírání načítání dat ....
##############

class ProjectClass():
    def __init__(self, arg):
        self.config = configparser.ConfigParser()
        self.loaded = False
        self.arg = arg
        self.ProjectName = None
        self.ProjectAuthorName = None
        self.ProjectAuthorEmail = None
        self.ProjectAuthorAdress = None
        self.ProjectAuthorWeb = None
        self.ProjectAuthorNotes = None
        self.ProjectFile = None
        self.ProjectFolder = None
        self.ProjectCreationDate = None
        self.ProjectLastOpen = None
        self.Project_colour = None
        self.ProjectLoadType = -1        # 0 - from system, 1-trought terminal, 2- open trought gui, 3 - open from last, 4 - new project
        self.Propelties = {}
        self.File = None
        FileConfig = None
        for x in arg:
            if ".lds" in x.lower() or ".ldsa" in x.lower():
                print "vstupni parametr obsahuje nejaky muj soubor"
                self.ProjectLoadType = 1
                self.load(x)

    def new(self):
        self.ProjectCreationDate = datetime.datetime.utcnow()
        self.File = h5py.File(self.ProjectFile, 'w')
        self.FileConfig = self.File.require_dataset("config", (10,2), maxshape=(None, 2), dtype = h5py.special_dtype(vlen=unicode))
        self.FileConfig.attrs.modify("ProjectName", self.ProjectName)
        self.FileConfig.attrs.modify("ProjectCreationDate", str(self.ProjectCreationDate))
        self.FileConfig.attrs.modify("ProjectLastOpen", [str(self.ProjectCreationDate)])
        self.FileConfig.attrs.modify("test", [10,23,023,034])
        self.File.flush()

    def load(self, path):
        print _("Loading varibales from %s")%(path)
        self.File = h5py.File(path, 'r+')
        self.FileConfig = self.File['config']
        self.ProjectFile = path
        self.ProjectName = self.FileConfig.attrs['ProjectName']
        self.ProjectCreationDate = self.FileConfig.attrs['ProjectCreationDate']
        self.ProjectLastOpen = self.FileConfig.attrs['ProjectLastOpen']
        self.FileConfig.attrs['ProjectLastOpen'] = np.append(self.ProjectLastOpen, str(datetime.datetime.utcnow()))

    def save(self):
        print _("Saving varibales")

    def save_as(self):
        print _("Saving as varibales")

    def OnClose(self):
        self.File.flush()
        self.File.close()

##########################################################################################################
##########################################################################################################
###### První panel hl. okna
#############

class Page_project():
    def __init__(self, parrent, notebook):
        self.parent = parrent
        self.page = wx.Panel(notebook)

        self.splitter = wx.SplitterWindow(self.page, style = wx.EXPAND | wx.SP_3D | wx.SP_LIVE_UPDATE )
        self.splitter.SetMinimumPaneSize(10)

        self.rightPanel = wx.Panel (self.splitter)
        self.rightPanel.SetBackgroundColour(wx.BLUE)
        
        panel = wx.Panel(self.rightPanel, -1)
        panel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)

        midPan = wx.Panel(panel, -1)
        midPan.SetBackgroundColour('#ededed')

        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 20)

    ########
        ## Left panel
    ########
        self.leftPanel = wx.Panel (self.splitter)
        LeftPanel_vbox = wx.BoxSizer(wx.VERTICAL)
        self.HeaderImage = wx.StaticBitmap(self.leftPanel, bitmap=wx.Bitmap("LinuxDeepStacker/media/headerA.png"))
        LeftPanel_vbox.Add(self.HeaderImage)
        LeftPanel_vbox.Add(wx.StaticText(self.leftPanel, -1, _("Project name: %s") % str(self.parent.prj.ProjectName), (10,193)))

        self.splitter.SplitVertically (self.leftPanel, self.rightPanel, 315)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.page.SetSizer(sizer)
    
    def getPage(self):
        return self.page 

#########################################################################################################
#########################################################################################################
###### Tvoří základní okno
#############

class LinuxDeepStacker(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + "Err.: " + _("Není otevřen žádný projekt"), prj = None, app = None):
        self.app = app
        self.prj = prj
        self.parent = parent
        wx.Frame.__init__(self, self.parent, id, title, size=(800, 500))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        notebook = wxfnb.FlatNotebook(panel, agwStyle= wxfnb.FNB_NO_X_BUTTON | wxfnb.FNB_NAV_BUTTONS_WHEN_NEEDED | wxfnb.FNB_SMART_TABS  )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.page_project = Page_project(self, notebook)
        notebook.AddPage(self.page_project.getPage(), _("Project tab"))
        notebook.AddPage(self.CreatePage(notebook, _("caption2")), _("caption2"))

        self.Show(True)
        self.Centre()

        if self.prj.ProjectName == None:
            LoadProject.LoadProject(self, prj = prj)

    def CreatePage(self, notebook, caption):
        p = wx.Panel(notebook)
        wx.StaticText(p, -1, caption, (20,20))
        wx.TextCtrl(p, -1, "", (20,40), (150,-1))
        return p

    def OnClose(self, widget=None):
        print ('Ukončuji program z události tlačítka')
        self.prj.OnClose()
        self.Destroy()

##########################################################################################################
##########################################################################################################

class main:
    def __init__(self, argv):
        self.argv = argv
        self.app = wx.App()
        self.prj = ProjectClass(self.argv)                              # Stará se o projekt a práci s ním Otevirani, Cteni , Ukladaní, atd....
        self.LDS = LinuxDeepStacker(app=self.app, prj = self.prj)       # Stará se o UI
        self.app.MainLoop()
