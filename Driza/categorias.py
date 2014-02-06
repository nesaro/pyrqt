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

"""Gestion de categorias"""

import logging
LOG = logging.getLogger(__name__)

def conv_categorias_arbol(nombre, conjuntoscategorias):
    """Genera un arbol a partir de un conjunto de categorias. 
    Las categorias se cargan de las descripciones de operacion
    En cada nivel se escoge como rama la categoria que tiene mas subcategorias
    """
    arbolsalida = Arbol(nombre)
    listahijos = []
    listacompuestos = []
    # Elementos longitud 1
    listaintroducidos = []
    for categorias in conjuntoscategorias:
        if len(categorias) <= 1:
            if not categorias[0] in listaintroducidos:
                listahijos.append(Arbol(categorias[0]))
                listaintroducidos.append(categorias[0])
        else:
            listacompuestos.append(categorias)
    # Elemento longitud n (llamada recursiva)
    elementomasfrecuente = moda_lista(listacompuestos)
    import copy
    copialistacompuestos1 = copy.deepcopy(listacompuestos)
    copialistacompuestos2 = copy.deepcopy(listacompuestos)
    while elementomasfrecuente:
        listalistasconelemento = []
        for listaelemento in copialistacompuestos1:
            if elementomasfrecuente in listaelemento:
                listalistasconelemento.append(listaelemento)
                copialistacompuestos2.remove(listaelemento)
                listaelemento.remove(elementomasfrecuente)
        miarbol = conv_categorias_arbol(elementomasfrecuente, listalistasconelemento)
        listahijos.append(miarbol)
        elementomasfrecuente = moda_lista(copialistacompuestos2)
        copialistacompuestos1 = copy.deepcopy(copialistacompuestos2)
    # Elementos disjuntos
    for lista in listacompuestos:
        miarbol = conv_categorias_arbol(lista[0], [lista[1:]])
        listahijos.append(miarbol)
    arbolsalida.setenlaces(listahijos)
    return arbolsalida

def moda_lista(listalistas):
    """Dada una lista con listas de cadenas, 
    devuelve aquella cadena que es la más frecuente"""
    diccionariofrecuencia = dict()
    for lista in listalistas:
        for elemento in lista:
            if not diccionariofrecuencia.has_key(elemento):
                diccionariofrecuencia[elemento] = 0
            else:
                diccionariofrecuencia[elemento] += 1
    maximo = 0
    resultado = None
    for (elemento, frecuencia) in diccionariofrecuencia.items():
        if frecuencia > maximo:
            maximo = frecuencia
            resultado = elemento
    return resultado

class Arbol:
    """Un arbol n-ario. Sirve para representar la jerarquia de categorias de operaciones"""
    def __init__(self, contenido):
        self.contenido = contenido
        self.enlaces = []

    def setenlaces(self, enlaces):
        """Establece los hijos del arbol"""
        for enlace in enlaces:
            if not isinstance(enlace, Arbol):
                raise TypeError
        self.enlaces = enlaces


class GestorCategorias:
    """Clase que carga y almacena las categorias.
    El indice es un conjunto (que es una lista en la que no importa el orden
    """
    def __init__(self):
        self.listacategorias = []
        self.cargar()

    def cargar(self):
        """Carga las categorias en el gestor"""
        micategoria = Categoria("Texto de prueba para descriptivo","Descriptivo")
        micategoria2 = Categoria("Texto de prueba para CH","Contraste de Hipotesis")
        self.listacategorias = [micategoria, micategoria2]

    def has_key(self, key):
        """Devuelve verdadero si existe la categoria"""
        from sets import Set
        if not isinstance (key, Set):
            assert TypeError
        for categoria in self.listacategorias:
            if categoria.etiquetas == key:
                return True
        return False

    def __getitem__(self, key):
        """Operador []"""
        if not self.has_key(key):
            raise IndexError
        for categoria in self.listacategorias:
            if categoria.etiquetas == key:
                return categoria
    
    def obtener_categoria(self, key):
        """Equivalente a [], solo que si no encuentra el valor
        devuelve False en vez de una excepción"""
        from sets import Set
        if not isinstance (key, Set):
            assert TypeError
        for categoria in self.listacategorias:
            if categoria.etiquetas == key:
                return categoria
        return False

    def obtener_categoria_aprox(self, key):
        """Devuelve el label Mas cercano a la definicion que se nos pide.
        key es una lista ordenada, el elemento general esta por la izquierda"""
        from sets import Set
        if not isinstance(key, list):
            assert TypeError
        copialista = key[:]
        while copialista:
            if self.obtener_categoria(Set(copialista)):
                return self.obtener_categoria(Set(copialista))
            else:
                copialista = copialista[1:]
        LOG.debug("No encontre ningun subconjunto de labels")
        return False

        
      
class Categoria:
    """Clase que representa una categoria a la que puede pertenecer una operación.
    Incluye un texto que sirve como descripcion.
    No la identifica un nombre, sino un conjunto de etiquetas"""
    def __init__(self, texto, *etiquetas):
        for etiqueta in etiquetas:
            if not isinstance(etiqueta, str):
                raise TypeError
        self.descripcion = texto
        from sets import Set
        self.etiquetas = Set(etiquetas)

