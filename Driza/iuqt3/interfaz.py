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

"""Interfaces a las clases de interfaz de usuario"""

from Driza.iuqt3 import temas
from qt import QApplication, QMessageBox
import logging
from Driza.iuqt3.vprincipal.vprincipal import VPrincipal
from Driza.iuqt3.dcrevar import DCrevar
from Driza.iuqt3.dsplash import DSplash
from Driza.iuqt3.vsalida import VSalida
from Driza.iuqt3.dimportartexto import DImportarTexto
from Driza import gestores
from Driza.iuqt3.operaciones.doperaciones import DOperaciones
LOG = logging.getLogger("Driza.iuqt3.interfaz")

class InterfazQt3(QApplication):
    """Clase principal de la interfaz de Qt3"""
    def __init__(self, interfazconfig, portero, idu, idf, interfazproyectos, \
            interfazoperaciones, gestorpaquetes, options, esnuevo):
        QApplication.__init__(self, [])
        self.__options = options
        self.__nuevo = esnuevo
        gestortemas = temas.GestorTemas()
        gestorsalida = gestores.GestorSalida()
        LOG.info('Cargado modulo de temas')
        self.__gestorconfig = interfazconfig
        self.__gestorproyectos = interfazproyectos
        self.__ioperaciones = interfazoperaciones
        self.vprincipal = VPrincipal(self, self.__gestorconfig, portero, \
                idu, self.__gestorproyectos, gestortemas, interfazoperaciones)
        self.vsalida = VSalida(self, gestorsalida, gestortemas)
        self.dcrevar = DCrevar(self.vprincipal, idu, interfazconfig, gestorpaquetes)
        LOG.info('Cargado dialogo de creación de variables')
        self.__dsplash = DSplash(self.vprincipal, gestortemas, self.__gestorconfig, self.vsalida)
        self.doperaciones = DOperaciones(self.vprincipal, idu, interfazoperaciones, self.vsalida)
        self.dimportartexto = DImportarTexto(self.vprincipal, idf)
        self.vprincipal.conexiones()

    def loop(self):
        """ 
        Procedimiento Bucle principal. 
        Lanza la ventana splash despues de la principal para que obtenga el foco
        Despues espera nuevos eventos por parte del usuario
        """
        self.vprincipal.show()
        if self.__options.vsplash == None: 
            if (self.__gestorconfig.configuracion["vsplash"] and not self.__gestorproyectos.fichero):
                self.__dsplash.show()
        elif self.__options.vsplash:
            self.__dsplash.show()
        if self.__nuevo:
            #Es la primera vez que se ejecuta el programa
            QMessageBox.information(self.vprincipal, 'Bienvenido', 'Parece que es la primera vez que ejecutas Driza')
        if self.__ioperaciones.listamodulosdefectuosos:
            ristra = u""
            for modulo in self.__ioperaciones.listamodulosdefectuosos:
                ristra += unicode(modulo) + "\n"
            mensaje = u"Las siguientes operaciones no han podido ser cargadas:\n" + ristra
            QMessageBox.information(self.vprincipal, "Error en la carga de operaciones", mensaje)
        logging.info('Lanzando Bucle Principal')
        self.exec_loop() 
        return

