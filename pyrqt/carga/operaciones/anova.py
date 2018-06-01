#!/usr/bin/python
# -*- coding: utf-8 -*-


#Copyright (C) 2006-2008  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
#This file is part of pyrqt.
#
#pyrqt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#pyrqt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyrqt; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""Anova"""

#TODO: pasar a formato nuevo

nombre = u"Anova Simple"
#tipo = "Variable"
tipo = "Casos" #FIXME: Tipo incorrecto
etiquetas = ["Otros"]

factor = {"nombre":"Factor", "tipo":"Factores"}
widget = {"tipo":"Variable", "opciones":[factor]}

def funcion(dato, variable, caso, opciones):  
    """Funcion que convierte los datos de entrada en los resultados"""
    import rpy #pylint: disable=import-error
    diccionario = {}
    r_data = {"Variable":[], "Factor":[]}
    for x in dato.query(variable, caso = caso):
        r_data["Variable"].append(float(x))
    for x in dato.query(opciones["Factor"], caso = caso):
        r_data["Factor"].append(repr(x))

#    lista=[float(x) for x in dato.getCol(variable,caso=caso)]
#    agrupacion=[x for x in dato.getCasos(opciones["Factor"])]
#    agrupacion2=[x for x in dato.getCol(opciones["Factor"],caso=caso)]
#    mifuncion=lambda f:agrupacion.index(f)
#    agrupacionfinal=map(mifuncion,agrupacion2)
    r_data_table = rpy.with_mode(rpy.NO_CONVERSION, rpy.r.data_frame)(r_data)
    modelo = rpy.r("Variable ~ Factor")
    aov = rpy.with_mode(rpy.NO_CONVERSION, rpy.r.aov)(modelo, r_data_table)
    diccionario = rpy.r.summary(aov)
    return diccionario

def initresultado(resultado, opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTablaSimple("resultado")
    resultado["resultado"].titulo = u"Anova"
    lista = []
    if opciones["caso"]:
        lista.append("Caso")
    lista += [u"Resultado en bruto"]
    resultado["resultado"].settitulo(lista)


def interfazresultado(resultado, listaopciones, floatrender = None):
    """Este método dice como introducir los datos en la tabla"""
    lista = []
    variable = listaopciones[0]
    caso = listaopciones[1]
    if caso:
        lista.append(caso)
    diccionario = listaopciones[2]
    resultado["resultado"].set(variable, [str(diccionario)])


def comprobarentrada(opciones):  
    if not opciones["Factor"]:
        from pyrqt.excepciones import OpcionesIncorrectaException
        raise OpcionesIncorrectaException

def funcionprincipal(): pass
def funcionchequeocondiciones(interfazdato): return False
def funcionchequeoentradausuario(opciones): return False
definicionresultado = []
