#!/usr/bin/python
# -*- coding: utf-8 -*-

#compmedsim.py: Ejecuta una comparacion de medias simple

#Copyright (C) 2006  Inmaculada Luengo Merino, Néstor Arocha Rodríguez
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

nombre=u"Comparación de Varianzas entre dos variables"
tipo="Calculo"
diccionarioalternativa={ "nombre":u"Hipótesis alternativa", "tipo":"SeleccionSimple", "opciones":["<",">","!="]}
significacion={"nombre":u"Significación","tipo":"EntradaTexto"}
widget={"tipo":"CalculoDoble","opciones":[significacion,diccionarioalternativa]}

def funcion(dato,variable,caso,opciones):  
    from rpy import r
    diccionario={}
    lista1=[float(x) for x in dato.getCol(variable[0],caso=caso)]
    lista2=[float(x) for x in dato.getCol(variable[1],caso=caso)]
    if opciones[u"Hipótesis alternativa"]==">":
        lateral="greater"
    elif opciones[u"Hipótesis alternativa"]=="<":
        lateral="less"
    else:
        lateral="two.sided"
    diccionario["resultado"]=r.var_test(lista1,lista2,alt=lateral,conf_level=float(opciones[u"Significación"])/100)
    diccionario["confianza"]=float(opciones[u"Significación"])/100
    return diccionario

def initresultado(resultado,opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTablaDoble("resultado")
    resultado["resultado"].titulo=u"Prueba de Hipótesis"
    lista=[]
    if opciones["caso"]:
        lista.append("Caso")
    lista+=[u"Hipótesis alternativa","Valor p obtenido","Conclusion"]
    resultado["resultado"].settitulo(lista)


def interfazresultado(resultado,listaopciones,floatrender=None):
    """Este método dice como introducir los datos en la tabla"""
    lista=[]
    variable=listaopciones[0]
    caso=listaopciones[1]
    if caso:
        lista.append(caso)
    diccionario=listaopciones[2]
    lista.append(diccionario["resultado"]["alternative"])
    lista.append(diccionario["resultado"]["p.value"])
    if (diccionario["resultado"]["p.value"] < diccionario["confianza"]): 
        texto=u"Hay evidencias estadísticas de que la hipótesis alternativa es válida"
    else: 
        texto=u"No hay evidencias estadísticas de que la hipótesis alternativa sea válida"
    lista.append(texto)
    resultado["resultado"].set(variable,lista)

def comprobarentrada(opciones):  
    if not opciones.has_key(u"Significación"):
        from Driza.excepciones import OpcionesIncorrectaException
        raise OpcionesIncorrectaException




def funcionprincipal(): pass
def funcionchequeocondiciones(interfazdato): return False
def funcionchequeoentradausuario(opciones): return False
definicionresultado = []
tipo = "Casos" #FIXME: Tipo incorrecto
etiquetas = ["Otros"]
widget = {"tipo":"Variable", "opciones":[]}
