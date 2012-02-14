#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez, Inmaculada Luengo Merino

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

"""Módulo con las listas de elementos fijos usadas en el programa"""

from Driza.operaciones import OperacionCalculo, OperacionCasos
from Driza.iuqt4.operaciones import wopciones
from Driza.datos import variables
from Driza.salida import componenteresultado
from Driza.iuqt4.operaciones import seleccion

TIPOSOPERACION = {
        "Calculo":{"nombre":"Calculo","clase":OperacionCalculo},
        "Casos":{"nombre":"Casos","clase":OperacionCasos}
        }

TIPOSWIDGETOPCIONESQT3 = {
        "SeleccionSimple":{"clase":wopciones.EWOSeleccionSimple},
        "SeleccionMultiple":{"clase":wopciones.EWOSeleccionMultiple},
        "ListaSimple":{"clase":wopciones.EWOListaSimple},
        "EntradaTexto":{"clase":wopciones.EWOEntradaTexto},
        "Texto":{"clase":wopciones.EWOEtiqueta},
        "Variables":{"clase":wopciones.EWOListaVariables},
        "Factores":{"clase":wopciones.EWOListaFactores}
        }

TIPOSWIDGETOPERACIONESQT3 = {
        "Variable":{
            "seleccion":seleccion.SelectorVariable},
        "VariableVariable":{
            "seleccion":seleccion.SelectorVariableVariable},
        "VariableCaso":{
            "seleccion":seleccion.SelectorDiscriminadorSimple},
        "VariableCasoCaso":{
            "seleccion":seleccion.SelectorDiscriminadorDoble},
        "VariableVariableCaso":{
            "seleccion":seleccion.SelectorVariableDiscriminadorSimple},
        "VariableCasoCasoVariableVariable":{
            "seleccion":seleccion.SelectorVariableVariableDiscriminadorDoble},
        "DiscriminadorCasoCasoVariable":{
            "seleccion":seleccion.SelectorVariableDiscriminadorDoble}
        }

TIPOSWIDGETOPCIONESQT4 = {
        "SeleccionSimple":{"clase":wopciones.EWOSeleccionSimple},
        "SeleccionMultiple":{"clase":wopciones.EWOSeleccionMultiple},
        "ListaSimple":{"clase":wopciones.EWOListaSimple},
        "EntradaTexto":{"clase":wopciones.EWOEntradaTexto},
        "Texto":{"clase":wopciones.EWOEtiqueta},
        "Variables":{"clase":wopciones.EWOListaVariables},
        "Factores":{"clase":wopciones.EWOListaFactores}
        }

TIPOSWIDGETOPERACIONESQT4 = {
        "Variable":{
            "seleccion":seleccion.SelectorVariable},
        "VariableVariable":{
            "seleccion":seleccion.SelectorVariableVariable},
        "VariableCaso":{
            "seleccion":seleccion.SelectorDiscriminadorSimple},
        "VariableCasoCaso":{
            "seleccion":seleccion.SelectorDiscriminadorDoble},
        "VariableVariableCaso":{
            "seleccion":seleccion.SelectorVariableDiscriminadorSimple},
        "VariableCasoCasoVariableVariable":{
            "seleccion":seleccion.SelectorVariableVariableDiscriminadorDoble},
        "DiscriminadorCasoCasoVariable":{
            "seleccion":seleccion.SelectorVariableDiscriminadorDoble}
        }

TIPOSAGRUPADOR = {
        "Real":{
            "clasevariable":variables.Real, 
            "diccionarioconversion":{
                "Agrupador":["CDefault"], 
                "Entero":["CRedondeoInferior"], 
                "Ordinal":["CRedondeoInferior"]}, 
            "numerico":True,
            "numerodecimales":3,
            "valorpordefecto":"NA"},
        "Entero":{
            "clasevariable":variables.Entero, 
            "diccionarioconversion":{
                "Agrupador":["CDefault"], 
                "Ordinal":["CIgualdad"], 
                "Real":["CIgualdad"]},
            "discreto":True,
            "numerico":True,
            "etiquetable":True,
            "valorpordefecto":"NA"},
        "Logico":{
            "clasevariable":variables.Logico, 
            "diccionarioconversion":{
                "Agrupador":["CDefault"]}, 
            "discreto":True,
            "valorpordefecto":"NA"}, 
        "Ordinal":{
            "clasevariable":variables.Entero,
            "diccionarioconversion":{
                "Agrupador":["CDefault"], 
                "Entero":["CIgualdad"], 
                "Real":["CIgualdad"]},
            "discreto":True, 
            "etiquetable":True,
            "valorpordefecto":"NA"},
        "Factor":{
            "clasevariable":variables.Factor, 
            "diccionarioconversion":{
                "Agrupador":["CDefault"]}, 
            "discreto":True,
            "valorpordefecto":""}}

ELEMENTOSSALIDA = {
        "Texto":{"clase":componenteresultado.DefinicionElementoResultadoParrafo},
        "Tabla":{"clase":componenteresultado.DefinicionElementoResultadoTabla},
        "Fila":{"clase":componenteresultado.DefinicionElementoResultadoFila},
        "Imagen":{"clase":componenteresultado.DefinicionElementoResultadoImagen}
        }


def nombrevariables():
    """ La lista de los tipos que soporta driza """
    return ("Entero", "Real", "Factor", "Logico", "Ordinal")


def extensiones_fichero():
    """ Lista los tipos de fichero soportados por driza """
    return ["driza"]

def extensiones_importar():
    """ Lista con las extensiones de formatos de importacion aceptados"""
    return ["txt"]
