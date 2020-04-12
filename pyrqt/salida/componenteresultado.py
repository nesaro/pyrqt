#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino

#This file is part of pyrqt.
#
#pyrqt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by

#
#pyrqt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyrqt; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Definicion de los componentes de los resultados"""

class DefinicionElementoResultado:
    """Esta clase define un elemento del resultado.
    En la inicialización se definen los elementos estáticos, 
    como los titulos y bordes.  Además, se ofrece una clase 
    para agregar elementos que es empleada por las clases de Operacion
    """
    def __init__(self, nombre):
        self.nombre = nombre

class DefinicionElementoResultadoTabla(DefinicionElementoResultado):
    """Define una tabla por cada resultado"""
    def __init__(self, nombre, diccionarioopciones):
        DefinicionElementoResultado.__init__(self, nombre)
        self.numerofilas = 1
        self.autoencoger = False
        self.disposicion = "Horizontal"
        self.numerodecimales = diccionarioopciones["config"]["decimales"]
        if "borde" in diccionarioopciones:
            pass #TODO
        if "autoencoger" in diccionarioopciones:
            self.autoencoger = True
        if "disposicion" in diccionarioopciones:
            self.disposicion = diccionarioopciones["disposicion"]
        if "numerofilas" in diccionarioopciones:
            self.numerofilas = diccionarioopciones["numerofilas"]
        self.cabecera = diccionarioopciones["cabecera"]

    def renderizar(self, listadiccionarios):
        """Añade una nueva tabla. El parametro ha de ser 
        una lista (filas)con listas (columnas)"""
        from pyrqt.salida.componentesalida import CSLista, CSTexto, CSTabla
        resultado = CSLista()
        titulo = CSTexto(size=3)
        titulo.establecer(self.nombre)
        resultado.append(titulo)
        if self.numerofilas > 1:
            for diccionario in listadiccionarios:
                tabla = CSTabla(self.autoencoger, disposicion = self.disposicion, \
                        decimales = self.numerodecimales)
                tabla.establecer_cabecera(self.cabecera)
                for i in range(self.numerofilas):
                    listatmp = []
                    for indice in self.cabecera:
                        listatmp.append(diccionario[i][indice])
                    tabla.append(listatmp)
                resultado.append(tabla)
        else:
            for diccionario in listadiccionarios:
                tabla = CSTabla(self.autoencoger, disposicion = self.disposicion, \
                        decimales = self.numerodecimales)
                tabla.establecer_cabecera(self.cabecera)
                listatmp = []
                for indice in self.cabecera:
                    listatmp.append(diccionario[indice])
                tabla.append(listatmp)
                resultado.append(tabla)
        return resultado


class DefinicionElementoResultadoFila(DefinicionElementoResultado):
    """Define una tabla a la que cada llamada le añade una fila"""
    def __init__(self, nombre, diccionarioopciones):
        DefinicionElementoResultado.__init__(self, nombre)
        if "borde" in diccionarioopciones:
            pass #TODO
        self.cabecera = diccionarioopciones["cabecera"]

    def renderizar(self, listadiccionarios):
        """Añade una nueva tabla. 
        El parametro ha de ser una lista (filas)con listas (columnas)"""
        from pyrqt.salida.componentesalida import CSLista, CSTexto, CSTabla
        resultado = CSLista()
        titulo = CSTexto(size=3)
        titulo.establecer(self.nombre)
        resultado.append(titulo)
        tabla = CSTabla()
        tabla.establecer_cabecera(self.cabecera)
        for diccionario in listadiccionarios:
            listatmp = []
            for indice in self.cabecera:
                listatmp.append(diccionario[indice])
            tabla.append(listatmp)
        resultado.append(tabla)
        return resultado

class DefinicionElementoResultadoParrafo(DefinicionElementoResultado):
    """Elemento compuesto por un parrafo con texto"""
    def __init__(self, nombre, diccionario = None):
        """El diccionario es leido del fichero de la operacion"""
        DefinicionElementoResultado.__init__(self, nombre)
        if diccionario:
            self.__tamanofuente = diccionario["tamanofuente"]

    def renderizar(self, diccionario):
        """El diccionario es recibido por la funcionprincipal de la operacion"""
        from pyrqt.salida.componentesalida import CSTexto
        miresultado = CSTexto()
        miresultado.establecer(diccionario["contenido"])
        return miresultado

class DefinicionElementoResultadoImagen(DefinicionElementoResultado):
    """Elemento compuesto por una Imagen"""
    def __init__(self, nombre, diccionario = None):
        """El diccionario es leido del fichero de la operacion"""
        DefinicionElementoResultado.__init__(self, nombre)
        if diccionario:
            pass
        #    self.nombre = nombre
        #    if "ruta" in diccionario:
        #        self.__ruta = diccionario["ruta"]


    def renderizar(self, listadiccionario):
        """El diccionario es recibido por la funcionprincipal de la operacion"""
        from pyrqt.salida.componentesalida import CSImagen, CSLista
        resultado = CSLista()
        for diccionario in listadiccionario:
            miresultado = CSImagen()
            miresultado.establecer_ruta(diccionario["ruta"])
            resultado.append(miresultado)
        return resultado

