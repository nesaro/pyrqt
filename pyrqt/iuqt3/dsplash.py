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

"""Dialogo splash que precede a la ventana principal"""

from Driza.iuqt3.ui.dsplash import DialogoSplash
from qt import SIGNAL


class DSplash(DialogoSplash):
    """Dialogo que muestra un acceso rápido a las acciones que puede realizar el usuario"""
    def __init__(self, parent, gestortemas, config, vsalida):
        DialogoSplash.__init__(self, parent, "Dialogo Splash")
        #VARIABLES PRIVADAS
        self.__textohtml = ""
        self.__config = config
        self.__vsalida = vsalida

        self.pixmapLabel1.setPixmap(gestortemas.portada())
        self.__conexiones()
        self.__inithtml()
        self.textBrowser1.append(self.__textohtml)
    
    #FUNCIONES PRIVADAS

    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.textBrowser1, SIGNAL("linkClicked(const QString & )"), self.__enlace)

    def __inithtml(self):
        """Devuelve el html que muestra la ventana"""
        nuevoproyecto = "<tr><td><a href=\"nuevo\">Nuevo Proyecto</a></td></tr>"
        abrirproyecto = "<tr><td><a href=\"abrir\">Abrir Proyecto</a></td></tr>"
        self.__textohtml = "<table> " + nuevoproyecto + abrirproyecto + "<tr><td><hr></td></tr>"
        for i in range(len(self.__config.configuracion["lfichero"])):
            #Antes salia del bucle en caso de excepcion
            nfichero = self.__config.configuracion["lfichero"][i]
            ristra = "<tr><td><a href=\"%d\">%s</a></td></tr>" % (i, nfichero)
            self.__textohtml += ristra
        self.__textohtml += "<tr><td><hr></td></tr><tr><td><a href=\"salida\">Dialogo de salida</a></td></tr></table>"

    def __enlace(self, parametro):
        """Define las acciones que realizará el programa tras pulsar en un enlace"""
        parametro = parametro.latin1()
        if parametro == "nuevo":
            self.textBrowser1.setSource("")
            self.accept()
        elif parametro == "abrir":
            if self.parent().abrir_proyecto(self):
                self.accept()
            self.textBrowser1.setSource("")
        elif parametro == "0" or parametro == "1" or \
                parametro=="2" or parametro=="3" or \
                parametro=="4":
            self.textBrowser1.setSource("")
            if self.parent().abrir_proyecto(self, self.__config.configuracion["lfichero"][eval(parametro)]):
                self.accept()
        elif parametro == "salida":
            self.textBrowser1.setSource("")
            self.parent().hide()
            self.__vsalida.show()
            self.accept()
        else:
            self.reject()
        return

        

