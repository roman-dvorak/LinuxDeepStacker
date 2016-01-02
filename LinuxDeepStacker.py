#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lds
import gettext

print gettext.bindtextdomain('cs_CZ')
print gettext.find('cs_CZ')
print gettext.textdomain('cs_CZ')
_ = gettext.gettext

print _("caption2")

if __name__ == "__main__":
    import LinuxDeepStacker.main as main
    LDS = main.Launcher()
    #LDS.main()
