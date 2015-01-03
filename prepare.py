#!/usr/bin/env python
# -*- coding: utf-8 -*-
# prepare.py

# Copyright (c) 2014-2015, Roman Dvorak, roman-dvorak@email.cz
#

import sys
import os

if __name__ == "__main__":
		
	root=sys.argv[1]

	if not os.path.exists(root+"/LDS_data"):
	    os.makedirs(root+"/LDS_data")
	if not os.path.exists(root+"/LDS_data/"):
	    os.makedirs(root+"/LDS_data/")
	if not os.path.exists(root+"/LDS_data/tmp"):
	    os.makedirs(root+"/LDS_data/tmp")
	if not os.path.exists(root+"/LDS_data/StackImages"):
	    os.makedirs(root+"/LDS_data/StackImages")
	if not os.path.exists(root+"/LDS_data/FlatFields"):
	    os.makedirs(root+"/LDS_data/FlatFields")
	if not os.path.exists(root+"/LDS_data/DarkFrames"):
	    os.makedirs(root+"/LDS_data/DarkFrames")
	if not os.path.exists(root+"/LDS_data/OUT"):
	    os.makedirs(root+"/LDS_data/OUT")