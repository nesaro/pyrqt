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

from __future__ import absolute_import

"""Funciones para la creacion/edicion de variables"""

class GestorPaquetes(dict):
    """
    Gestiona los paquetes que contendran las funciones. Estos paquetes son 
    equivalentes al modulo de python que los contiene
    """
    def __init__(self):
        dict.__init__(self)
        basicas = Paquete("basicas")
        self.basicas = basicas
        #Intenta cargar el modulo
        #Cargaria todas las funciones de este
        #Leeria una descripción del modulo 
        #(Atributo "descripcion" dentro del ficher)
        #Cada funcion tendria un parametro nombre, y otro descripcion

        #La estructura final seria:
        #{PAritmeticas:[FSuma,FResta,etc...],...} #PAritmeticas es un paquete
        # El dialogo o lo que sea consultaria a cada funcion el nombre 
        # y la descripcion

    def __getitem__(self, clave):
        """Redefine la funcion del diccionario.
        Si no encuentra el paquete asociado a la clave, busca en las funciones directamente
        """
        try:
            return dict.__getitem__(self, clave)
        except KeyError:
            funcion = self.obtener_funcion(clave)
            if not funcion:
                raise
            return funcion

    def lista_funciones(self):
        """Devuelve una lista con todos los paquetes y todas las funciones
        Prefijo determina si en el nombre se incluye la familia de la funcion
        """
        for paquete in self.items():
            lista = [funcion for funcion in paquete[1].keys()]
        return lista

    def obtener_funcion(self, texto):
        """Busca una funcion con el nombre indicado en todos los paquetes, 
        y la devuelve. Si no encuentra nada, devuelve False"""
        for paquete in self.items():
            for funcion in paquete[1].keys():
                if funcion == texto:
                    return paquete[1][funcion]
        return False

              
class Paquete(dict):
    """Representa un paquete. 
    Un paquete es un conjunto de funciones. 
    El acceso a los modulos de las funciones se hace como un diccionario
    """
    def __init__(self, nombre):
        """Inicializa el paquete, cargando como diccionario todos sus modulos"""
        dict.__init__(self)
        self.nombrereal = nombre # El nombre real del paquete
        self.__loadModules()

    def __loadModules(self):
        """Carga todas las funciones pertenecientes al paquete como modulo"""
        cargarmodulo = lambda f: __import__(f, None, None, ["pyrqt.carga.funciones"])
        ruta = "pyrqt.carga.funciones." + self.nombrereal
        modulo = cargarmodulo(ruta)
        listamiembros = dir(modulo)
        import re
        principal = re.compile('^[A-Z]+')
        nuevalista = [x for x in listamiembros if principal.match(x)]
        del nuevalista[nuevalista.index("Funcion")] #El único elemento que no interesa
        nuevalista2 = [getattr(modulo,nombremodulo)() for nombremodulo in nuevalista]
        for indicepaquete in range(len(nuevalista)):
            self.__setitem__(nuevalista[indicepaquete], \
                    nuevalista2[indicepaquete]) 
            #Ponemos valor al diccionario

class Funcion:
    """Clase padre de todas las funciones del dialogo de creacion de variables"""
    def __init__(self, nombre):
        """Todas las clases hijas deben reescribir el valor de estos atributos"""
        self.nombre = nombre

    def nombre_completo(self):
        """Devuelve el nombre completo del modulo, con su paquete"""
        return self.__module__.split(".")[-1] + "." + self.nombre

