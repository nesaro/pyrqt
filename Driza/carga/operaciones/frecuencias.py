#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
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

"""Operacion Frecuencias"""

nombre="Frecuencias"
tipo="Casos"
etiquetas=["Descriptivos"]

#Definicion widget
widget={"tipo":"Variable","opciones":[]} #FIXME cambiar el formato de esta descripcion

#Definicion del formato de resultados
definicionresultado = [
        {"tipo":"Fila","nombre":"Frecuencias","disposicion":"Horizontal","cabecera":["Variable","Caso","Frecuencia"]}]


def funcionprincipal(dato,variable,caso,opciones):
    diccionario={"Frecuencias":{}}
    condicion1=variable+"="+caso
    lista=dato.query(variable,condicion1)
    diccionario["Frecuencias"]["Variable"] = variable
    diccionario["Frecuencias"]["Caso"] = caso
    diccionario["Frecuencias"]["Frecuencia"] = len(lista)
    return diccionario


def funcionchequeoentradausuario(opciones):  
    return True

def funcionchequeocondiciones(interfazdato):
    return True

