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
from ui import mwdg
import logging
import threading
from work import threads
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


##########################################################################################################
##########################################################################################################    
##### Třída starající se o práci s projektem .. ukladaní, toření, otevírání načítání dat ....
##############

class ProjectClass():
    def __init__(self, arg, parent):
        logger.info("ProjectClass __init__")
        self.config = configparser.ConfigParser()
        self.loaded = False
        self.arg = arg
        self.parent = parent
        self.ProjectName = None
        self.ProjectAuthorName = None
        self.ProjectAuthorEmail = None
        self.ProjectAuthorAdress = None
        self.ProjectAuthorWeb = None
        self.ProjectAuthorNotes = None
        self.ProjectFile = None
        #self.ProjectFolder = None
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
                self.ProjectFile = x

    def new(self):
        self.ProjectCreationDate = datetime.datetime.utcnow()
        self.File = h5py.File(self.ProjectFile, 'w')
        self.FileConfig = self.File.require_dataset("config", (10,2), maxshape=(None, 2), dtype = h5py.special_dtype(vlen=unicode))
        self.FileConfig.attrs.modify("ProjectName", self.ProjectName)
        self.FileConfig.attrs.modify("ProjectCreationDate", str(self.ProjectCreationDate))
        self.FileConfig.attrs.modify("ProjectLastOpen", [str(self.ProjectCreationDate)])
        self.FileConfig.attrs.modify("Chanels", ['R', 'G', 'B'])
        self.File.create_group("Light")
        self.File.create_group("Dark")
        self.File.create_group("Flat")
        self.File.create_group("Bias")
        self.File.flush()
        self.parent.LDS.Update()

    def load(self, path):
        logger.info(_("ProjectClass load, loading variables from%s")%(path))
        self.File = h5py.File(path, 'r+')
        self.FileConfig = self.File['config']
        self.ProjectFile = path
        self.ProjectName = self.FileConfig.attrs['ProjectName']
        self.ProjectCreationDate = self.FileConfig.attrs['ProjectCreationDate']
        self.ProjectLastOpen = self.FileConfig.attrs['ProjectLastOpen']
        self.FileConfig.attrs['ProjectLastOpen'] = np.append(self.ProjectLastOpen, str(datetime.datetime.utcnow()))
        print "bla"
        try:
            self.parent.LDS.Update()
        except Exception, e:
            logger.error(str(e))

    def save(self):
        logger.info("ProjectClass save")

    def save_as(self):
        logger.info("ProjectClass save_as")

    def OnClose(self):
        logger.info("ProjectClass OnClose")
        try:
            self.File.flush()
            self.File.close()
        except Exception, e:
            logger.error(str(e))

    def importMultipleFiles(self, files = []):
        if len(files) == 1:
            self.importSingleFile(file = files[0])
        else:
            for x in files:
                self.importSingleFile(file = x)

    def importSingleFile(self, file=None, type=None):
        logger.info("Importing file: %s as type %s" %(file, str(type)))
        self.File['Light'].create_dataset("L"+str(10+1), (500,500,3))


##########################################################################################################
##########################################################################################################
###### První panel hl. okna
#############  AndFit

class Page_project():
    def __init__(self, parrent, notebook):
        logger.info("ProjectPage __init__")
        self.parent = parrent
        self.page = wx.Panel(notebook)

        self.splitter = wx.SplitterWindow(self.page, style = wx.EXPAND | wx.SP_3D | wx.SP_LIVE_UPDATE )
        self.splitter.SetMinimumPaneSize(10)

        self.rightPanel = wx.Panel (self.splitter)
        self.RightPanelSizer = wx.GridBagSizer(2, 2)
        
        toolbar = wx.ToolBar(self.rightPanel)
        print wx.ID_EXIT
        LT_FileAdd = toolbar.AddLabelTool(wx.ID_ANY, '&Import file', wx.Bitmap("LinuxDeepStacker/media/icons/Gnome-List-Add-32.png"))
        LT_FileRemove = toolbar.AddLabelTool(wx.ID_ANY, '&Remove file', wx.Bitmap("LinuxDeepStacker/media/icons/Gnome-List-Remove-32.png"))
        toolbar.Realize()

        self.list_ctrl = wx.ListCtrl(self.rightPanel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'ID', width = 25)
        self.list_ctrl.InsertColumn(1, 'Status')
        self.list_ctrl.InsertColumn(2, 'Type')
        self.list_ctrl.InsertColumn(3, 'Exposition')
        self.list_ctrl.InsertColumn(4, 'Time')
        self.list_ctrl.InsertColumn(5, 'Stars')
        self.list_ctrl.InsertColumn(6, 'Position')
        self.list_ctrl.InsertColumn(7, 'Source file location')
        self.list_ctrl.InsertColumn(8, 'Status')

        self.RightPanelSizer.Add(toolbar, (0,0), flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)
        self.RightPanelSizer.Add(self.list_ctrl, (1,0), flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)

        self.RightPanelSizer.AddGrowableCol(0,3)
        self.RightPanelSizer.AddGrowableRow(1,3)
        self.rightPanel.SetSizer(self.RightPanelSizer)

        self.parent.Bind(wx.EVT_TOOL, self.OnAddFile, LT_FileAdd)
        self.parent.Bind(wx.EVT_TOOL, self.OnRemoveFile, LT_FileRemove)

    ########
        ## Left panel
    ########
        self.leftPanel = wx.Panel (self.splitter)
        self.LeftPanelSizer = wx.GridBagSizer(2, 2)
        self.HeaderImage = wx.StaticBitmap(self.leftPanel, bitmap=wx.Bitmap("LinuxDeepStacker/media/headerA.png"))
        LabelProjectName = wx.StaticText(self.leftPanel, -1, _("  Project name: "))
        self.BBProjectName = wx.BitmapButton(self.leftPanel, -1, bitmap=wx.Bitmap("LinuxDeepStacker/media/icons/Gnome-Accessories-Text-Editor-32.png"))
        self.TcProjectName = wx.TextCtrl(self.leftPanel, -1)
        self.TcProjectName.SetEditable(False)
        LabelProjectChanels = wx.StaticText(self.leftPanel, -1, _("  Image chanels: "))
        self.BBProjectChanels = wx.BitmapButton(self.leftPanel, -1, bitmap=wx.Bitmap("LinuxDeepStacker/media/icons/Gnome-Accessories-Text-Editor-32.png"))
        self.TcProjectChanels = wx.TextCtrl(self.leftPanel, -1)
        self.TcProjectChanels.SetEditable(False)

        self.LeftPanelSizer.Add(self.HeaderImage, (0,0), span=(1, 4))
        self.LeftPanelSizer.Add(LabelProjectName, (1,0))
        self.LeftPanelSizer.Add(self.BBProjectName, (1,1))
        self.LeftPanelSizer.Add(self.TcProjectName, (1,2), span=(1, 2) , flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)
        self.LeftPanelSizer.Add(LabelProjectChanels, (3,0))
        self.LeftPanelSizer.Add(self.BBProjectChanels, (3,1))
        self.LeftPanelSizer.Add(self.TcProjectChanels, (3,2), span=(1, 2) , flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)

        #self.RightPanelSizer.AddGrowableCol(2,3)
        self.leftPanel.SetSizer(self.LeftPanelSizer)

        self.splitter.SplitVertically (self.leftPanel, self.rightPanel, 315)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.page.SetSizer(sizer)


    def OnAddFile(self, widget=None):
        #logger.info("OnOpenProject --- Nemam zdroj")
        dlg = wx.FileDialog(self.parent, message="Vyber datovy soubor(y)", style= wx.OPEN | wx.CHANGE_DIR | wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.parent.prj.importMultipleFiles(files=dlg.GetPaths());
        dlg.Destroy()


    def OnRemoveFile(self, widget=None):
        pass

    def Update(self):
        logger.info("ProjectPage Update")
        print "Aktualizace panelu 'project'"
        self.TcProjectName.SetValue(self.parent.prj.FileConfig.attrs['ProjectName'])
        self.TcProjectChanels.SetValue(str(len(self.parent.prj.FileConfig.attrs['Chanels'])) + " " + str(self.parent.prj.FileConfig.attrs['Chanels']))
    
    def UpdateFileList(self):
        logger.info("ProjectPage Update file list")

    def getPage(self):
        logger.info("ProjectPage getPage")
        return self.page 

#########################################################################################################
#########################################################################################################
###### Tvoří základní okno
#############

class LinuxDeepStacker(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + "Err.: " + _("Není otevřen žádný projekt"), prj = None, app = None):
        logger.info("LinuxDeepStacker __init__")
        self.app = app
        self.prj = prj
        self.parent = parent
        wx.Frame.__init__(self, self.parent, id, title, size=(800, 500))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        notebook = wxfnb.FlatNotebook(panel, agwStyle= wxfnb.FNB_NO_X_BUTTON | wxfnb.FNB_NAV_BUTTONS_WHEN_NEEDED | wxfnb.FNB_SMART_TABS )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.page_project = Page_project(self, notebook)
        notebook.AddPage(self.page_project.getPage(), _("Project tab"))
        notebook.AddPage(self.CreatePage(notebook, _("caption2")), _("caption2"))

        self.statusbar = self.CreateStatusBar(4)
        self.Show(True)
        self.Centre()

        LoadProject.LoadProject(self, prj = prj)

    def CreatePage(self, notebook, caption):
        logger.info("LinuxDeepStacker CreatePage")
        p = wx.Panel(notebook)
        wx.StaticText(p, -1, caption, (20,20))
        wx.TextCtrl(p, -1, "", (20,40), (150,-1))
        return p

    def OnClose(self, widget=None):
        logger.info("LinuxDeepStacker OnClose")
        self.prj.OnClose()
        self.Destroy()

    def Update(self):
        logger.info("LinuxDeepStacker Update")
        self.SetTitle(_("Linux deep stacker | ") + self.prj.FileConfig.attrs['ProjectName'])
        self.page_project.Update()

##########################################################################################################
##########################################################################################################

class main:
    def __init__(self, argv):
        self.classes = []
        self.thrdI = Queue.Queue()
        self.thrdO = Queue.Queue()

        self.threads = [threads.Importer(input_q=self.thrdI, output_q=self.thrdO, classes=self.classes),
                        threads.UiUpdater(input_q=self.thrdI, output_q=self.thrdO, classes=self.classes),
                        threads.Processer(input_q=self.thrdI, output_q=self.thrdO, classes=self.classes) ]

        for thread in self.threads:
            thread.start()

        self.argv = argv
        self.app = wx.App()
        self.prj = ProjectClass(arg = self.argv, parent = self)         # Stará se o projekt a práci s ním Otevirani, Cteni , Ukladaní, atd....
        self.LDS = LinuxDeepStacker(app=self.app, prj = self.prj)       # Stará se o UI
        self.classes = [self.argv, self.thrdI, self.thrdO, self.app, self.prj, self.LDS, self.threads]
        self.app.MainLoop()
