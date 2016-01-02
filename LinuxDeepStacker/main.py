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

print "hallo"
gettext.bindtextdomain('cs_CZ', '')
#gettext.find('cs_CZ')
gettext.textdomain('cs_CZ')
_ = gettext.gettext

class Launcher:
    def __init__(self):
        self.app = wx.App()
        LDS = LinuxDeepStacker()
        self.app.MainLoop()

class Page_project():
    def __init__(self, parrent, notebook):
        self.page = wx.Panel(notebook)
        wx.StaticText(self.page, -1, _("caption"))
        wx.TextCtrl(self.page, -1, "aa" , size = (150,-1))
    
    def getPage(self):
        return self.page 

class LinuxDeepStacker(wx.Frame):
    def __init__(self, parent=None, id=-1, title=_("Linux deep stacker | ") + "Výběr projektu"):
        wx.Frame.__init__(self, parent, id, title, size=(300, 200))
        panel = wx.Panel(self)
        notebook = wxfnb.FlatNotebook(panel, agwStyle= wxfnb.FNB_NO_X_BUTTON | wxfnb.FNB_NAV_BUTTONS_WHEN_NEEDED | wxfnb.FNB_SMART_TABS  )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.page_project = Page_project(self, notebook)
        notebook.AddPage(self.page_project.getPage(), _("Project tab"))
        notebook.AddPage(self.CreatePage(notebook, _("caption2")), _("caption2"))

        self.Show(True)

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

'''        
    def initUI(self): 

        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)              
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)  

        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(200, 50)      
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()

'''        