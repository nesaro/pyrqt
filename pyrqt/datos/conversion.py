#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez,Inmaculada Luengo Merino
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

"""Clases de conversión de agrupadores y variables"""

import logging
LOG = logging.getLogger(__name__)

class AgenteConversion:
    """Esta clase realiza una conversion de un tipo a otro, 
    devolviendo la nueva variable y la lista de campos de registros ya transformados"""
    def __init__(self, interfazdatos):
        self.__idu = interfazdatos

    def __call__(self, variable, tipovariabledestino, metododeseado):
        from pyrqt.datos.agrupadores import Agrupador
        nuevavariable = Agrupador(variable.name, tipovariabledestino)
        nuevavariable.update(variable) #Copia de atributos de la variable
        lista = self.__idu.col(variable)
        LOG.debug("Lista de registros obtenida para la conversión de tipos:" + str(lista))
        tipofuncion = eval(metododeseado) #Devuelve el objeto funcion
        lafuncion = tipofuncion(variable, nuevavariable) #Devuelve la instancia de la funcion con las variables cargadas
        nuevalista = map(lafuncion, lista) #Pasa la funcion a la lista
        return [nuevavariable, nuevalista]

class FuncionConversion:
    """Clase padre de todas las funciones de conversion entre las TVariables"""
    def __init__(self, tvar1, tvar2):
        """Toda funcion de conversion debe conocer los dos tvariable implicados"""
        self.tvar1 = tvar1
        self.tvar2 = tvar2

class CDefault(FuncionConversion):
    """Funcion de conversion por defecto. Transforma al valor por defecto de la TVariable destino"""
    def __call__(self, var):
        return self.tvar2.valorpordefecto


class CIgualdad(FuncionConversion):
    """Funcion de conversion. Devuelve el valor de la variable 1"""
    def __call__(self, var):
        return var.valor

class CRedondeoInferior(FuncionConversion):
    """Devuelve el valor de entrada con redondeo inferior"""
    def __call__(self, var):
        if var.valor is None: 
            return None
        return int(var.valor)

