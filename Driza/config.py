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

class ListaFicheros(list):
    """
    Contenedor de la lista de ficheros. 
    Funciona como cola LIFO, y hereda de list.
    El parametro pasado es la longitud de lista que se desea
    """
    def __init__(self, size, lista=None):
        """
        El parametro size es la longitud de lista que se desea
        """
        self.__nelementos = size
        if isinstance(lista, list):
            list.__init__(self, lista)
        else:
            list.__init__(self)

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
    config = Configuracion()
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
    #Volvemos a poner a un tipo ListaFicheros
    config["lfichero"] = ListaFicheros(5, config["lfichero"].split(","))

class GestorConfig:
    """
    Gestor de configuracion. Se encarga de controlar si esta cargada la configuracion
    si el formato es el más actual, y mantiene una referencia al propio objeto
    de configuración
    """
    def __init__(self):
        import os
        self.__fichero = os.environ["HOME"]+"/.driza"
        self.configuracion = None

    def cargar(self, fichero = None):
        """Carga un fichero de configuracion, por defecto ~/.driza"""
        from Driza.excepciones import VersionAnterior
        nuevo = False
        if fichero:
            self.__fichero = fichero
        configuracion = None
        try:
            configuracion = cargar_config(self.__fichero)
        except IOError:
            nuevo = True
            configuracion = Configuracion()
            guardar_config(configuracion, self.__fichero)
        except VersionAnterior(configuracion):
            #Aqui van las correcciones para cada revision
            if configuracion["version"] < 2:
                del configuracion["primeravez"]
                configuracion["nundo"] = 5
                configuracion["decimales"] = 3
            configuracion["version"] = 2

            self.configuracion = configuracion
        
        self.configuracion = configuracion
        return nuevo #Devuelve si el fichero es nuevo o no
            
    def guardar(self, fichero = None):
        """Guarda el fichero de configuracion en un fichero"""
        if fichero:
            self.__fichero = fichero
        guardar_config(self.configuracion, self.__fichero)


class Configuracion(dict):
    """Redefinición de diccionario que contiene todos los valores de la configuración.
    Posee funciones para exportación a texto"""
    def __init__(self):
        dict.__init__(self)
        listaficheros = ListaFicheros(5)
        #Entero que representa la versión del formato de configuración
        self.__setitem__("version", 2) 
        #Directorio de trabajo temporal
        self.__setitem__("tmpdir", "/tmp")
        #Lista de los últimos ficheros abiertos
        self.__setitem__("lfichero", listaficheros)
        #Decimales a mostrar en la salida
        self.__setitem__("decimales", 3)
        #Número de niveles de deshacer
        self.__setitem__("nundo", 5)
        #Determina si se muestra la ventana splash
        self.__setitem__("vsplash", True)

    def cargar_diccionario(self, diccionario):
        """Rellena los valores a partir de un diccionario"""
        self.__setitem__("version", diccionario["version"])
        self.__setitem__("tmpdir", diccionario["tmpdir"])
        self.__setitem__("lfichero", ListaFicheros(5, diccionario["lfichero"].split(',')))
        self.__setitem__("decimales", eval(diccionario["decimales"]))
        self.__setitem__("nundo", eval(diccionario["nundo"]))
        self.__setitem__("vsplash", eval(diccionario['vsplash']))
