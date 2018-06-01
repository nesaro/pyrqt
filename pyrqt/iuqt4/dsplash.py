#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez

#This file is part of pyrqt.
#
#pyrqt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#pyrqt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyrqt; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Dialogo splash que precede a la ventana principal"""
#textBrowser1: La ventana con las opciones
#pixmapLabel1: La fotografia


from PyQt4 import QtCore,QtGui
from pyrqt.iuqt4.ui.dsplash import Ui_DialogoSplash
from PyQt4.QtGui import QMessageBox
import logging 
log = logging.getLogger("__name__")


class DSplash(QtGui.QDialog):
    """Dialogo que muestra un acceso rápido a las acciones que puede realizar el usuario"""
    def __init__(self, parent, gestortemas, config, vsalida):
        QtGui.QDialog.__init__(self, parent)
        #VARIABLES PRIVADAS
        self.ui=Ui_DialogoSplash()
        self.ui.setupUi(self)
        self.__textohtml = ""
        self.__config = config
        self.__vsalida = vsalida

        self.ui.label.setPixmap(gestortemas.portada())
        self.__conexiones()
        self.__inithtml()
        self.ui.textBrowser.append(self.__textohtml)
    
    #FUNCIONES PRIVADAS

    def __conexiones(self):
        """Bloque de conexiones"""
        from PyQt4.QtCore import SIGNAL
        #self.connect(self.ui.textBrowser,SIGNAL("sourceChanged(const QUrl & )"),self.__enlace)
        self.connect(self.ui.textBrowser,SIGNAL("anchorClicked(const QUrl & )"),self.__enlace)

    def __inithtml(self):
        """Devuelve el html que muestra la ventana"""
        self.__textohtml="<table> \\ <tr><td><a href=\"nuevo\">Nuevo Proyecto</a></td></tr> <tr> <td><a href=\"abrir\">Abrir Proyecto</a></td></tr><tr><td><hr></td></tr>"
        for i in range(len(self.__config.configuracion["lfichero"])):
            try: 
                nfichero=self.__config.configuracion["lfichero"][i]
                ristra="<tr><td><a href=\"%d\">%s</a></td></tr>" % (i,nfichero)
                self.__textohtml+=ristra
            except:
                i=4
        self.__textohtml+="<tr><td><hr></td></tr><tr><td><a href=\"salida\">Dialogo de salida</a></td></tr></table>"

    def __enlace(self, parametro):
        """Define las acciones que realizará el programa tras pulsar en un enlace"""
        log.debug("Pulsado enlace"+parametro.toString())
        parametro = parametro.toString()
        self.ui.textBrowser.setSource(QtCore.QUrl(""))
        if parametro == "nuevo":
            self.accept()
        elif parametro == "abrir":
            if self.parent().abrir_proyecto(self):
                self.accept()
        elif parametro == "0" or parametro == "1" or \
                parametro=="2" or parametro=="3" or \
                parametro=="4":
            if self.parent().abrir_proyecto(self, self.__config.configuracion["lfichero"][eval(str(parametro))]):
                self.accept()
        elif parametro == "salida":
            self.parent().hide()
            self.__vsalida.show()
            self.accept()
        else:
            self.reject()
        return

        
    def __errormsg(self,msg=None):
        if not msg:
            msg="Generado error"
        QMessageBox.critical(self,u'Error!', msg)
        


