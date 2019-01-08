#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino

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

"""Módulo de gestores"""

import logging
import pickle
import os
from .excepciones import FicheroTipoDesconocidoException
LOG = logging.getLogger(__name__)

def _save_pkl(fichero, content, sobreescribir=False):
    """Guardar un fichero con pickle"""
    if not sobreescribir and os.path.exists(fichero):
        from pyrqt.excepciones import FicheroExisteException
        raise FicheroExisteException(fichero)
    with open(fichero, 'w') as f:
        pickle.dump(content, f)

def _load_pkl(filepath):
    """ Carga un fichero con Pickle """
    if not os.path.exists(filepath):
        from pyrqt.excepciones import FicheroNoExisteException
        raise FicheroNoExisteException(filepath)
    with open(filepath, 'r') as f:
        return pickle.load(f) 

class GestorFicheros:
    """Clase padre de los gestores que trabajan con ficheros"""
    def __init__(self):
        self.fichero = None

    def _guardar(self, fichero=None):
        """Acciones comunes al guardar un fichero"""
        if fichero: 
            self.fichero = fichero
        if not self.fichero:
            from pyrqt.excepciones import NombreFicheroNoIndicadoException
            raise NombreFicheroNoIndicadoException


class GestorSalida(GestorFicheros):
    """
    Gestiona los ficheros de almacenamiento de resultados
    """
    def __init__(self):
        GestorFicheros.__init__(self)
        import re
        self.__dro = re.compile('.*\.dro')

    def guardar(self, contenido, fichero=None,
                sobreescribir=False):
        """Guarda un fichero de salida"""
        self._guardar(fichero)
        if not self.__dro.match(self.fichero):
            raise FicheroTipoDesconocidoException(self.fichero)
        _save_pkl(self.fichero, contenido, sobreescribir)

    def cargar(self, fichero):
        """Carga los datos del fichero indicado"""
        if not self.__dro.match(fichero):
            raise FicheroTipoDesconocidoException(fichero)
        self.fichero = fichero
        return _load_pkl(self.fichero)


class GestorProyectos(GestorFicheros):
    """
    Almacena la variable que actua como fichero.  
    Dispone además de funciones de carga y almacenamiento
    """
    def __init__(self, portero, config):
        GestorFicheros.__init__(self)
        self.__config = config
        self.__portero = portero
        import re
        self.__driza = re.compile('.*\.driza$')
        self.__txt = re.compile('.*\.txt$')


    def guardar(self, fichero=None, sobreescribir=False):
        """Guarda la copia actual de los datos en el fichero indicado"""
        tipo = "Auto"
        self._guardar(fichero)
        if not self.__driza.match(self.fichero):
            raise FicheroTipoDesconocidoException(self.fichero)
        _save_pkl(self.fichero, self.__portero.actual(), sobreescribir)
        self.__config.configuracion["lfichero"].insert(self.fichero)

    def cargar(self, fichero, tipo="Auto"):
        """Carga los datos del fichero indicado"""
        if fichero:
            self.fichero = fichero
        if not ((tipo == "Auto" and self.__driza.match(fichero)) or tipo == "Driza"):
            raise FicheroTipoDesconocidoException(fichero)
        datos = _load_pkl(self.fichero)
        self.__portero.guardar_estado()
        self.__portero.insertar_estado(datos,
                                       flagoriginal=True)
        self.__config.configuracion["lfichero"].insert(self.fichero)
