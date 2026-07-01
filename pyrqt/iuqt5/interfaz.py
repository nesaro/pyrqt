#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################
#
#  DRIZA
#
###################################


#Copyright (C) 2006-2008  Néstor Arocha Rodríguez
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

"""Interfaces a las clases de interfaz de usuario"""

from __future__ import absolute_import
from . import temas
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QMessageBox,QApplication
import logging
from .vprincipal.vprincipal import VPrincipal
from .dcrevar import DCrevar
from .dsplash import DSplash
from .vsalida import VSalida
#from .iuqt4.dimportartexto import DImportarTexto
from .. import gestores
from .operaciones.doperaciones import DOperaciones
LOG = logging.getLogger("Driza.iuqt4.interfaz")

class InterfazQt4(QApplication):
    def __init__(self,interfazconfig, portero, idu, idf, interfazproyectos,interfazoperaciones, gestorpaquetes, options, esnuevo):
        QApplication.__init__(self,[])
        #Translations
        appTranslator = QtCore.QTranslator()
        idioma = QtCore.QLocale.system().name()
        if not (appTranslator.load('driza_'+idioma+'.qm')):
            logging.info('Unable to load language translation file')
        self.installTranslator(appTranslator)

        self.__options = options
        self.__nuevo = esnuevo
        gestortemas = temas.GestorTemas()
        gestorsalida = gestores.GestorSalida()

        self.__gestorproyectos = interfazproyectos
        self.__iconfig=interfazconfig
        self.__iproyectos=interfazproyectos
        self.__ioperaciones=interfazoperaciones
        self.vprincipal = VPrincipal(self, self.__iconfig, portero, idu, self.__iproyectos, gestortemas, self.__ioperaciones)
        self.vsalida = VSalida(self, gestorsalida, gestortemas)
        self.dcrevar = DCrevar(self.vprincipal, idu, interfazconfig, gestorpaquetes)
        self.__dsplash = DSplash(self.vprincipal, gestortemas, self.__iconfig, self.vsalida)
        self.doperaciones = DOperaciones(self.vprincipal, idu, interfazoperaciones, self.vsalida)
        #self.dimportartexto = DImportarTexto(self.vprincipal, idf) #TODO: pasar a qt4
        self.vprincipal.conexiones()


    def loop(self):
        """ 
        Procedimiento Bucle principal. 
        Lanza la ventana splash despues de la principal para que obtenga el foco
        Despues espera nuevos eventos por parte del usuario
        """
        self.vprincipal.show()
        if self.__options.vsplash == None: 
            if (self.__iconfig.configuracion["vsplash"] and not self.__gestorproyectos.fichero):
                self.__dsplash.show()
        elif self.__options.vsplash:
            self.__dsplash.show()
        if self.__nuevo:
            #TODO: Que el mensaje lo muestre la ventana principal
            #Es la primera vez que se ejecuta el programa
            QMessageBox.information(self.vprincipal, 'Bienvenido', 'Parece que es la primera vez que ejecutas Driza')
        if self.__ioperaciones.listamodulosdefectuosos:
            ristra = u""
            for modulo in self.__ioperaciones.listamodulosdefectuosos:
                ristra += modulo + "\n"
            mensaje = u"Las siguientes operaciones no han podido ser cargadas:\n" + ristra
            QMessageBox.information(self.vprincipal, QtCore.QCoreApplication.translate("VPrincipal","Error loading operations"), mensaje)
        logging.info('Lanzando Bucle Principal')
        self.exec_()
        return
