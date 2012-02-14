#!/usr/bin/python
# -*- coding: utf-8 -*-


#Copyright (C) 2006-2007  Néstor Arocha Rodríguez
#This file is part of Driza.
#
#Driza is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#Driza is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Driza; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from Driza import VERSION
from distutils.core import setup
from glob import glob
import sys
import os

pyver = '%d.%d'%sys.version_info[0:2]
PACKAGE = 'Driza'

def _p(unix_path):
    return os.path.normpath(unix_path)

setup (name = "driza", 
        version = VERSION,
        packages=['Driza',
            'Driza.datos',
            'Driza.iuqt3', 'Driza.iuqt3.operaciones', 'Driza.iuqt3.vprincipal','Driza.iuqt3.ui',
            'Driza.salida',
            'Driza.carga', 'Driza.carga.funciones', 'Driza.carga.operaciones'],
        data_files=[(_p('/usr/lib/python%s/site-packages/Driza/carga/images/' % pyver ), glob('Driza/carga/images/*.png'))],
        scripts = ['driza-qt'])


if sys.version_info < (2, 4):
    print >>sys.stderr, 'You need at least Python 2.4 for %s %s' % (PACKAGE, VERSION)
    sys.exit(3)

