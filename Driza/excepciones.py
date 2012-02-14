#!/usr/bin/python
# -*- coding: utf-8 -*-
#

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

"""Todas las excepciones definidas para el programa"""

class FicheroExisteException(Exception):
    """
    Define la excepcion que sera lanzada cuando se intente escribir 
    un fichero existente
    """
    def __init__(self, nombrefichero):
        Exception.__init__(self)
        self.fichero = nombrefichero

class FicheroNoExisteException(Exception):
    """
    Define la excepcion que sera lanzada cuando se intente 
    abrir un fichero inexistente
    """
    def __init__(self, nombrefichero):
        Exception.__init__(self)
        self.fichero = nombrefichero

class FicheroTipoDesconocidoException(Exception):
    """
    Define la excepcion que sera lanzada cuando se intente 
    abrir un fichero de tipo desconocido
    """
    def __init__(self, nombrefichero):
        Exception.__init__(self)
        self.fichero = nombrefichero

class FicheroErroneoException(Exception):
    """
    Define la excepcion que sera lanzada cuando se intente 
    abrir un fichero corrupto o similar
    """
    def __init__(self, nombrefichero):
        Exception.__init__(self)
        self.fichero = nombrefichero

class NombreFicheroNoIndicadoException(Exception):
    """
    Define la excepcion que sera lanzada cuando no se haya definido el nombre de fichero
    """
    def __init__(self, nombrefichero):
        Exception.__init__(self)
        self.fichero = nombrefichero

class VariableExisteException(Exception):
    """
    A la hora de añadir una nueva variable en los datos, 
    indica que ya existe
    """
    pass

class VersionAnterior(Exception):
    """Determina que la version cargada es anterior a la actual2"""
    def __init__(self, configuracion):
        Exception.__init__(self)
        self.configuracion = configuracion

class TipoIncorrectoException(Exception):
    """excepcion para argumentos de tipo incorrecto en las funciones"""
    def __init__(self, tipoesperado, tiporecibido):
        Exception.__init__(self)
        self.tipoesperado = tipoesperado
        self.tiporecibido = tiporecibido

class OpcionesIncorrectaException(Exception):
    """Excepcion que ocurre cuando se pasan los parametros incorrectamente"""
    def __init__(self):
        Exception.__init__(self)

class SeleccionIncorrectaException(Exception):
    """Excepcion que ocurre cuando se hace una seleccion incorrecta en una tabla"""
    def __init__(self):
        Exception.__init__(self)
