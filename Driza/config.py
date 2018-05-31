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

"""Módulo de configuracion"""


class LIFOList(list):
    """
    Contenedor de la lista de ficheros. 
    Funciona como cola LIFO, y hereda de list.
    """
    def __init__(self, size, *args, **kwargs):
        """ El parametro size es la longitud de lista que se desea """
        self.__nelementos = size
        list.__init__(self, *args, **kwargs)

    def insert(self, elemento):
        """Inserta un elemento"""
        if elemento in self:
            self.remove(elemento)
        list.insert(self, 0, elemento)
        if len(self) > self.__nelementos:
            self.pop()

def cargar_config(fichero):
    """
    Carga la configuración del fichero de configuración del programa, 
    devolviendo la configuración por defecto si no la encuentra. 
    El parametro fichero es opcional e indica un fichero alternativo 
    al de configuracion por defecto 
    """
    try:
        from ConfigParser import ConfigParser
    except ImportError:
        from configparser import ConfigParser
    configfile = ConfigParser()
    config = Configuration.default_factory()
    archivo = open(fichero,"r")
    configfile.readfp(archivo)
    config.cargar_diccionario(configfile._sections["General"])
    if config["version"] < 2:
        from Driza.excepciones import VersionAnterior
        raise VersionAnterior(config)
    archivo.close()
    return config


def guardar_config(config, fichero):
    """
    Guarda la configuracion en el fichero de configuración del programa. 
    El parametro fichero es opcional e indica un fichero alternativo al 
    de configuracion por defecto
    """
    from ConfigParser import ConfigParser
    configfile = ConfigParser()
    config["lfichero"] = ",".join(config["lfichero"])
    configfile.add_section("General")

    for oper, valor in config.items():
        configfile.set("General", oper, valor)

    archivo = open(fichero, "w")
    configfile.write(archivo)
    archivo.close()
    #Volvemos a poner a un tipo LIFOList
    config["lfichero"] = LIFOList(5, config["lfichero"].split(","))

class GestorConfig:
    """
    Gestor de configuracion. Se encarga de controlar si esta cargada la configuracion
    si el formato es el más actual, y mantiene una referencia al propio objeto
    de configuración
    """
    def __init__(self):
        import os
        self.__fichero = os.environ["HOME"]+"/.driza"
        self.configuracion = {}

    def cargar(self, fichero=None):
        """Carga un fichero de configuracion, por defecto ~/.driza"""
        from Driza.excepciones import VersionAnterior
        nuevo = False
        if fichero:
            self.__fichero = fichero
        configuracion = {}
        try:
            configuracion = cargar_config(self.__fichero)
        except IOError:
            nuevo = True
            configuracion = Configuration.default_factory()
            guardar_config(configuracion, self.__fichero)
        except VersionAnterior:
            #Aqui van las correcciones para cada revision
            if configuracion["version"] < 2:
                del configuracion["primeravez"]
                configuracion["nundo"] = 5
                configuracion["decimales"] = 3
            configuracion["version"] = 2

            self.configuracion = configuracion
        
        self.configuracion = configuracion
        return nuevo
            
    def save(self, fichero=None):
        """Guarda el fichero de configuracion en un fichero"""
        if fichero:
            self.__fichero = fichero
        guardar_config(self.configuracion, self.__fichero)


class Configuration(dict):
    """Redefinición de diccionario que contiene todos los valores de la configuración.
    Posee funciones para exportación a texto"""
    @classmethod
    def default_factory(cls):
        listaficheros = LIFOList(5)
        return cls({"version": 2,
                    "tmpdir": "/tmp",
                    "lfichero": listaficheros,
                    "decimales": 3,
                    "nundo": 5,
                    "vsplash": True})

    def cargar_diccionario(self, diccionario):
        """Rellena los valores a partir de un diccionario"""
        for field in ("tmpdir",):
            self[field] = diccionario[field]
        for field in ("version",):
            self[field] = int(diccionario[field])
        self.__setitem__("lfichero", LIFOList(5, diccionario["lfichero"].split(',')))
        self.__setitem__("decimales", eval(diccionario["decimales"]))
        self.__setitem__("nundo", eval(diccionario["nundo"]))
        self.__setitem__("vsplash", eval(diccionario['vsplash']))
