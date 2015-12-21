#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser
import sys
import time
import datetime
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


class ProjectWindow(object):
    def __init__(self, parent, home, name):
        self.parent = parent
        self.pathHome = home
        self.projectName = name 

    def general(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("LinuxDeepStackerData | "+self.projectName)
        self.window.set_icon_from_file("icon.ico")
        self.window.show_all()
        gtk.main()
        



class LinuxDeepStacker(object):
    def __init__(self):
        self.pojectTypeWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.pojectTypeWindow.connect("destroy", gtk.main_quit)
        self.pojectTypeWindow.set_title("LinuxDeepStackerData | type chooser")
        self.pojectTypeWindow.set_icon_from_file("icon.ico")
        settings = gtk.settings_get_default()
        settings.props.gtk_button_images = True
        vbox = gtk.VBox(False, 8)

        ### Část s texteboxem jako název projektu
        label_projectName = gtk.Label("Název:")
        text_projectName = gtk.Entry(max=128)
        text_projectName.set_text(str(datetime.datetime.now().isoformat()))

        ### Část se seznamem jako typ projektu
        label_typechoose = gtk.Label("Vyberte typ projektu:")

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # tady pak bude listwiev

        # Tlačítka s Zavřít, Nový a Opevřít
        Hbox_potvrdit = gtk.HBox(False, 8)
        BtnCancel = gtk.Button(stock=gtk.STOCK_CLOSE)
        Hbox_potvrdit.pack_start(BtnCancel, True, True, 0)
        BtnApply = gtk.Button(stock=gtk.STOCK_NEW)
        Hbox_potvrdit.pack_start(BtnApply, True, True, 0)
        BtnOpen = gtk.Button(stock=gtk.STOCK_OPEN)
        Hbox_potvrdit.pack_start(BtnOpen, True, True, 0)

        # zařazení do poliček
        vbox.pack_start(label_projectName, False, False, 0)
        vbox.pack_start(text_projectName, False, False, 0)
        vbox.pack_start(label_typechoose, False, False, 0)
        vbox.pack_start(sw, True, True, 0)
        vbox.pack_start(Hbox_potvrdit, False, False, 0)

        self.statusbar = gtk.Statusbar()
        vbox.pack_start(self.statusbar, False, False, 0)
        self.pojectTypeWindow.add(vbox)
        self.pojectTypeWindow.show_all()

        BtnCancel.connect("clicked", gtk.main_quit)
        BtnApply.connect("clicked", self.NewProject, text_projectName.get_text())
        BtnOpen.connect("clicked", gtk.main_quit)
        

    def main(self):
        gtk.main()

    def NewProject(self, widget, *data):
        print widget, data
        try:
            home = str(expanduser("~"))+"/.LinuxDeepStacker/"+str(data[0]+str("/"))
        except Exception, e:
            print "Soubor již existuje"
        os.makedirs(home)
        self.openGeneralWin(data[0], home)

    def openGeneralWin(self, projectName, ProjectHome):
        print projectName, ProjectHome
       # os.chdir(ProjectHome)
        self.pojectTypeWindow.destroy() 
        self.ProjectWindow = ProjectWindow(self, ProjectHome, projectName)
        self.ProjectWindow.general()       
