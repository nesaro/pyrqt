#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino

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

#textBrowser1: La ventana con las opciones
#pixmapLabel1: La fotografia
"""Dialogo de ayuda"""


from Driza.iuqt3.ui.dayuda import DialogoAyuda


class DAyuda(DialogoAyuda):
    """Dialogo que muestra un acceso rápido a las acciones que puede realizar el usuario"""
    def __init__(self, parent):
        DialogoAyuda.__init__(self, parent, "Dialogo Splash")
        self.__url = ""
        self.__inithtml()
    
    #FUNCIONES PRIVADAS

    def mostrar(self, pagina):
        """Muestra la pagina solicitada"""
        import os
        self.__url = os.path.abspath(os.curdir) + "/Driza/ayuda/" + pagina + ".html"
        self.show()

    def __inithtml(self):
        """Devuelve el html que muestra la ventana"""
        import os
        self.__url = os.path.abspath(os.curdir) + "/Driza/ayuda/index.html"

    def showEvent(self, event):
        """Redefine el showEvent de qt"""
        self.textBrowser1.setSource(self.__url)
        DialogoAyuda.showEvent(self, event)


