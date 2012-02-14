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

#TODO: Consultar dudas
nombre=u"Comparación de proporciones entre dos variables"
tipo="Calculo"
diccionarioalternativa={ "nombre":u"Hipótesis alternativa", "tipo":"SeleccionSimple", "opciones":["<",">","!="]}
significacion={"nombre":u"Significación","tipo":"EntradaTexto"}

widget={"tipo":"2Variables3Casos","opciones":[significacion,diccionarioalternativa]}


def funcion(dato,variable,caso,opciones):  
    from rpy import r
    diccionario={}
    primertermino=variable[0]
    segundotermino=variable[1]
    condicion=primertermino[0]+"="+primertermino[1] #La condicion (ser miope por ejemplo)
    condiciongrupo1=segundotermino[0]+"="+segundotermino[1]
    totalcondicion1=len(dato.query(segundotermino[0],caso,condicion,condiciongrupo1))
    totalsincondicion1=len(dato.query(segundotermino[0],caso,condiciongrupo1))
    #proporcion1=totalcondicion1/totalsincondicion1
    condiciongrupo2=segundotermino[0]+"="+segundotermino[2]
    totalcondicion2=len(dato.query(segundotermino[0],caso,condicion,condiciongrupo2))
    totalsincondicion2=len(dato.query(segundotermino[0],caso,condiciongrupo2))
    #proporcion1=totalcondicion2/totalsincondicion2
    vector1=[totalcondicion1,totalcondicion2]
    vector2=[totalsincondicion1,totalsincondicion2]
    if opciones[u"Hipótesis alternativa"]==">":
        lateral="greater"
    elif opciones[u"Hipótesis alternativa"]=="<":
        lateral="less"
    else:
        lateral="two.sided"
    diccionario["elresultado"]=r.prop_test(vector1,vector2,alt=lateral,conf_level=float(opciones[u"Significación"])/100)
    diccionario["confianza"]=float(opciones[u"Significación"])/100
    return diccionario

def initresultado(resultado,opciones):
    """Inicializa al objeto resultado, añadiendole lo que crea conveniente"""
    resultado.addTablaDoble("resultado")
    resultado["resultado"].titulo=u"Prueba de Hipótesis"
    lista=[]
    if opciones["caso"]:
        lista.append("Caso")
    lista+=[u"resultado"]
    resultado["resultado"].settitulo(lista)


def interfazresultado(resultado,listaopciones,floatrender=None):
    """Este método dice como introducir los datos en la tabla"""
    lista=[]
    variable=listaopciones[0]
    caso=listaopciones[1]
    if caso:
        lista.append(caso)
    lista.append(str(listaopciones[2]["elresultado"]))
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
