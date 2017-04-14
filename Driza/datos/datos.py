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

"""
Datos: Todas las clases relacionadas con los datos, 
y sus correspondientes metodos
"""

import logging
LOG = logging.getLogger(__name__)

class Registro(dict):
    """Almacena un registro, permitiendo el acceso tanto por el objeto variable
    como por el nombre de variable.  Esta clase garantiza que la lista de 
    valores se ajusta a los tipos de la lista de variables.
    """
    def __init__(self, lvariables):
        """ 
        Clase constructora
        lvariables es el array de variables al que esta asociado el registro
        Añade los valores por defecto para todos los atributos
        """
        dict.__init__(self)
        self.__lvariables = lvariables
    
    #FUNCIONES PUBLICAS
    def __getitem__(self, indice):
        """ Redefinicion del [] del diccionario
        Si nos pasan una ristra, comprobamos si corresponde a alguna variable
        Si nos pasan un objeto, comprobamos si se corresponde a alguna variable
        Si nos pasa un entero, devolvemos el campo asociado a la variable con ese indice
        """
        miindice = indice
        from Driza.datos.agrupadores import Agrupador
        if isinstance(indice, Agrupador):
            miindice = indice.name()
        if isinstance(indice, int):
            miindice = self.__lvariables[indice].name()
        if not (isinstance(miindice, str) or isinstance(miindice, unicode)): 
            LOG.warning(u"Tipo erroneo del registro:" + str(miindice.__class__))
            raise TypeError
        if not self.has_key(miindice): 
            nuevovalor = self.__lvariables[miindice].nuevo_item()
            self.__setitem__(miindice, nuevovalor)
            return nuevovalor
        return dict.__getitem__(self, miindice)

    def __setitem__(self, indice, valor):
        """ 
        Redefinicion de []= de la lista. Almacena en el valor 
        convertido a formato interno por la variable asociada
        """
        #import traceback
        #traceback.print_stack()
        from Driza.datos.agrupadores import Agrupador
        miindice = indice
        if isinstance(indice, Agrupador):
            miindice = indice.name()
        if isinstance(indice, int):
            miindice = self.__lvariables[indice].name()
        if not isinstance(miindice, str): 
            raise TypeError
        LOG.debug("Estableciendo valor" + str(valor) + "a:" + str(miindice))
        dict.__setitem__(self, miindice, self.__lvariables[miindice].nuevo_item\
                (valor))

    def __delitem__(self, indice):
        """Pemite hacer el del"""
        from Driza.datos.agrupadores import Agrupador
        miindice = indice
        if isinstance(indice, Agrupador):
            miindice = indice.name()
        if isinstance(indice, int):
            miindice = self.__lvariables[indice].name()
        if not isinstance(miindice, str): 
            raise TypeError
        dict.__delitem__(self, miindice)

    def establecer_valores(self, lista):
        """ 
        Esta funcion establece los valores del registro, 
        teniendo como argumento una lista o derivado . El orden debe ser el mismo que el de la lista variables
        """
        if not isinstance(lista, list):
            raise TypeError
        i = 0
        listanombrevars = self.__lvariables.arr_nombres()
        for valor in lista:
            self.__setitem__(listanombrevars[i], self.__lvariables[i].nuevo_item(valor))
            i += 1


class ListaVar(list): 
    """
    ListaVar hereda de list. Su utilidad es almacenar un conjunto de 
    variables, permitiendo recuperarlas no solo por el indice, sino por 
    el nombre.
    """
    def __getitem__(self, indice):
        miindice = self.obtener_indice(indice)
        return list.__getitem__(self, miindice)

    def __setitem__(self, indice, valor):
        list.__setitem__(self, self.obtener_indice(indice), valor)

    def __delitem__(self, indice):
        miindice = self.obtener_indice(indice)
        list.__delitem__(self, miindice)

    def __getcopy__(self):
        resultado = ListaVar()
        for i in self:
            resultado.append(i)
        return resultado

    #FUNCIONES PUBLICAS

    def lista_valores_por_defecto(self):
        """
        Devuelve una lista con las ristras de todos 
        los valores por defecto
        """
        return [x.valorpordefecto for x in self]

    def lista_nombres(self):
        """ Devuelve una lista con los nombres de las variables"""
        return [x.name() for x in self]


    def obtener_indice(self, parametro):
        """
         Permite obtener el indice de una variable a partir de su nombre, 
         del objeto, o de un entero.  Devuelve un entero.
        """
        import types
        if isinstance(parametro, int):
            return parametro
        elif parametro.__class__ == types.StringType:
            for elemento in self:  
                if elemento.name() == parametro:
                    return self.index(elemento)
        elif parametro in self:
            return self.index(parametro)
        raise IndexError


class ContenedorRegVar:
    """
    Esta clase almacena los datos del programa. Tiene dos miembros, 
    una lista de registros y una lista de variables
    """
    def __init__(self, registros = None, variables = None):
        """Inicialización del contenedor principal"""
        if not registros: 
            registros = []
        self.__reg = registros #Un array para datos
        if not variables: 
            variables = ListaVar()
        self.__var = variables #Un array de variables 

    def __deepcopy__(self, memo):
        """Reimplementación de __deepcopy__, permite una copia del objeto"""
        LOG.debug("Realizando copia del contenedor de datos")
        nuevalista = self.__var.__getcopy__()
        nuevalistaregistros = list()
        for registro in self.__reg:
            nuevoregistro = Registro(nuevalista)
            for i in range(len(registro)):
                nuevoregistro[i] = nuevalista[i].nuevo_item(registro[i].valor)
            nuevalistaregistros.append(nuevoregistro)
        resultado = ContenedorRegVar(nuevalistaregistros, nuevalista)
        memo[id(self)] = resultado
        LOG.debug("Copia de datos terminada")
        return resultado

    def registros(self):
        """Devuelve la lista de registros"""
        return self.__reg

    def variables(self):
        """Devuelve la lista de variables"""
        return self.__var




class ListaUndoRedo(list):
    """ListaUndoRedo hereda de lista. Es similar a una cola lifo.
    Los elementos almacenados son tuplas (estado,flagoriginal)
    """
    def __init__(self, tama):
        list.__init__(self)
        self.tama = tama #Almacena el tamaño almacenado

    def encolar(self, objeto, flagoriginal = False, index = 0):
        """Si pasan un indice es que quieren encolar desde alguna posición"""
        if index >= self.tama:
            raise IndexError
        else:
            if self.__len__() == self.tama:
                self.__delitem__(-1)
            del self[:index]
            self.insert(0, (objeto, flagoriginal))

    def establecer_nuevo(self, indice, valor):
        """Modifica la flag de original de un indice dado"""
        if (valor != True and valor != False):
            raise TypeError
        estadoactual = self.__getitem__(indice)[0]
        self.__setitem__(indice, (estadoactual, valor))

class PorteroDatos:
    """
    Clase de portera. Gestiona una lista con todas las copias de los datos, 
    determinando cual es la vigente y permitiendo el undo y el redo
    """
    def __init__(self, config):
        self.__index = 0 #Variable que lleva el indice
        self.__lista = ListaUndoRedo(config.configuracion["nundo"])
        self.__lista.encolar(ContenedorRegVar(), True)

    def undo(self):
        """Realiza un undo, desplazando el indice de ListaUndoRedo"""
        LOG.debug("Solicitud de undo a portero")
        if self.__index < self.__lista.tama:
            LOG.debug("Undo ha resuelto satisfactoriamente")
            self.__index += 1
        else:
            raise IndexError

    def redo(self):
        """Realiza un redo, desplazando el indice de ListaUndoRedo"""
        if self.__index > 0:
            self.__index -= 1
        else:
            raise IndexError

    def puedo_undo(self):
        """Devuelve un valor lógico indicando si es posible realizar un undo"""
        return ((self.__index<self.__lista.tama) and (len(self.__lista)>1) and \
                (self.__index<(len(self.__lista)-1)))

    def puedo_redo(self):
        """Devuelve un valor lógico indicando si es posible realizar un redo"""
        return self.__index > 0

    def guardar_estado(self, flagoriginal = False):
        """
        guarda un estado en la lista de estados, 
        creando una copia a partir del último
        La flagoriginal se activa si se esta abriendo un nuevo fichero
        """
        estadoactual = self.__lista[self.__index][0]
        import copy
        objetocopia = copy.deepcopy(estadoactual)
        self.__lista.encolar(objetocopia, flagoriginal, self.__index)
        self.__index = 0
    
    def insertar_estado(self, estado, flagoriginal = False):
        """Introduce un estado y lo encola"""
        self.__lista.encolar(estado, flagoriginal, self.__index)
        self.__index = 0

    def nuevo_estado(self, flagoriginal = False):
        """Introduce un estado nuevo y vacio"""
        self.__lista.encolar(ContenedorRegVar(), flagoriginal)
        self.__index = 0

    def actual(self):
        """Devuelve el estado vigente"""
        return self.__lista[self.__index][0]

    def actual_original(self):
        """Devuelve si el estado vigente es original"""
        return self.__lista[self.__index][1]

    def establecer_actual_original(self):
        """Establece que el estado actual es original"""
        self.__lista.establecer_nuevo(self.__index, True)

