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

"""Diagrama de barras"""

nombre = u"Diagrama de barras"
tipo = "Calculo"
etiquetas = ["Descriptivos"]
widget = {"tipo":"Variable", "opciones":[]}
definicionresultado = [ 
        {"tipo":"Imagen","nombre":"Diagrama de Barras"}
        ]

def funcionprincipal(dato, variable, opciones): 
    from rpy import r
    diccionario = {"Diagrama de Barras":{}}
    lista = dato.query(variable)
    import random
    nombrefichero = "/tmp/driza" + str(random.randint(1, 99999)) + ".png"
    diccionario["Diagrama de Barras"]["ruta"] = nombrefichero
    r.png(nombrefichero) #Directorio temporal de la config
    r.barplot(lista, main = variable, axisnames = True, axes = True)
    r.dev_off()
    return diccionario


def funcionchequeoentradausuario(opciones):  
    return True

def funcionchequeocondiciones(interfazdato):
    return True

