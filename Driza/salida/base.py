##!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino 

#This file is part of Driza.
#
#Driza is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by

#
#Driza is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Driza; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Clases base de la salida"""

class GestorFormatoResultado(dict):
    """Almacena las diferentes definiciones de resultado"""
    def __init__(self, nombre, config):
        self.__nombre = nombre
        self.__config = config
        dict.__init__(self)
        self.__listaordenada = [] #guarda los elementos ordenados

    def __setitem__(self, indice, elemento):
        """Equivalente al append de list, salvo que controla los tipos"""
        from Driza.salida.componenteresultado import DefinicionElementoResultado
        if not isinstance(elemento, DefinicionElementoResultado):
            raise TypeError
        dict.__setitem__(self, indice, elemento)
        self.__listaordenada.append(indice)

    def cargar_definicion(self, listadiccionariodefinicion):
        """Carga las definiciones del resultado 
        a partir de una lista con dicionarios (Obtenidos de la operacion)"""
        from Driza.listas import ELEMENTOSSALIDA
        for dicdefinicion in listadiccionariodefinicion:
            objeto = ELEMENTOSSALIDA[dicdefinicion["tipo"]]["clase"]
            if dicdefinicion["tipo"] == "Texto" or \
                    dicdefinicion["tipo"] == "Imagen":
                elemento = objeto(dicdefinicion) 
            elif dicdefinicion["tipo"] == "Tabla" or \
                    dicdefinicion["tipo"] == "Fila":
                diccionarioconfig = {}
                #Añade la configuración driza al diccionario
                diccionarioconfig["config"] = dict(self.__config.configuracion) 
                diccionarioconfig.update(dicdefinicion)
                elemento = objeto(dicdefinicion["nombre"], diccionarioconfig)
            else:
                raise TypeError
            self.__setitem__(dicdefinicion["nombre"], elemento)


    def renderizar(self, listaresultados):
        """Devuelve un ResultadoOperacion con todos sus elementos ya relleno"""
        resultadooperacion = ResultadoOperacion(self.__nombre)
        from Driza.salida.componentesalida import CSTexto
        titulo = CSTexto(size = 5)
        titulo.establecer(self.__nombre)
        separador = CSTexto()
        separador.establecer("<br>")
        resultadooperacion.append(titulo)
        for indice in self.__listaordenada:
            definicion = self.__getitem__(indice)
            listafiltrada = []
            for diccionario in listaresultados:
                #Solo enviamos los diccionarios destinados a ese elemento 
                listafiltrada.append(diccionario[indice]) 
            resultadooperacion.append(definicion.renderizar(listafiltrada))
            resultadooperacion.append(separador)
        return resultadooperacion


class ResultadoOperacion(list):
    """Esta clase representa un resultado, 
    que es un conjunto de DefinicionElementosresultado. 
    Posee funciones para conversion a html
    """
    def __init__(self, titulo):
        list.__init__(self)
        self.titulo = titulo


    def html(self):
        """Genera el html a partir de todos sus componentes + el titulo"""
        ristra = u""
        for elemento in self:
            ristra += elemento.html()
        return ristra
        
    def exportar_html(self, ruta):
        """Genera el html a partir de todos sus componentes + el titulo"""
        ristra = u""
        for elemento in self:
            ristra += elemento.exportar_html(ruta)
        return ristra

