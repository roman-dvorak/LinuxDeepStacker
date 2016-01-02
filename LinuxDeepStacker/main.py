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

print "hallo"
gettext.bindtextdomain('cs_CZ', '')
#gettext.find('cs_CZ')
gettext.textdomain('cs_CZ')
_ = gettext.gettext


##########################################################################################################
##########################################################################################################    

class ProjectClass():
    def __init__(self, arg):
        self.loaded = False
        self.arg = arg
        self.ProjectName = None
        self.ProjectFile = None
        self.ProjectFolder = None
        self.ProjectCreationDate = None
        self.ProjectLastUpdate = None
        self.ProjectLastOpen = None
        self.Project_colour = None
        self.Propelties = {}
        self.File = None
        for x in arg:
            if ".lds" in x.lower() or ".ldsa" in x.lower():
                print "vstupni parametr obsahuje nejaky muj soubor"
                self.load(x)

    def new(self):
        self.File = h5py.File(self.ProjectFile)
        self.File.create("PrjName", self.ProjectName)
        self.File.flush()

    def load(self, path):
        print _("Loading varibales from %s")%(path)

    def save(self):
        print _("Saving varibales")

    def save_as(self):
        print _("Saving as varibales")


##########################################################################################################
##########################################################################################################

class LoadProject(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + _("Výběr projektu"), prj = None):
        super(LoadProject, self).__init__(parent, title=title, size=(557, 410), style= wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT)
        self.parent = parent
        self.prj = prj
        self.status = False
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(1, 1)

        box = wx.BoxSizer(wx.VERTICAL)
        HeaderImage = wx.StaticBitmap(panel, bitmap=wx.Bitmap("LinuxDeepStacker/media/headerB.png"))

        BtnOpen = wx.Button(panel, label=_("Open"))
        BtnNew = wx.Button(panel, label=_("New"))
        BtnDone = wx.Button(panel, label=_("OK"))
        BtnCancel = wx.Button(panel, label=_("Cancel"))
        self.TcLocation = wx.TextCtrl(panel, -1)
        self.TcLocation.SetEditable(False)
        self.TcProjectName = wx.TextCtrl(panel, -1)
        self.TcProjectName.SetEditable(False)
        BtnRecently = wx.Choice(panel)
        LabLocation = wx.StaticText(panel, -1, _('  ProjectFile:  '))
        LabPrjName = wx.StaticText(panel, -1, _('  ProjectName:  '))
        self.LabInfo = wx.StaticText(panel, -1, _('  Info:  ') + " " + _('from %s to %s, %d Lights, %d Flats and %d Darks shots.')%('2015-10-10t23:34:45UT', '2015-10-10t23:50:45UT', 530, 10, 10))
        self.LabInfoR2 = wx.StaticText(panel, -1, _('from %s to %s, %d Lights, %d Flats and %d Darks shots.')%('2015-10-10t23:34:45UT', '2015-10-10t23:50:45UT', 530, 10, 10))

        sizer.Add(HeaderImage, pos=(0, 0), span=(1, 9), flag = wx.RIGHT|wx.TOP)
        sizer.Add(BtnOpen, pos=(1, 1), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer.Add(BtnNew, pos=(1, 2), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer.Add(BtnRecently, pos=(1, 3), span=(1, 4), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer.Add(LabLocation, pos=(3, 0), flag= wx.LEFT)
        sizer.Add(self.TcLocation, pos=(3, 1), span=(1, 7), flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)
        sizer.Add(LabPrjName, pos=(4, 0), flag=wx.LEFT)
        sizer.Add(self.TcProjectName, pos=(4, 1), span=(1, 7), flag = wx.EXPAND |wx.TOP | wx.LEFT | wx.BOTTOM)
        sizer.Add(self.LabInfo, pos=(5, 0), span=(1, 9), flag = wx.TOP | wx.LEFT)
        sizer.Add(self.LabInfoR2, pos=(6, 1), span=(1, 8), flag = wx.TOP | wx.LEFT)
        sizer.Add(BtnDone, pos=(8, 5), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer.Add(BtnCancel, pos=(8, 6), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, BtnCancel)
        self.Bind(wx.EVT_BUTTON, self.OnCreateProject, BtnNew)
        self.Bind(wx.EVT_BUTTON, self.OnOpenProject, BtnOpen)
        self.Bind(wx.EVT_BUTTON, self.OnLoadProject, BtnDone)

        #sizer.Add(HeaderImage, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=5)
        panel.SetSizer(sizer)

        self.MakeModal(True)
        self.Show(True)
        self.Centre()

    def OnCloseWindow(self, widget=None):
        self.Close()
        self.parent.Close()
        self.status = False
        self.MakeModal(False)

    def OnCreateProject(self, widget=None):
        dlg = wx.FileDialog(
            self, message="Vyber projektovy soubor", wildcard = "ProjectFile (*.lds,*.ldsa)|*.lds;*.ldsa",
            style=wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if ".lds" not in path.lower():
                path = path+".lds"
            print "You chose the following file(s):",
            print path
            self.TcLocation.SetEditable(False)
            self.TcLocation.SetValue(path)
            self.TcProjectName.SetEditable(True)
            self.TcProjectName.SetValue(_("Projekt bez názvu z %s.") %str(datetime.datetime.utcnow()))
            self.prj.ProjectFile = self.TcLocation.GetValue()
            self.prj.ProjectName = self.TcProjectName.GetValue()
            self.prj.load(path = path)
            self.prj.new()
        dlg.Destroy()
        

    def OnOpenProject(self, widget=None):
        dlg = wx.FileDialog(
            self, message="Vyber projektovy soubor", wildcard = "ProjectFile (*.lds,*.ldsa)|*.lds;*.ldsa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following file(s):",
            print path
            self.TcLocation.SetEditable(False)
            self.TcLocation.SetValue(path)
            self.TcProjectName.SetEditable(False)
            self.TcProjectName.SetValue(path)
            self.prj.load(path = path)
        dlg.Destroy()

    def OnLoadProject(self, widget=None):
        self.prj.ProjectFile = self.TcLocation.GetValue()
        self.prj.ProjectName = self.TcProjectName.GetValue()
        self.MakeModal(False)
        self.status = True
        self.Destroy()
        return self.status
        
    def UpdateUI(self, widget=None):
        print "Update load screen"

    def status(self):
        return self.status



##########################################################################################################
##########################################################################################################

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

class LinuxDeepStacker(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + "Err.: " + _("Není otevřen žádný projekt"), prj = None, app = None):
        self.app = app
        self.prj = prj
        self.parent = parent
        wx.Frame.__init__(self, self.parent, id, title, size=(800, 500))
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
            LoadProject(self, prj = prj)

    def CreatePage(self, notebook, caption):
        '''
        Creates a simple :class:`Panel` containing a :class:`TextCtrl`.

        :param `notebook`: an instance of `FlatNotebook`;
        :param `caption`: a simple label.
        '''

        p = wx.Panel(notebook)
        wx.StaticText(p, -1, caption, (20,20))
        wx.TextCtrl(p, -1, "", (20,40), (150,-1))
        return p

##########################################################################################################
##########################################################################################################

class main:
    def __init__(self, argv):
        self.argv = argv
        self.app = wx.App()
        self.prj = ProjectClass(self.argv)                              # Stará se o projekt a práci s ním Otevirani, Cteni , Ukladaní, atd....
        self.LDS = LinuxDeepStacker(app=self.app, prj = self.prj)       # Stará se o UI
        self.app.MainLoop()