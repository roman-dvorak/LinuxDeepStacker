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
import logging

logger = logging.getLogger('LPrj.py')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

gettext.bindtextdomain('cs_CZ')
gettext.textdomain('cs_CZ')
_ = gettext.gettext

class LoadProject(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + _("Výběr projektu"), prj = None):
        logger.info("LoadProject __init__ function")
        super(LoadProject, self).__init__(parent, title=title, size=(557, 410), style= wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT)
        self.parent = parent
        self.prj = prj
        self.status = False

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(1, 1)

        box = wx.BoxSizer(wx.VERTICAL)
        HeaderImage = wx.StaticBitmap(panel, bitmap=wx.Bitmap("LinuxDeepStacker/media/headerB.png"))

        BtnOpen = wx.Button(panel, wx.ID_OPEN)
        BtnNew = wx.Button(panel, wx.ID_NEW)
        BtnDone = wx.Button(panel, wx.ID_OK)
        BtnCancel = wx.Button(panel, wx.ID_EXIT)
        self.TcLocation = wx.TextCtrl(panel, -1)
        self.TcLocation.SetValue(os.path.expanduser("~"))
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
        sizer.Add(BtnCancel, pos=(8, 5), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer.Add(BtnDone, pos=(8, 6), span=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT)

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

        if self.prj.ProjectFile != None:
            self.OnLoadProject()


    def OnCloseWindow(self, widget=None):
        logger.info("OnCloseWindow")
        self.Close()
        self.parent.Close()
        self.status = False
        self.MakeModal(False)

    def OnCreateProject(self, widget=None):
        logger.info("OnCreateProject")
        dlg = wx.FileDialog(
            self, message="Vyber projektovy soubor", wildcard = "ProjectFile (*.lds,*.ldsa)|*.lds;*.ldsa",
            style=wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if ".lds" not in path.lower():
                path = path+".lds"
            self.TcLocation.SetEditable(False)
            self.TcLocation.SetValue(path)
            self.TcProjectName.SetEditable(True)
            self.TcProjectName.SetValue(_("Projekt bez názvu z %s.") %str(datetime.datetime.utcnow()))
            self.prj.ProjectFile = self.TcLocation.GetValue()
            self.prj.ProjectName = self.TcProjectName.GetValue()
            self.prj.ProjectLoadType = 4
        dlg.Destroy()
        
    def OnOpenProject(self, widget=None):
        logger.info("OnOpenProject")
        dlg = wx.FileDialog(
            self, message="Vyber projektovy soubor", wildcard = "ProjectFile (*.lds,*.ldsa)|*.lds;*.ldsa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.prj.ProjectLoadType = 2
            path = dlg.GetPath()
            self.TcLocation.SetEditable(False)
            self.TcLocation.SetValue(path)
            self.TcProjectName.SetEditable(False)
            self.TcProjectName.SetValue("Uneable to read project name, try continue")
            self.prj.load(path = path)
        dlg.Destroy()
        self.MakeModal(False)
        self.status = True
        self.Destroy()

    def OnLoadProject(self, widget=None):
        logger.info("OnLoadProject")
        if self.prj.ProjectLoadType != -1:
            if self.prj.ProjectLoadType == 4:
                print "novy soubor skrz Gui"
                self.prj.ProjectFile = self.TcLocation.GetValue()
                self.prj.ProjectName = self.TcProjectName.GetValue()
                self.prj.new()
            elif self.prj.ProjectLoadType == 1:
                logger.debug("loading project from comand line parametr")
                self.prj.load(path = self.prj.ProjectFile)
            else:
                self.prj.ProjectFile = self.TcLocation.GetValue()
                self.prj.ProjectName = self.TcProjectName.GetValue()
                self.prj.load(path = self.prj.ProjectFile)
            self.MakeModal(False)
            self.status = True
            self.Destroy()
            return self.status
        
    def UpdateUI(self, widget=None):
        logger.info("UpdateUI")
        print "Update load screen"

    def status(self):
        return self.status