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

"""Definicion de agrupadores de variables"""

#TODO: Aplicar decoradores como solución de diseño
#http://es.wikipedia.org/wiki/Decorator_(patr%C3%B3n_de_dise%C3%B1o)

class Agrupador:
    """Clase de tipo que es padre de todos los Agrupadores.
    Un agrupador son aquellas caracteristicas de una variable de estudio
    """
    def __init__(self, nombre, ristratipo, descripcion = "", valorpordefecto = None):
        from Driza.datos.variables import Variable
        from Driza.listas import SL
        if not isinstance(ristratipo, str):
            raise TypeError
        if not SL.TIPOSAGRUPADOR.has_key(ristratipo):
            raise NameError
        dic = SL.TIPOSAGRUPADOR[ristratipo]
        if not issubclass(dic["clasevariable"], Variable):
            raise TypeError
        self.set_name(nombre)
        self.descripcion = descripcion
        self.diccionarioconversion = dic["diccionarioconversion"]
        if valorpordefecto == None:
            self.valorpordefecto = dic["valorpordefecto"]
        else:
            self.valorpordefecto = valorpordefecto
        self.tipo = ristratipo
        if dic.has_key("numerodecimales"):
            self.numerodecimales = 3
        self.tags = [ristratipo] #Tiene una lista con las caracteristicas del agrupador
        if dic.get("etiquetable"):
            self.etiquetas = {}
            self.tags.append("etiquetable")
        if dic.get("discreto"):
            self.tags.append("discreto")
        if dic.get("numerico"):
            self.tags.append("numerico")
        self.__tipovariableasociado = dic["clasevariable"]

    def update(self, objeto):
        """Función de copia de los atributos para cualquier Agrupador.
        Sirve para hacer copias entre Agrupadores
        """
        self.__nombre = objeto.name()
        self.descripcion = objeto.descripcion

    def nuevo_item(self, valor = TypeError): #FIXME Por defecto un valor no usable 
        """Crea un nuevo item del tipo indicado"""
        if isinstance(valor, self.__tipovariableasociado):
            return self.__tipovariableasociado(self, valor)
        if valor == TypeError:
            return self.__tipovariableasociado(self, self.valorpordefecto)
        return self.__tipovariableasociado(self, valor)

    def name(self):
        return self.__nombre

    def set_name(self, name):
        """Sets var name, with alphanumeric check"""
        import re
        alphanumeric = re.compile("^\*?[a-zA-Z0-9_ ]*$")
        if not alphanumeric.match(name):
            raise NameError
        self.__nombre = name

