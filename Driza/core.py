#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################
#
#  DRIZA
#
###################################


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

"""
Driza Core Class
"""

from Driza.datos import datos
from Driza.datos import interfaces
from Driza.datos import funciones
from Driza import gestores
from Driza import config
from Driza import operaciones

import logging
LOG = logging.getLogger(__name__)

class DrizaCore:
    """
    Clase Driza - Es el núcleo de la aplicación. 
    Llama al resto de clases, inicializandolas con sus respectivos valores
    """
    def __init__(self, options):
        """ 
        Constructor de la clase general
        options son las opciones escogidas en la linea de comandos
        """
        self.__gestorconfig = config.GestorConfig()
        logging.info('Cargado modulo de configuracion')
        gestorpaquetes = funciones.GestorPaquetes()
        logging.info('Cargado modulo de funciones')
        esnuevo = self.__gestorconfig.cargar()
        portero = datos.PorteroDatos(self.__gestorconfig)
        idf = interfaces.InterfazDatosFicheros(portero)
        idu = interfaces.InterfazDatosUsuario(portero, gestorpaquetes)
        idr = interfaces.InterfazDatosR(portero)
        logging.info('Cargado modulo de datos')
        gestorproyectos = gestores.GestorProyectos(portero, self.__gestorconfig)
        logging.info('Cargado modulo de proyectos')
        gestoroperaciones = operaciones.GestorOperaciones(idr, self.__gestorconfig)
        logging.info('Cargado modulo de operaciones')
        if True: #En futuras revisiones se podrá decidir la interfaz
            from Driza.iuqt3.interfaz import InterfazQt3
            self.__iu = InterfazQt3(self.__gestorconfig, portero, idu, idf, \
                    gestorproyectos, gestoroperaciones, gestorpaquetes, \
                    options, esnuevo)
            logging.info('Cargado modulo de Interfaz de usuario qt3')
        else:
            from Driza.iuqt4.interfaz import InterfazQt4
            self.__iu = InterfazQt4(self.__gestorconfig, portero, idu, idf, \
                    gestorproyectos, gestoroperaciones, gestorpaquetes, \
                    options, esnuevo)
            logging.info('Cargado modulo de Interfaz de usuario qt4')

    #FUNCIONES PUBLICAS

    def cargarfichero(self, fichero):
        """Carga un fichero. Delega la tarea a la ventana principal"""
        self.__iu.vprincipal.abrir_proyecto(None, fichero)

    def bucle(self):
        """Bucle principal del programa. 
        Llama al bucle de la interfaz gráfica"""
        self.__iu.loop()
        logging.info('Finalizado Loop del interfaz de usuario')

