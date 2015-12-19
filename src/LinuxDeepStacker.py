
import os
import sys
import os
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



class LinuxDeepStacker(object):
    def __init__(self):
    	pass
    	self.main()
    	gtk.main()

    def main(self):
        print "ahoj"
        self.pojectTypeWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.pojectTypeWindow.connect("destroy", gtk.main_quit)
        self.pojectTypeWindow.set_title("LinuxDeepStackerData type chooser")
        self.pojectTypeWindow.show_all()