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


class StaticList:
    """Stores statics lists"""
    @property
    def TIPOSOPERACION(self):
        from Driza.operaciones import OperacionCalculo, OperacionCasos
        return {
            "Calculo":{"nombre":"Calculo","clase":OperacionCalculo},
            "Casos":{"nombre":"Casos","clase":OperacionCasos}
            }

    @property
    def TIPOSWIDGETOPCIONESQT3(self):
        from Driza.iuqt3.operaciones import wopciones
        return {
            "SeleccionSimple":{"clase":wopciones.EWOSeleccionSimple},
            "SeleccionMultiple":{"clase":wopciones.EWOSeleccionMultiple},
            "ListaSimple":{"clase":wopciones.EWOListaSimple},
            "EntradaTexto":{"clase":wopciones.EWOEntradaTexto},
            "Texto":{"clase":wopciones.EWOEtiqueta},
            "Variables":{"clase":wopciones.EWOListaVariables},
            "Factores":{"clase":wopciones.EWOListaFactores}
            }

    @property
    def TIPOSWIDGETOPERACIONESQT3(self):
        from Driza.iuqt3.operaciones import seleccion
        return {
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

    @property
    def TIPOSWIDGETOPCIONESQT4(self):
        from Driza.iuqt4.operaciones import wopciones
        return {
            "SeleccionSimple":{"clase":wopciones.EWOSeleccionSimple},
            "SeleccionMultiple":{"clase":wopciones.EWOSeleccionMultiple},
            "ListaSimple":{"clase":wopciones.EWOListaSimple},
            "EntradaTexto":{"clase":wopciones.EWOEntradaTexto},
            "Texto":{"clase":wopciones.EWOEtiqueta},
            "Variables":{"clase":wopciones.EWOListaVariables},
            "Factores":{"clase":wopciones.EWOListaFactores}
            }

    @property
    def TIPOSWIDGETOPERACIONESQT4(self):
        from Driza.iuqt4.operaciones import seleccion
        return {
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

    @property
    def TIPOSAGRUPADOR(self):
        from Driza.datos import variables
        return {
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

    @property
    def ELEMENTOSSALIDA(self):
        from Driza.salida import componenteresultado
        return {
            "Texto":{"clase":componenteresultado.DefinicionElementoResultadoParrafo},
            "Tabla":{"clase":componenteresultado.DefinicionElementoResultadoTabla},
            "Fila":{"clase":componenteresultado.DefinicionElementoResultadoFila},
            "Imagen":{"clase":componenteresultado.DefinicionElementoResultadoImagen}
            }

    @property
    def nombrevariables(self):
        """ La lista de los tipos que soporta driza """
        return ("Entero", "Real", "Factor", "Logico", "Ordinal")


    @property
    def extensiones_fichero(self):
        """ Lista los tipos de fichero soportados por driza """
        return ["driza"]

SL = StaticList()

