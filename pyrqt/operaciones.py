#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007   Néstor Arocha Rodríguez, Inmaculada Luengo Merino

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

"""Clases de operaciones"""

from __future__ import absolute_import
import logging
LOG = logging.getLogger(__name__)


class GestorOperaciones(dict):
    """
    Gestiona las operaciones que están activas en la ejecución 
    del programa
    """
    def __init__(self, dato, config):
        dict.__init__(self)
        self.__idr = dato
        self.__config = config
        self.listamodulosdefectuosos = []
        self.__init_integrado() 

    def __init_integrado(self):
        """Esta funcion carga en el diccionario las operaciones"""
        from .listas import SL
        modules = self.__lista_modulos()
        for operacion in modules:
            try:
                tipo = operacion.tipo
                widget = operacion.widget
                definicionresultado = self.__cargar_definiciones(\
                        operacion.nombre, operacion.definicionresultado)
                if SL.TIPOSOPERACION.has_key(tipo):
                    objetooperacion = SL.TIPOSOPERACION[tipo]["clase"]
                    mioperacion = objetooperacion(operacion.nombre, \
                            self.__idr, operacion.etiquetas, widget, \
                            definicionresultado,operacion.funcionprincipal, \
                            operacion.funcionchequeocondiciones, \
                            operacion.funcionchequeoentradausuario)
                else:
                    raise TypeError
                self.__setitem__(operacion.nombre, mioperacion)

            except AttributeError:
                self.listamodulosdefectuosos.append(operacion.nombre)
                LOG.exception(u"Excepcion cargando el módulo:" + operacion.nombre)

    def __lista_modulos(self):
        """Devuelve una lista con los modulos ya cargados"""
        #Sacado de:
        # http://www.diveintopython.org/functional_programming/all_together.html
        import pyrqt.carga.operaciones
        ruta = pyrqt.carga.operaciones.__path__[0]
        import os
        import re
        ficheros = os.listdir(ruta)
        del ficheros[ficheros.index("__init__.py")]
        test = re.compile(".*\.py$", re.IGNORECASE)
        ficheros = filter(test.search, ficheros)   
        filenametomodulename = lambda f: os.path.splitext(f)[0]
        modulenames = map(filenametomodulename, ficheros)
        mifuncion = lambda f: "pyrqt.carga.operaciones."+f
        modulenames = map(mifuncion, modulenames)
        mifuncion2 = lambda f: __import__(f, None, None, ["pyrqt.carga.operaciones"])
        modules = []
        for nombremodulo in modulenames:
            try:
                modules.append(mifuncion2(nombremodulo))
            except SyntaxError:
                self.listamodulosdefectuosos.append(nombremodulo)
                LOG.exception(u"Excepcion cargando el modulo del sistema: "+ nombremodulo)
        return modules


    def __cargar_definiciones(self, nombre, listadiccionariodefinicion):
        """Carga la definicion de los resultados a partir del diccionario suministrado por el modulo de la operacion"""
        from pyrqt.salida.base import GestorFormatoResultado
        fresultado = GestorFormatoResultado(nombre, self.__config)
        fresultado.cargar_definicion(listadiccionariodefinicion)
        return fresultado

    def funcionchequeocondiciones(self, nombre):
        """Realiza el chequeo de condiciones llamando a la funcion suministrada por la operacion, 
        pasando como parametros la interfazdedatos"""
        return self.__getitem__(nombre).funcionchequeocondiciones(self.__idr)

    def obtener_etiqueta(self, key):
        """Devuelve la operación que tenga esas etiquetas, o false si no las encuentra"""
        from sets import Set
        if not isinstance (key, Set):
            assert TypeError
        for operacion in self.values():
            if Set(operacion.etiquetas) == key:
                return operacion
        return False


class Operacion:
    """Clase base de las operaciones. Una operación consta de los siguientes elementos:
        -una interfaz para el usuario 
        -un procedimiento que lee los valores introducidos por el usuario
        -una descripcion de como mostrar esos datos en la salida
        -funciones de verificacion de correctitud de la entrada
        Cada subtipo reimplementa el procedimiento según lo necesita"""
    def __init__(self, nombre, interfazdatosr, etiquetas, widget, listadefinicionresultado, \
            funcionprincipal, funcionchequeocondiciones, funcionchequeoentradausuario):
        self.dato = interfazdatosr
        self.nombre = nombre
        self.listadefinicionresultado = listadefinicionresultado
        self.funcion = funcionprincipal
        self.widget = widget #FIXME Cambiar los nombres de los indices que definen al widget, 
        # seria conveniente añadir opciones para poder tener solo variables discretas, 
        # por ejemplo, sin que ello implique crear un nuevo subtipo
        self.funcionchequeocondiciones = funcionchequeocondiciones
        self.funcionchequeoentradausuario = funcionchequeoentradausuario
        self.etiquetas = etiquetas

class OperacionCalculo(Operacion):
    """Los calculos que se realizan sobre un conjunto de variables por separado"""
    def procedimiento(self, seleccion, opciones):
        """Esta funcion llama a la funcion "funcion" definida por cada operacion,
        y despues crea un objeto del tipo salida, tambien definido en cada operacion
        Finalmente, lo devuelve para la ventana de salida"""

        #Obtenemos los datos que ha introducido el usuario
        listaelementos = seleccion
        if not listaelementos:
            raise IndexError #TODO Cambiar por execpción mejor
        if not self.funcionchequeoentradausuario(opciones):
            from pyrqt.excepciones import OpcionesIncorrectaException
            raise OpcionesIncorrectaException
        lista = []
        #Guardamos en lista cada pareja, enunciado-resultado
        for elemento in listaelementos:
            lista.append(self.funcion(self.dato, elemento, opciones))
       
        
        #Creamos el resultado de salida
        resultado = self.listadefinicionresultado.renderizar(lista)

        #Devolvemos el objeto
        return resultado

class OperacionCasos(Operacion):
    """Los calculos que se realizan sobre un conjunto de variables por separado. 
    A cada variable se le suministra todos sus casos posibles. 
    Solo acepta una lista con una variable"""
    def procedimiento(self, seleccion, opciones):
        """Esta funcion llama a la funcion "funcion" definida por cada operacion, 
        y despues crea un objeto del tipo salida, tambien definido en cada operacion
        Finalmente, lo devuelve para la ventana de salida"""
        #Obtenemos los datos que ha introducido el usuario
        listaelementos = seleccion
        if not listaelementos:
            raise IndexError #TODO Cambiar por execpción mejor
        if not self.funcionchequeoentradausuario(opciones):
            from pyrqt.excepciones import OpcionesIncorrectaException
            raise OpcionesIncorrectaException
        lista = []
        #Guardamos en lista cada pareja, enunciado-resultado
        for variable in listaelementos:
            listacasos = self.dato.obtener_casos(variable)
            for caso in listacasos:
                lista.append(self.funcion(self.dato, variable, str(caso.valor), opciones))
       
        #Creamos el resultado de salida
        resultado = self.listadefinicionresultado.renderizar(lista)

        #Devolvemos el objeto
        return resultado

