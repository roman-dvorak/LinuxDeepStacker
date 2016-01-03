#!/usr/bin/python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages
import sys
import os
import os.path as path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name             = 'LinuxDeepStacker',
    version          = '0.01',
    packages 		 = ['LinuxDeepStacker'],
    author           = 'Roman Dvořák',
    author_email     = 'roman-dvorak@email.cz',
    description      = 'Astroimage processing app',
    long_description = 'Astroimage processing app',
    #long_description=read('README'),
    url              = 'https://github.com/roman-dvorak/LinuxDeepStacker',
    
 
    license     = 'Lesser General Public License v3',
    
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Czech',
        # 'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
